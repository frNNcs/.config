"""Extractor de shortcuts de skhd."""

import re
from typing import List

from ..models import Shortcut
from ..ollama_client import OllamaClient
from .base import BaseExtractor


class SkhdExtractor(BaseExtractor):
    """Extractor de shortcuts de skhd (Simple Hotkey Daemon)."""

    def __init__(self, config_files: List[str]):
        super().__init__("skhd", config_files)
        self.ollama = OllamaClient()

    async def extract(self) -> List[Shortcut]:
        """Extrae shortcuts de skhdrc.

        Returns:
            Lista de shortcuts de skhd
        """
        content = self.read_config_files()
        shortcuts: List[Shortcut] = []

        lines = content.split('\n')
        current_section = ""

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Detectar secciones por comentarios
            if stripped.startswith('#'):
                section_match = re.match(r'#\s*-+\s*(.+?)\s*-+', stripped)
                if section_match:
                    current_section = section_match.group(1).strip()
                continue

            # Pattern: key_combo : command
            # alt - h : yabai -m window --focus west
            # shift + alt - r : yabai -m space --rotate 270
            if ':' in stripped and not stripped.startswith('#'):
                parts = stripped.split(':', 1)
                if len(parts) == 2:
                    key_combo = parts[0].strip()
                    command = parts[1].strip()

                    # Limpiar comentarios inline
                    if '#' in command:
                        command = command.split('#')[0].strip()

                    shortcut = Shortcut(
                        key=key_combo,
                        description=await self._get_description(command, current_section),
                        app="skhd",
                        context=self._infer_context(current_section, command),
                        tags=["yabai", "hotkey"],
                        raw_command=command,
                        source_file=self.config_files[0],
                        line_number=i + 1,
                    )
                    shortcuts.append(shortcut)

        return shortcuts

    async def _get_description(self, command: str, section: str) -> str:
        """Genera descripción del comando.

        Args:
            command: Comando yabai
            section: Sección actual

        Returns:
            Descripción del comando
        """
        # Fallbacks para comandos comunes
        fallbacks = {
            "--focus": "Focus",
            "--swap": "Swap",
            "--warp": "Warp",
            "--rotate": "Rotate",
            "--mirror": "Mirror",
            "--toggle float": "Toggle float",
            "--toggle zoom-fullscreen": "Toggle fullscreen",
            "--balance": "Balance layout",
            "--layout": "Toggle layout",
            "--stop-service": "Stop service",
            "--start-service": "Start service",
            "--restart-service": "Restart service",
            "--toggle padding": "Toggle padding",
        }

        for pattern, desc in fallbacks.items():
            if pattern in command:
                return desc

        # Usar Ollama para descripciones complejas
        try:
            prompt = f"""
Describe this yabai command briefly (max 8 words, Spanish):
Command: {command}
Section: {section}

Response: Just the description.
"""
            description = await self.ollama.generate(
                prompt=prompt,
                temperature=0.1,
                max_tokens=20,
            )
            return description.strip() or f"Execute: {command[:40]}"
        except Exception:
            return f"Execute: {command[:40]}"

    def _infer_context(self, section: str, command: str) -> str:
        """Infiere el contexto.

        Args:
            section: Sección del archivo
            command: Comando

        Returns:
            Contexto
        """
        if section:
            return section.lower().replace(' ', '_')

        cmd_lower = command.lower()
        if "window" in cmd_lower:
            return "window"
        elif "space" in cmd_lower:
            return "space"
        elif "display" in cmd_lower:
            return "display"
        elif "service" in cmd_lower:
            return "service"
        else:
            return "general"
