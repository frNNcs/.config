"""Extractor de shortcuts de tmux."""

import re
from typing import List

from ..models import Shortcut
from ..ollama_client import OllamaClient
from .base import BaseExtractor


class TmuxExtractor(BaseExtractor):
    """Extractor de shortcuts de tmux."""

    # Mapeo de teclas de tmux a formato legible
    KEY_MAP = {
        "C-": "Ctrl+",
        "M-": "Alt+",
        "S-": "Shift+",
    }

    def __init__(self, config_files: List[str]):
        super().__init__("tmux", config_files)
        self.ollama = OllamaClient()
        self.prefix = "Ctrl+Space"  # Default

    def _parse_prefix(self, content: str) -> str:
        """Detecta el prefix key de la configuración de tmux."""
        # Buscar set -g prefix C-Space o similar
        prefix_match = re.search(r'set\s+-g\s+prefix\s+([^\s]+)', content)
        if prefix_match:
            prefix = prefix_match.group(1)
            return self._format_key(prefix)
        return "Ctrl+Space"  # Default

    def _format_key(self, key: str) -> str:
        """Convierte notación de tmux a formato legible."""
        # C-Space -> Ctrl+Space
        # C-M-[ -> Ctrl+Alt+[
        # M-h -> Alt+h
        result = key
        for tmux_key, readable in self.KEY_MAP.items():
            result = result.replace(tmux_key, readable)
        return result

    async def extract(self) -> List[Shortcut]:
        """Extrae shortcuts de tmux.conf.

        Returns:
            Lista de shortcuts de tmux
        """
        content = self.read_config_files()
        shortcuts: List[Shortcut] = []

        # Detectar prefix
        self.prefix = self._parse_prefix(content)

        # Regex para bindings de tmux
        bind_pattern = r'^\s*bind\s+(?:-n\s+)?(?:-r\s+)?([^\s]+)\s+(.+?)(?:\s*#.*)?$'

        lines = content.split('\n')

        for i, line in enumerate(lines):
            match = re.match(bind_pattern, line)
            if match:
                key, command = match.groups()
                command = command.strip()

                # Determinar si tiene prefijo
                has_prefix = "-n " not in line

                # Formatear la tecla
                formatted_key = self._format_key(key)

                # Construir display key con prefix real
                if has_prefix:
                    display_key = f"{self.prefix} + {formatted_key}"
                else:
                    display_key = formatted_key

                shortcut = Shortcut(
                    key=display_key,
                    description=await self._get_description(command),
                    app="tmux",
                    context=self._infer_context(command),
                    tags=["bind"],
                    raw_command=command,
                    source_file=self.config_files[0],
                    line_number=i + 1,
                )
                shortcuts.append(shortcut)

        return shortcuts

    async def _get_description(self, command: str) -> str:
        """Genera descripción del comando usando Ollama o fallback.

        Args:
            command: Comando tmux

        Returns:
            Descripción del comando
        """
        # Fallbacks comunes para evitar llamadas a Ollama innecesarias
        fallbacks = {
            "split-window -h": "Split horizontal",
            "split-window -v": "Split vertical",
            "select-pane -L": "Select pane left",
            "select-pane -R": "Select pane right",
            "select-pane -U": "Select pane up",
            "select-pane -D": "Select pane down",
            "switch-client -p": "Previous session",
            "switch-client -n": "Next session",
            "choose-tree": "Show session tree",
            "send-prefix": "Send prefix key",
        }

        for cmd, desc in fallbacks.items():
            if cmd in command:
                return desc

        # Intentar usar Ollama
        try:
            prompt = f"""
Describe this tmux command briefly (max 8 words):
{command}

Response format: Just the description, nothing else.
"""
            description = await self.ollama.generate(
                prompt=prompt,
                temperature=0.1,
                max_tokens=20,
            )
            return description.strip() or f"Execute: {command[:40]}"
        except Exception:
            return f"Execute: {command[:40]}"

    def _infer_context(self, command: str) -> str:
        """Infiere el contexto basado en el comando.

        Args:
            command: Comando tmux

        Returns:
            Contexto del comando
        """
        cmd_lower = command.lower()

        contexts = [
            ("split-window", "window management"),
            ("select-pane", "navigation"),
            ("switch-client", "session"),
            ("choose-tree", "session"),
            ("resize-pane", "resize"),
            ("copy-mode", "copy mode"),
            ("send-prefix", "prefix"),
        ]

        for pattern, context in contexts:
            if pattern in cmd_lower:
                return context

        return "general"
