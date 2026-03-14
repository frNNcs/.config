"""Extractor de shortcuts de opencode.nvim."""

import re
from pathlib import Path
from typing import List

from ..models import Shortcut
from .base import BaseExtractor


class OpencodeExtractor(BaseExtractor):
    """Extractor de shortcuts de opencode.nvim desde archivos de configuración."""

    # Mapeo de comodines de nvim a formato legible
    KEY_MAP = {
        "<leader>": "Space",
        "<localleader>": "\\",
        "<D->": "Cmd+",
        "<C->": "Ctrl+",
        "<M->": "Alt+",
        "<S->": "Shift+",
        "<CR>": "Enter",
        "<Esc>": "Escape",
        "<Tab>": "Tab",
        "<Space>": "Space",
        "<BS>": "Backspace",
        "<Del>": "Delete",
        "<Up>": "↑",
        "<Down>": "↓",
        "<Left>": "←",
        "<Right>": "→",
    }

    def __init__(self, config_files: List[str]):
        super().__init__("opencode", config_files)
        self.leader = "Space"
        self.local_leader = "\\"

    def _parse_leaders(self, content: str) -> None:
        """Detecta los leader keys."""
        leader_match = re.search(r'vim\.g\.mapleader\s*=\s*["\'](.+?)["\']', content)
        if leader_match:
            leader = leader_match.group(1)
            self.leader = "Space" if leader == " " else leader

        local_leader_match = re.search(r'vim\.g\.maplocalleader\s*=\s*["\'](.+?)["\']', content)
        if local_leader_match:
            local_leader = local_leader_match.group(1)
            self.local_leader = local_leader

    def _format_key(self, key: str) -> str:
        """Convierte notación de nvim a formato legible."""
        result = key

        # Detectar si es combinación con modificadores
        if self._has_modifier_combination(result):
            result = self._process_modifier_combinations(result)
            for vim_key, readable in self.KEY_MAP.items():
                if vim_key not in ["<D->", "<C->", "<M->", "<S->"]:
                    result = result.replace(vim_key, readable)
            return result

        # Es una secuencia
        if "<leader>" in result:
            rest = result.replace("<leader>", "")
            if rest:
                sequence = " → ".join(list(rest))
                return f"{self.leader} → {sequence}"
            else:
                return self.leader

        if "<localleader>" in result:
            rest = result.replace("<localleader>", "")
            if rest:
                sequence = " → ".join(list(rest))
                return f"{self.local_leader} → {sequence}"
            else:
                return self.local_leader

        # Reemplazar otros comodines
        for vim_key, readable in self.KEY_MAP.items():
            result = result.replace(vim_key, readable)

        return result

    def _has_modifier_combination(self, key: str) -> bool:
        """Detecta si hay combinación con modificadores."""
        return bool(re.search(r'<[SCMD]+-', key))

    def _process_modifier_combinations(self, key: str) -> str:
        """Procesa combinaciones de modificadores."""
        pattern = r'<([SCMD]+)-([^>]+)>'

        def replace_match(match):
            mods = match.group(1)
            actual_key = match.group(2)

            modifier_map = {
                'S': 'Shift',
                'C': 'Ctrl',
                'M': 'Alt',
                'D': 'Cmd',
            }

            parts = []
            for mod in mods:
                if mod in modifier_map:
                    parts.append(modifier_map[mod])

            parts.append(actual_key)
            return '+'.join(parts)

        return re.sub(pattern, replace_match, key)

    async def extract(self) -> List[Shortcut]:
        """Extrae shortcuts de opencode desde archivos de configuración."""
        shortcuts: List[Shortcut] = []

        for config_file in self.config_files:
            path = Path(config_file).expanduser()

            if path.is_dir():
                for lua_file in path.rglob("opencode*.lua"):
                    shortcuts.extend(await self._extract_from_file(lua_file))
            elif path.exists() and "opencode" in str(path):
                shortcuts.extend(await self._extract_from_file(path))

        return shortcuts

    async def _extract_from_file(self, file_path: Path) -> List[Shortcut]:
        """Extrae shortcuts de opencode de un archivo."""
        shortcuts: List[Shortcut] = []

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            return shortcuts

        # Parsear leaders
        self._parse_leaders(content)

        # Buscar keymaps de opencode - estrategia línea por línea
        lines = content.split('\n')
        current_keymap = ""
        in_keymap = False

        for i, line in enumerate(lines):
            if 'vim.keymap.set' in line:
                in_keymap = True
                current_keymap = line
                # Si la línea no termina con ')', acumular líneas
                if ')' not in line or line.count('(') != line.count(')'):
                    continue
            elif in_keymap:
                current_keymap += " " + line.strip()
                if ')' in line and current_keymap.count('(') == current_keymap.count(')'):
                    in_keymap = False
                else:
                    continue
            else:
                continue

            if not current_keymap or 'desc' not in current_keymap:
                continue

            # Extraer componentes
            # Modo(s)
            mode_match = re.search(r'\(\s*["\']([nivxtc,\s]+)["\']\s*,|\(\s*\{([^}]+)\}\s*,', current_keymap)
            modes = "n"
            if mode_match:
                modes = (mode_match.group(1) or mode_match.group(2) or "n").strip()

            # Tecla
            key_match = re.search(r',\s*["\'](<[^"\']+>|[^"\',]+)["\']\s*,', current_keymap)
            if not key_match:
                continue
            key = key_match.group(1).strip()

            # Descripción
            desc_match = re.search(r'desc\s*=\s*["\']([^"\']+)["\']', current_keymap)
            if not desc_match:
                continue
            desc = desc_match.group(1)

            # Solo incluir si la descripción menciona opencode
            if "opencode" in desc.lower():
                formatted_key = self._format_key(key)

                shortcut = Shortcut(
                    key=formatted_key,
                    description=desc,
                    app="opencode",
                    context="opencode",
                    tags=self._infer_tags(modes),
                    source_file=str(file_path),
                )
                shortcuts.append(shortcut)

        return shortcuts

    def _infer_tags(self, modes: str) -> List[str]:
        """Infiere tags de los modos."""
        mode_map = {
            "n": "normal",
            "i": "insert",
            "v": "visual",
            "x": "visual",
            "t": "terminal",
            "c": "command",
        }

        tags: List[str] = []
        for mode in modes.split(","):
            mode = mode.strip().strip('"\'')
            if mode in mode_map:
                tags.append(mode_map[mode])

        return tags
