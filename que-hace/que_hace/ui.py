"""TUI para Que hace? con tema Catppuccin Mocha."""

import subprocess
from typing import List

from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import DataTable, Input, Label, Static

from .database import load_database
from .models import Shortcut, ShortcutsDatabase


# Catppuccin Mocha Colors
CATPPUCCIN = {
    "base": "#1e1e2e",
    "mantle": "#181825",
    "crust": "#11111b",
    "surface0": "#313244",
    "surface1": "#45475a",
    "surface2": "#585b70",
    "overlay0": "#6c7086",
    "overlay1": "#7f849c",
    "overlay2": "#9399b2",
    "text": "#cdd6f4",
    "subtext0": "#a6adc8",
    "subtext1": "#bac2de",
    "lavender": "#b4befe",
    "blue": "#89b4fa",
    "sapphire": "#74c7ec",
    "sky": "#89dceb",
    "teal": "#94e2d5",
    "green": "#a6e3a1",
    "yellow": "#f9e2af",
    "peach": "#fab387",
    "maroon": "#eba0ac",
    "red": "#f38ba8",
    "mauve": "#cba6f7",
    "pink": "#f5c2e7",
    "flamingo": "#f2cdcd",
    "rosewater": "#f5e0dc",
}


class ShortcutRow(Static):
    """Widget para mostrar un shortcut individual."""

    def __init__(self, shortcut: Shortcut, **kwargs):
        self.shortcut = shortcut
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        with Horizontal(classes="shortcut-row"):
            yield Label(
                f"[b {CATPPUCCIN['green']}]{self.shortcut.key}[/]",
                classes="key-col"
            )
            yield Label(
                f"[{CATPPUCCIN['text']}]{self.shortcut.description}[/]",
                classes="desc-col"
            )
            yield Label(
                f"[{CATPPUCCIN['mauve']}]{self.shortcut.app}[/]",
                classes="app-col"
            )
            yield Label(
                f"[{CATPPUCCIN['blue']}]{self.shortcut.context or '-'}[/]",
                classes="context-col"
            )


class QueHaceApp(App):
    """TUI principal del plugin Que hace?"""

    CSS = f"""
    Screen {{
        align: center middle;
        background: {CATPPUCCIN['base']};
    }}

    #main-container {{
        width: 95%;
        height: 95%;
        border: solid {CATPPUCCIN['mauve']};
        background: {CATPPUCCIN['mantle']};
    }}

    #header {{
        height: 3;
        background: {CATPPUCCIN['surface0']};
        color: {CATPPUCCIN['text']};
        content-align: center middle;
        text-style: bold;
    }}

    #search-container {{
        height: 3;
        padding: 0 1;
        background: {CATPPUCCIN['mantle']};
    }}

    #search-input {{
        width: 100%;
        background: {CATPPUCCIN['surface0']};
        color: {CATPPUCCIN['text']};
        border: solid {CATPPUCCIN['surface1']};
    }}

    #search-input:focus {{
        border: solid {CATPPUCCIN['mauve']};
    }}

    #content {{
        height: 1fr;
        padding: 0 1;
        background: {CATPPUCCIN['mantle']};
    }}

    #shortcuts-table {{
        height: 100%;
        background: {CATPPUCCIN['mantle']};
        color: {CATPPUCCIN['text']};
    }}

    #shortcuts-table:focus {{
        border: solid {CATPPUCCIN['mauve']};
    }}

    #footer {{
        height: 1;
        background: {CATPPUCCIN['surface0']};
        color: {CATPPUCCIN['subtext0']};
        content-align: center middle;
    }}

    .datatable--header {{
        background: {CATPPUCCIN['surface0']};
        color: {CATPPUCCIN['lavender']};
        text-style: bold;
    }}

    .datatable--header-hover {{
        background: {CATPPUCCIN['surface1']};
    }}

    .datatable--row {{
        background: {CATPPUCCIN['mantle']};
    }}

    .datatable--row-hover {{
        background: {CATPPUCCIN['surface0']};
    }}

    .datatable--row-cursor {{
        background: {CATPPUCCIN['surface1']};
    }}
    """

    BINDINGS = [
        Binding("q", "quit", "Salir"),
        Binding("escape", "quit", "Salir"),
        Binding("ctrl+c", "quit", "Salir"),
        Binding("?", "help", "Ayuda"),
        Binding("a", "filter_app", "Filtrar App"),
        Binding("c", "copy", "Copiar"),
        Binding("r", "refresh", "Refrescar"),
    ]

    database: reactive[ShortcutsDatabase | None] = reactive(None)
    current_filter: reactive[str] = reactive("")
    current_app_filter: reactive[str | None] = reactive(None)

    def __init__(self, database_path: str, **kwargs):
        self.database_path = database_path
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        with Vertical(id="main-container"):
            yield Static("  Que hace?    Central de Shortcuts", id="header")

            with Vertical(id="search-container"):
                yield Input(
                    placeholder="Buscar shortcut... (ej: 'split', 'focus', 'tmux')  |  ↑↓ navegar  |  Enter copiar  |  q salir",
                    id="search-input"
                )

            with Vertical(id="content"):
                table = DataTable(id="shortcuts-table", cursor_type="row")
                table.add_column("Key", width=25)
                table.add_column("Description", width=45)
                table.add_column("App", width=12)
                table.add_column("Context", width=15)
                yield table

            yield Static("[q] Salir  [a] Filtrar App  [c] Copiar  [r] Refrescar  [?] Ayuda", id="footer")

    def on_mount(self) -> None:
        """Carga inicial de datos."""
        self.load_database()
        self.update_table()
        self.query_one("#search-input", Input).focus()

    def load_database(self) -> None:
        """Carga la base de datos desde JSON."""
        try:
            self.database = load_database(self.database_path)
        except Exception:
            self.database = None

    def watch_current_filter(self) -> None:
        """Actualiza la tabla cuando cambia el filtro."""
        self.update_table()

    def watch_current_app_filter(self) -> None:
        """Actualiza la tabla cuando cambia el filtro de app."""
        self.update_table()

    def update_table(self) -> None:
        """Actualiza la tabla con los shortcuts filtrados."""
        table = self.query_one("#shortcuts-table", DataTable)
        table.clear()

        if not self.database:
            return

        shortcuts = self._get_filtered_shortcuts()

        # Ordenar por app y luego por key
        shortcuts.sort(key=lambda s: (s.app, s.key))

        for shortcut in shortcuts:
            table.add_row(
                Text(shortcut.key, style=f"bold {CATPPUCCIN['green']}"),
                Text(shortcut.description, style=CATPPUCCIN['text']),
                Text(shortcut.app, style=CATPPUCCIN['mauve']),
                Text(shortcut.context or "-", style=CATPPUCCIN['blue']),
            )

    def _get_filtered_shortcuts(self) -> List[Shortcut]:
        """Obtiene shortcuts filtrados por búsqueda y app."""
        if not self.database:
            return []

        # Filtrar por app primero
        if self.current_app_filter:
            shortcuts = self.database.get_shortcuts_by_app(self.current_app_filter)
        else:
            shortcuts = self.database.get_all_shortcuts()

        # Luego filtrar por búsqueda
        if self.current_filter:
            query = self.current_filter.lower()
            shortcuts = [
                s for s in shortcuts
                if (query in s.key.lower()
                    or query in s.description.lower()
                    or any(query in tag.lower() for tag in s.tags))
            ]

        return shortcuts

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handler para cambios en el input de búsqueda."""
        self.current_filter = event.value

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handler para selección de fila."""
        self._copy_selected_shortcut()

    def action_copy(self) -> None:
        """Copia el shortcut seleccionado al clipboard."""
        self._copy_selected_shortcut()

    def _copy_selected_shortcut(self) -> None:
        """Copia el shortcut seleccionado al clipboard."""
        table = self.query_one("#shortcuts-table", DataTable)
        if table.cursor_row is not None:
            shortcuts = self._get_filtered_shortcuts()
            if 0 <= table.cursor_row < len(shortcuts):
                shortcut = shortcuts[table.cursor_row]
                try:
                    subprocess.run(["pbcopy"], input=shortcut.key.encode())
                    self.notify(
                        f"Copiado: {shortcut.key}",
                        severity="information",
                        timeout=2
                    )
                except Exception:
                    self.notify("Error al copiar", severity="error")

    def action_filter_app(self) -> None:
        """Muestra selector de apps para filtrar."""
        if not self.database:
            return

        apps = list(self.database.apps.keys())
        if not apps:
            return

        # Simple cycling through apps
        if self.current_app_filter is None:
            self.current_app_filter = apps[0]
        else:
            try:
                current_idx = apps.index(self.current_app_filter)
                next_idx = (current_idx + 1) % (len(apps) + 1)
                if next_idx == len(apps):
                    self.current_app_filter = None  # All apps
                else:
                    self.current_app_filter = apps[next_idx]
            except ValueError:
                self.current_app_filter = apps[0]

        app_name = self.current_app_filter or "Todas"
        self.notify(f"Filtrando: {app_name}", severity="information", timeout=1)

    def action_refresh(self) -> None:
        """Recarga la base de datos."""
        self.load_database()
        self.update_table()
        self.notify("Base de datos actualizada", severity="information", timeout=1)

    def action_help(self) -> None:
        """Muestra ayuda."""
        help_text = """
        [b]Atajos de teclado:[/b]

        [b]q / Escape / Ctrl+C[/b]  Salir
        [b]↑ / ↓[/b]                  Navegar shortcuts
        [b]Enter[/b]                 Copiar shortcut
        [b]c[/b]                     Copiar shortcut
        [b]a[/b]                     Filtrar por app
        [b]r[/b]                     Refrescar datos
        [b]?[/b]                     Mostrar ayuda
        """
        self.notify(help_text, title="Ayuda", severity="information")

    def action_quit(self) -> None:
        """Salir de la aplicación."""
        self.exit()
