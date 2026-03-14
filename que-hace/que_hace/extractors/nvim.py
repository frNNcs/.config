"""Extractor de shortcuts de Neovim."""

import re
from pathlib import Path
from typing import List

from ..models import Shortcut
from ..ollama_client import OllamaClient
from .base import BaseExtractor


class NvimExtractor(BaseExtractor):
    """Extractor de keymaps de Neovim desde archivos Lua."""

    # Mapeo de comodines de nvim a formato legible
    KEY_MAP = {
        "<leader>": "Space",  # Se reemplazará con el leader real
        "<localleader>": "\\",
        "<D->": "Cmd+",  # macOS Command key
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
        super().__init__("nvim", config_files)
        self.ollama = OllamaClient()
        self.leader = "Space"  # Default
        self.local_leader = "\\"  # Default

    def _parse_leaders(self, content: str) -> None:
        """Detecta los leader keys de la configuración."""
        # Buscar vim.g.mapleader
        leader_match = re.search(r'vim\.g\.mapleader\s*=\s*["\'](.+?)["\']', content)
        if leader_match:
            leader = leader_match.group(1)
            self.leader = "Space" if leader == " " else leader

        # Buscar vim.g.maplocalleader
        local_leader_match = re.search(r'vim\.g\.maplocalleader\s*=\s*["\'](.+?)["\']', content)
        if local_leader_match:
            local_leader = local_leader_match.group(1)
            self.local_leader = local_leader

    def _format_key(self, key: str) -> str:
        """Convierte notación de nvim a formato legible.
        
        Distingue entre:
        - Combinaciones simultáneas: <D-b> -> Cmd+b, <S-C-u> -> Shift+Ctrl+u
        - Secuencias: <leader>os -> Space → o → s (presionar una tras otra)
        """
        result = key
        
        # Detectar si es una combinación con modificadores (simultánea)
        if self._has_modifier_combination(result):
            # Procesar combinaciones de modificadores
            result = self._process_modifier_combinations(result)
            # Reemplazar otros comodines simples
            for vim_key, readable in self.KEY_MAP.items():
                if vim_key not in ["<D->", "<C->", "<M->", "<S->"]:
                    result = result.replace(vim_key, readable)
            return result
        
        # Es una secuencia (posiblemente con leader)
        # Separar el leader del resto de la secuencia
        if "<leader>" in result:
            rest = result.replace("<leader>", "")
            if rest:
                # Separar cada carácter de la secuencia
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
        """Detecta si la tecla contiene una combinación con modificadores."""
        # Buscar patrones como <D-b>, <C-M-[>, <S-C-u>, etc.
        return bool(re.search(r'<[SCMD]+-', key))

    def _process_modifier_combinations(self, key: str) -> str:
        """Procesa combinaciones de modificadores."""
        # Patrón para detectar <S-C-u>, <C-M-d>, etc.
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
        """Extrae keymaps de archivos Lua de nvim.

        Returns:
            Lista de shortcuts de nvim
        """
        shortcuts: List[Shortcut] = []

        # Primero, intentar leer init.lua para detectar leaders
        for config_file in self.config_files:
            path = Path(config_file).expanduser()
            if path.is_file() and "init.lua" in str(path):
                try:
                    content = path.read_text(encoding="utf-8")
                    self._parse_leaders(content)
                except Exception:
                    pass

        for config_file in self.config_files:
            path = Path(config_file).expanduser()

            if path.is_dir():
                # Buscar recursivamente archivos .lua
                for lua_file in path.rglob("*.lua"):
                    shortcuts.extend(await self._extract_from_file(lua_file))
            elif path.exists():
                shortcuts.extend(await self._extract_from_file(path))

        return shortcuts

    async def _extract_from_file(self, file_path: Path) -> List[Shortcut]:
        """Extrae keymaps de un archivo Lua.

        Args:
            file_path: Ruta al archivo Lua

        Returns:
            Lista de shortcuts extraídos
        """
        shortcuts: List[Shortcut] = []

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            return shortcuts

        # Buscar vim.keymap.set patterns
        # vim.keymap.set("n", "<leader>oa", function..., { desc = "..." })
        # vim.keymap.set({"n", "x"}, "<leader>ox", ..., { desc = "..." })

        patterns = [
            # Pattern 1: Single mode
            r'vim\.keymap\.set\s*\(\s*["\']([^"\']+)["\']\s*,\s*["\']([^"\']+)["\']\s*,[^,]+,\s*\{[^}]*desc\s*=\s*["\']([^"\']+)["\']',
            # Pattern 2: Multiple modes
            r'vim\.keymap\.set\s*\(\s*\{([^}]+)\}\s*,\s*["\']([^"\']+)["\']\s*,[^,]+,\s*\{[^}]*desc\s*=\s*["\']([^"\']+)["\']',
        ]

        for pattern in patterns:
            for match in re.finditer(pattern, content, re.DOTALL):
                groups = match.groups()
                if len(groups) == 3:
                    modes, key, desc = groups
                    modes = modes.strip()

                    # Formatear la tecla
                    formatted_key = self._format_key(key)

                    shortcut = Shortcut(
                        key=formatted_key,
                        description=desc,
                        app="nvim",
                        context=self._infer_context(key, desc),
                        tags=self._infer_tags(modes),
                        source_file=str(file_path),
                    )
                    shortcuts.append(shortcut)

        # Buscar leader definitions
        leader_match = re.search(r'vim\.g\.mapleader\s*=\s*["\'](.+?)["\']', content)
        if leader_match:
            leader = leader_match.group(1)
            leader_display = "Space" if leader == " " else leader
            shortcuts.append(
                Shortcut(
                    key=leader_display,
                    description=f"Leader key ({leader_display})",
                    app="nvim",
                    context="leader",
                    tags=["leader"],
                    source_file=str(file_path),
                )
            )

        # Buscar local leader
        local_leader_match = re.search(r'vim\.g\.maplocalleader\s*=\s*["\'](.+?)["\']', content)
        if local_leader_match:
            local_leader = local_leader_match.group(1)
            local_leader_display = self._format_key(local_leader)
            shortcuts.append(
                Shortcut(
                    key=local_leader_display,
                    description=f"Local leader ({local_leader_display})",
                    app="nvim",
                    context="leader",
                    tags=["leader", "local"],
                    source_file=str(file_path),
                )
            )

        return shortcuts

    def _infer_context(self, key: str, desc: str) -> str:
        """Infiere el contexto del keymap.

        Args:
            key: Keybinding
            desc: Descripción

        Returns:
            Contexto
        """
        key_lower = key.lower()
        desc_lower = desc.lower()

        contexts = {
            "opencode": ["opencode"],
            "neo-tree": ["neo-tree", "neotree", "tree", "file-explorer"],
            "obsidian": ["obsidian", "vault", "note", "daily"],
            "telescope": ["telescope", "find", "search", "grep"],
            "lsp": ["lsp", "diagnostic", "format", "code"],
            "git": ["git", "gitsigns", "fugitive"],
            "buffer": ["buffer", "buf"],
            "window": ["window", "win", "split"],
            "terminal": ["terminal", "term", "toggleterm"],
        }

        for context, keywords in contexts.items():
            if any(k in key_lower or k in desc_lower for k in keywords):
                return context

        return "general"

    def _infer_tags(self, modes: str) -> List[str]:
        """Infiere tags a partir de los modos.

        Args:
            modes: String con los modos (n, i, v, x, etc.)

        Returns:
            Lista de tags
        """
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
