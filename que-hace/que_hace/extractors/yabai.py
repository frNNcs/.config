"""Extractor de configuraciones de yabai.

Aunque yabai se controla típicamente vía skhd,
este extractor documenta los comandos disponibles de yabai.
"""

from typing import List

from ..models import Shortcut
from .base import BaseExtractor


class YabaiExtractor(BaseExtractor):
    """Extractor/documentador de comandos de yabai."""

    def __init__(self, config_files: List[str]):
        super().__init__("yabai", config_files)

    async def extract(self) -> List[Shortcut]:
        """Extrae/documenta comandos de yabai.

        Como yabai no tiene keybindings directos (usa skhd),
este método documenta los comandos comunes de yabai
        que pueden ser usados en scripts o atajos.

        Returns:
            Lista de comandos documentados
        """
        shortcuts: List[Shortcut] = []

        # Comandos comunes de yabai documentados
        yabai_commands = [
            ("yabai -m window --focus west", "Focus window west", "window", "focus"),
            ("yabai -m window --focus south", "Focus window south", "window", "focus"),
            ("yabai -m window --focus north", "Focus window north", "window", "focus"),
            ("yabai -m window --focus east", "Focus window east", "window", "focus"),
            ("yabai -m window --swap west", "Swap window west", "window", "swap"),
            ("yabai -m window --swap south", "Swap window south", "window", "swap"),
            ("yabai -m window --swap north", "Swap window north", "window", "swap"),
            ("yabai -m window --swap east", "Swap window east", "window", "swap"),
            ("yabai -m window --warp west", "Warp window west", "window", "warp"),
            ("yabai -m window --warp south", "Warp window south", "window", "warp"),
            ("yabai -m window --warp north", "Warp window north", "window", "warp"),
            ("yabai -m window --warp east", "Warp window east", "window", "warp"),
            ("yabai -m window --toggle float", "Toggle window float", "window", "toggle"),
            ("yabai -m window --toggle zoom-fullscreen", "Toggle fullscreen zoom", "window", "toggle"),
            ("yabai -m window --toggle sticky", "Toggle window sticky", "window", "toggle"),
            ("yabai -m window --toggle topmost", "Toggle window topmost", "window", "toggle"),
            ("yabai -m window --toggle shadow", "Toggle window shadow", "window", "toggle"),
            ("yabai -m window --toggle border", "Toggle window border", "window", "toggle"),
            ("yabai -m space --rotate 270", "Rotate space 270°", "space", "layout"),
            ("yabai -m space --rotate 90", "Rotate space 90°", "space", "layout"),
            ("yabai -m space --mirror y-axis", "Mirror space Y-axis", "space", "layout"),
            ("yabai -m space --mirror x-axis", "Mirror space X-axis", "space", "layout"),
            ("yabai -m space --balance", "Balance window tree", "space", "layout"),
            ("yabai -m space --layout bsp", "Set BSP layout", "space", "layout"),
            ("yabai -m space --layout float", "Set float layout", "space", "layout"),
            ("yabai -m space --toggle padding", "Toggle space padding", "space", "toggle"),
            ("yabai -m space --toggle gap", "Toggle window gap", "space", "toggle"),
            ("yabai -m display --focus west", "Focus display west", "display", "focus"),
            ("yabai -m display --focus east", "Focus display east", "display", "focus"),
            ("yabai --start-service", "Start yabai service", "service", "control"),
            ("yabai --stop-service", "Stop yabai service", "service", "control"),
            ("yabai --restart-service", "Restart yabai service", "service", "control"),
        ]

        for cmd, desc, context, tag in yabai_commands:
            shortcuts.append(
                Shortcut(
                    key="",  # yabai no tiene keys directos
                    description=desc,
                    app="yabai",
                    context=context,
                    tags=[tag],
                    raw_command=cmd,
                )
            )

        return shortcuts
