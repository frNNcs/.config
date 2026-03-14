"""Extractores de shortcuts para diferentes aplicativos."""

from .base import BaseExtractor
from .nvim import NvimExtractor
from .opencode import OpencodeExtractor
from .skhd import SkhdExtractor
from .tmux import TmuxExtractor
from .yabai import YabaiExtractor

__all__ = [
    "BaseExtractor",
    "TmuxExtractor",
    "SkhdExtractor",
    "NvimExtractor",
    "YabaiExtractor",
    "OpencodeExtractor",
]

# Registry de extractores disponibles
EXTRACTOR_REGISTRY = {
    "tmux": TmuxExtractor,
    "skhd": SkhdExtractor,
    "nvim": NvimExtractor,
    "yabai": YabaiExtractor,
    "opencode": OpencodeExtractor,
}


def get_extractor(app_name: str, config_files: list[str]):
    """Obtiene una instancia de extractor para una app.

    Args:
        app_name: Nombre de la aplicación
        config_files: Lista de archivos de configuración

    Returns:
        Instancia del extractor o None si no existe
    """
    extractor_class = EXTRACTOR_REGISTRY.get(app_name)
    if extractor_class:
        return extractor_class(config_files)
    return None


def register_extractor(name: str, extractor_class: type[BaseExtractor]) -> None:
    """Registra un nuevo extractor.

    Args:
        name: Nombre del extractor
        extractor_class: Clase del extractor
    """
    EXTRACTOR_REGISTRY[name] = extractor_class
