"""Modelos Pydantic para Que hace?"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class AppType(str, Enum):
    """Tipos de aplicativos soportados."""

    TMUX = "tmux"
    NVIM = "nvim"
    SHELL = "shell"
    TERMINAL = "terminal"
    WINDOW_MANAGER = "window_manager"
    HOTKEY_DAEMON = "hotkey_daemon"


class Shortcut(BaseModel):
    """Representa un atajo de teclado."""

    model_config = ConfigDict(extra="allow")

    key: str = Field(..., description="Combinación de teclas")
    description: str = Field(..., description="Qué hace el shortcut")
    app: str = Field(..., description="Aplicativo al que pertenece")
    context: Optional[str] = Field(None, description="Categoría/contexto")
    tags: List[str] = Field(default_factory=list)
    source_file: Optional[str] = None
    line_number: Optional[int] = None
    raw_command: Optional[str] = None


class AppConfig(BaseModel):
    """Configuración de un aplicativo."""

    model_config = ConfigDict(extra="allow")

    name: str
    display_name: str
    type: AppType
    config_files: List[str]
    enabled: bool = True
    shortcuts: List[Shortcut] = Field(default_factory=list)
    last_extracted: Optional[datetime] = None


class ShortcutsDatabase(BaseModel):
    """Base de datos centralizada de shortcuts."""

    model_config = ConfigDict(extra="allow")

    version: str = "1.0.0"
    last_updated: datetime = Field(default_factory=datetime.now)
    apps: Dict[str, AppConfig] = Field(default_factory=dict)

    def get_all_shortcuts(self) -> List[Shortcut]:
        """Retorna todos los shortcuts de todas las apps."""
        all_shortcuts: List[Shortcut] = []
        for app in self.apps.values():
            all_shortcuts.extend(app.shortcuts)
        return all_shortcuts

    def get_shortcuts_by_app(self, app_name: str) -> List[Shortcut]:
        """Retorna shortcuts de una app específica."""
        if app_name in self.apps:
            return self.apps[app_name].shortcuts
        return []

    def search_shortcuts(self, query: str) -> List[Shortcut]:
        """Búsqueda fuzzy en keys y descriptions."""
        query = query.lower()
        results: List[Shortcut] = []
        for shortcut in self.get_all_shortcuts():
            if (
                query in shortcut.key.lower()
                or query in shortcut.description.lower()
                or any(query in tag.lower() for tag in shortcut.tags)
            ):
                results.append(shortcut)
        return results

    def get_enabled_apps(self) -> Dict[str, AppConfig]:
        """Retorna solo las apps habilitadas."""
        return {name: app for name, app in self.apps.items() if app.enabled}
