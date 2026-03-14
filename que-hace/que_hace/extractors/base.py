"""Extractores base para diferentes tipos de configuraciones."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from ..models import Shortcut


class BaseExtractor(ABC):
    """Clase base para extractores de shortcuts."""

    def __init__(self, app_name: str, config_files: List[str]):
        self.app_name = app_name
        self.config_files = config_files

    @abstractmethod
    async def extract(self) -> List[Shortcut]:
        """Extrae shortcuts de los archivos de configuración.

        Returns:
            Lista de shortcuts extraídos
        """
        pass

    def read_config_files(self) -> str:
        """Lee el contenido de todos los archivos de configuración.

        Returns:
            Contenido concatenado de todos los archivos
        """
        content: List[str] = []

        for file_path in self.config_files:
            path = Path(file_path).expanduser()

            if path.is_dir():
                # Leer todos los archivos del directorio
                for file in path.rglob("*"):
                    if file.is_file():
                        try:
                            content.append(f"=== {file} ===\n")
                            content.append(file.read_text(encoding="utf-8"))
                            content.append("\n")
                        except Exception:
                            continue
            elif path.exists():
                try:
                    content.append(f"=== {file_path} ===\n")
                    content.append(path.read_text(encoding="utf-8"))
                    content.append("\n")
                except Exception:
                    continue

        return "\n".join(content)

    def read_single_file(self, file_path: str) -> str:
        """Lee un único archivo de configuración.

        Args:
            file_path: Ruta al archivo

        Returns:
            Contenido del archivo o string vacío si no existe
        """
        path = Path(file_path).expanduser()
        if path.exists():
            try:
                return path.read_text(encoding="utf-8")
            except Exception:
                return ""
        return ""
