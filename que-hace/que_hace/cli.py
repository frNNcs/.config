"""CLI para Que hace?"""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from .database import load_database, save_database
from .extractors import EXTRACTOR_REGISTRY, get_extractor
from .models import AppConfig, AppType, ShortcutsDatabase
from .ui import QueHaceApp

app = typer.Typer(
    name="que-hace",
    help="Central de shortcuts para tu dotfiles",
    no_args_is_help=True,
)
console = Console()

DEFAULT_DB_PATH = "~/.config/que-hace/data/shortcuts.json"


def get_version() -> str:
    """Obtiene la versión del paquete."""
    return "0.1.0"


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", is_eager=True, help="Muestra la versión"
    ),
):
    """Que hace? - Central de shortcuts."""
    if version:
        typer.echo(f"que-hace version {get_version()}")
        raise typer.Exit()


@app.command()
def popup(
    db_path: str = typer.Option(DEFAULT_DB_PATH, "--db", "-d", help="Ruta a la base de datos"),
):
    """Abre el popup interactivo de shortcuts."""
    QueHaceApp(database_path=db_path).run()


@app.command()
def list_apps(
    db_path: str = typer.Option(DEFAULT_DB_PATH, "--db", "-d"),
    enabled_only: bool = typer.Option(False, "--enabled", "-e", help="Solo apps habilitadas"),
):
    """Lista todas las aplicaciones registradas."""
    try:
        database = load_database(db_path)
    except Exception as e:
        console.print(f"[red]Error cargando base de datos: {e}[/red]")
        raise typer.Exit(1)

    if not database.apps:
        console.print("[yellow]No hay aplicaciones registradas. Ejecuta 'que-hace init' primero.[/yellow]")
        return

    table = Table(title="Aplicativos Configurados")
    table.add_column("App", style="cyan", no_wrap=True)
    table.add_column("Tipo", style="green")
    table.add_column("Estado", style="yellow")
    table.add_column("Shortcuts", style="blue", justify="right")
    table.add_column("Última actualización", style="magenta")

    for name, app_config in sorted(database.apps.items()):
        if enabled_only and not app_config.enabled:
            continue

        status = "[green]✓[/green]" if app_config.enabled else "[red]✗[/red]"
        last_updated = (
            app_config.last_extracted.strftime("%Y-%m-%d %H:%M")
            if app_config.last_extracted
            else "Nunca"
        )

        table.add_row(
            app_config.display_name,
            app_config.type.value,
            status,
            str(len(app_config.shortcuts)),
            last_updated,
        )

    console.print(table)


@app.command()
def show(
    app_name: str = typer.Argument(..., help="Nombre de la app (tmux, nvim, skhd, yabai)"),
    db_path: str = typer.Option(DEFAULT_DB_PATH, "--db", "-d"),
):
    """Muestra shortcuts de una app específica."""
    try:
        database = load_database(db_path)
    except Exception as e:
        console.print(f"[red]Error cargando base de datos: {e}[/red]")
        raise typer.Exit(1)

    if app_name not in database.apps:
        available = ", ".join(sorted(database.apps.keys()))
        console.print(f"[red]App '{app_name}' no encontrada[/red]")
        console.print(f"[yellow]Apps disponibles: {available}[/yellow]")
        raise typer.Exit(1)

    app_config = database.apps[app_name]

    if not app_config.shortcuts:
        console.print(f"[yellow]No hay shortcuts para {app_config.display_name}[/yellow]")
        console.print(f"[yellow]Ejecuta 'que-hace update --app {app_name}' para extraerlos.[/yellow]")
        return

    table = Table(title=f"Shortcuts: {app_config.display_name}")
    table.add_column("Key", style="green", no_wrap=True)
    table.add_column("Descripción", style="white")
    table.add_column("Contexto", style="blue")
    table.add_column("Tags", style="magenta")

    for shortcut in sorted(app_config.shortcuts, key=lambda s: s.context or ""):
        tags = ", ".join(shortcut.tags) if shortcut.tags else "-"
        table.add_row(
            shortcut.key,
            shortcut.description,
            shortcut.context or "-",
            tags,
        )

    console.print(table)


@app.command()
def search(
    query: str = typer.Argument(..., help="Término de búsqueda"),
    db_path: str = typer.Option(DEFAULT_DB_PATH, "--db", "-d"),
    app: Optional[str] = typer.Option(None, "--app", "-a", help="Buscar solo en esta app"),
):
    """Busca shortcuts por key o descripción."""
    try:
        database = load_database(db_path)
    except Exception as e:
        console.print(f"[red]Error cargando base de datos: {e}[/red]")
        raise typer.Exit(1)

    if app:
        shortcuts = database.get_shortcuts_by_app(app)
        query_lower = query.lower()
        results = [
            s for s in shortcuts
            if (query_lower in s.key.lower()
                or query_lower in s.description.lower()
                or any(query_lower in tag.lower() for tag in s.tags))
        ]
    else:
        results = database.search_shortcuts(query)

    if not results:
        console.print(f"[yellow]No se encontraron resultados para '{query}'[/yellow]")
        return

    table = Table(title=f"Resultados: '{query}' ({len(results)} encontrados)")
    table.add_column("App", style="cyan", no_wrap=True)
    table.add_column("Key", style="green", no_wrap=True)
    table.add_column("Descripción", style="white")
    table.add_column("Contexto", style="blue")

    for shortcut in results:
        table.add_row(
            shortcut.app,
            shortcut.key,
            shortcut.description,
            shortcut.context or "-",
        )

    console.print(table)


@app.command()
def update(
    app: Optional[str] = typer.Option(None, "--app", "-a", help="Actualizar solo esta app"),
    db_path: str = typer.Option(DEFAULT_DB_PATH, "--db", "-d"),
    use_ollama: bool = typer.Option(True, "--ollama/--no-ollama", help="Usar Ollama para extracción"),
):
    """Extrae y actualiza shortcuts de los archivos de configuración."""

    async def do_update():
        try:
            database = load_database(db_path)
        except Exception as e:
            console.print(f"[red]Error cargando base de datos: {e}[/red]")
            raise typer.Exit(1)

        # Determinar qué apps actualizar
        apps_to_update = [app] if app else list(database.apps.keys())

        with console.status("[bold green]Extrayendo shortcuts...") as status:
            for app_name in apps_to_update:
                if app_name not in database.apps:
                    console.print(f"[yellow]App '{app_name}' no encontrada en la base de datos[/yellow]")
                    continue

                app_config = database.apps[app_name]

                if not app_config.enabled:
                    console.print(f"[yellow]Ignorando {app_name} (deshabilitada)[/yellow]")
                    continue

                status.update(f"[bold green]Extrayendo {app_name}...")

                extractor = get_extractor(app_name, app_config.config_files)
                if not extractor:
                    console.print(f"[yellow]No hay extractor para '{app_name}'[/yellow]")
                    continue

                try:
                    shortcuts = await extractor.extract()

                    database.apps[app_name].shortcuts = shortcuts
                    database.apps[app_name].last_extracted = datetime.now()

                    console.print(f"[green]✓ {len(shortcuts)} shortcuts extraídos de {app_name}[/green]")

                except Exception as e:
                    console.print(f"[red]✗ Error extrayendo {app_name}: {e}[/red]")

        # Guardar base de datos
        try:
            save_database(database, db_path)
            console.print(f"\n[bold green]✓ Base de datos guardada en {db_path}[/bold green]")
        except Exception as e:
            console.print(f"[red]Error guardando base de datos: {e}[/red]")
            raise typer.Exit(1)

    asyncio.run(do_update())


@app.command()
def init(
    db_path: str = typer.Option(DEFAULT_DB_PATH, "--db", "-d"),
    force: bool = typer.Option(False, "--force", "-f", help="Sobrescribir si existe"),
):
    """Inicializa la base de datos con configuración por defecto."""
    path = Path(db_path).expanduser()

    if path.exists() and not force:
        console.print(f"[yellow]La base de datos ya existe en {db_path}[/yellow]")
        console.print("[yellow]Usa --force para sobrescribir[/yellow]")
        raise typer.Exit(1)

    database = ShortcutsDatabase(
        last_updated=datetime.now(),
        apps={
            "tmux": AppConfig(
                name="tmux",
                display_name="Tmux",
                type=AppType.TMUX,
                config_files=["~/.config/tmux/tmux.conf"],
                enabled=True,
            ),
            "skhd": AppConfig(
                name="skhd",
                display_name="SKHD",
                type=AppType.HOTKEY_DAEMON,
                config_files=["~/.config/skhd/skhdrc"],
                enabled=True,
            ),
            "nvim": AppConfig(
                name="nvim",
                display_name="Neovim",
                type=AppType.NVIM,
                config_files=["~/.config/nvim/init.lua", "~/.config/nvim/lua/plugins/"],
                enabled=True,
            ),
            "yabai": AppConfig(
                name="yabai",
                display_name="Yabai",
                type=AppType.WINDOW_MANAGER,
                config_files=["~/.config/yabai/yabairc"],
                enabled=True,
            ),
            "ghostty": AppConfig(
                name="ghostty",
                display_name="Ghostty",
                type=AppType.TERMINAL,
                config_files=["~/.config/ghostty/config"],
                enabled=True,
            ),
        }
    )

    # Crear directorio si no existe
    path.parent.mkdir(parents=True, exist_ok=True)

    save_database(database, db_path)
    console.print(Panel(
        f"[bold green]✓ Base de datos inicializada[/bold green]\n\n"
        f"Ubicación: [cyan]{db_path}[/cyan]\n"
        f"Apps registradas: [yellow]{len(database.apps)}[/yellow]\n\n"
        f"[dim]Próximos pasos:[/dim]\n"
        f"1. [bold]que-hace update[/bold] - Extraer shortcuts\n"
        f"2. [bold]que-hace popup[/bold] - Ver TUI interactivo\n"
        f"3. Configurar tmux: [bold]que-hace tmux-setup[/bold]",
        title="Que hace?",
        border_style="green"
    ))


@app.command()
def tmux_setup(
    db_path: str = typer.Option(DEFAULT_DB_PATH, "--db", "-d"),
):
    """Muestra instrucciones para configurar la integración con tmux."""
    setup_script = Path(__file__).parent / "que-hace.tmux"

    instructions = f"""
    [bold cyan]Configuración de Que hace? para Tmux[/bold cyan]

    [bold]Opción 1: Añadir a tmux.conf manualmente[/bold]
    
    Abre tu tmux.conf y añade:
    
    [green]
    # Que hace? - Central de shortcuts
    bind-key ? run-shell "cd ~/.config/que-hace && python -m que_hace popup"
    [/green]

    [bold]Opción 2: Usar el script de configuración[/bold]
    
    [green]
    chmod +x {setup_script}
    {setup_script}
    [/green]

    [bold]Opción 3: Añadir a TPM (Tmux Plugin Manager)[/bold]
    
    Añade a tu lista de plugins en tmux.conf:
    [green]
    set -g @plugin 'que-hace'
    [/green]

    [bold yellow]Nota:[/bold yellow] Asegúrate de haber instalado las dependencias:
    [green]
    cd ~/.config/que-hace
    pip install -e .
    [/green]
    """

    console.print(Panel(instructions, title="Setup Tmux", border_style="blue"))


@app.command()
def config(
    db_path: str = typer.Option(DEFAULT_DB_PATH, "--db", "-d"),
):
    """Muestra la configuración actual."""
    try:
        database = load_database(db_path)
    except Exception as e:
        console.print(f"[red]Error cargando base de datos: {e}[/red]")
        raise typer.Exit(1)

    # Info general
    console.print(Panel(
        f"Versión: [cyan]{database.version}[/cyan]\n"
        f"Última actualización: [cyan]{database.last_updated.strftime('%Y-%m-%d %H:%M:%S')}[/cyan]\n"
        f"Total apps: [cyan]{len(database.apps)}[/cyan]\n"
        f"Total shortcuts: [cyan]{len(database.get_all_shortcuts())}[/cyan]",
        title="Configuración",
        border_style="green"
    ))

    # Info por app
    for name, app_config in sorted(database.apps.items()):
        status = "[green]✓ Habilitada[/green]" if app_config.enabled else "[red]✗ Deshabilitada[/red]"
        shortcuts_count = len(app_config.shortcuts)

        console.print(f"\n[bold]{app_config.display_name}[/bold] ({name})")
        console.print(f"  Estado: {status}")
        console.print(f"  Tipo: [blue]{app_config.type.value}[/blue]")
        console.print(f"  Shortcuts: [yellow]{shortcuts_count}[/yellow]")
        console.print("  Archivos:")
        for cfg_file in app_config.config_files:
            console.print(f"    [dim]- {cfg_file}[/dim]")


@app.command()
def add_app(
    name: str = typer.Argument(..., help="Nombre interno de la app"),
    display_name: str = typer.Argument(..., help="Nombre para mostrar"),
    app_type: AppType = typer.Argument(..., help="Tipo de aplicativo"),
    config_files: list[str] = typer.Argument(..., help="Archivos de configuración (separados por espacio)"),
    db_path: str = typer.Option(DEFAULT_DB_PATH, "--db", "-d"),
):
    """Añade una nueva app a la base de datos."""
    try:
        database = load_database(db_path)
    except Exception as e:
        console.print(f"[red]Error cargando base de datos: {e}[/red]")
        raise typer.Exit(1)

    if name in database.apps:
        console.print(f"[red]La app '{name}' ya existe[/red]")
        raise typer.Exit(1)

    database.apps[name] = AppConfig(
        name=name,
        display_name=display_name,
        type=app_type,
        config_files=config_files,
        enabled=True,
    )

    save_database(database, db_path)
    console.print(f"[green]✓ App '{name}' añadida correctamente[/green]")
    console.print(f"[yellow]Ahora ejecuta 'que-hace update --app {name}' para extraer shortcuts[/yellow]")


@app.command()
def remove_app(
    name: str = typer.Argument(..., help="Nombre de la app a eliminar"),
    db_path: str = typer.Option(DEFAULT_DB_PATH, "--db", "-d"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Confirmar sin preguntar"),
):
    """Elimina una app de la base de datos."""
    try:
        database = load_database(db_path)
    except Exception as e:
        console.print(f"[red]Error cargando base de datos: {e}[/red]")
        raise typer.Exit(1)

    if name not in database.apps:
        console.print(f"[red]La app '{name}' no existe[/red]")
        raise typer.Exit(1)

    app_config = database.apps[name]

    if not yes:
        confirm = typer.confirm(f"¿Eliminar '{app_config.display_name}' y todos sus shortcuts?")
        if not confirm:
            console.print("[yellow]Operación cancelada[/yellow]")
            raise typer.Exit(0)

    del database.apps[name]
    save_database(database, db_path)
    console.print(f"[green]✓ App '{name}' eliminada[/green]")


@app.command()
def enable(
    name: str = typer.Argument(..., help="Nombre de la app"),
    db_path: str = typer.Option(DEFAULT_DB_PATH, "--db", "-d"),
):
    """Habilita una app."""
    _toggle_app(name, True, db_path)


@app.command()
def disable(
    name: str = typer.Argument(..., help="Nombre de la app"),
    db_path: str = typer.Option(DEFAULT_DB_PATH, "--db", "-d"),
):
    """Deshabilita una app."""
    _toggle_app(name, False, db_path)


def _toggle_app(name: str, enabled: bool, db_path: str):
    """Activa o desactiva una app."""
    try:
        database = load_database(db_path)
    except Exception as e:
        console.print(f"[red]Error cargando base de datos: {e}[/red]")
        raise typer.Exit(1)

    if name not in database.apps:
        console.print(f"[red]La app '{name}' no existe[/red]")
        raise typer.Exit(1)

    database.apps[name].enabled = enabled
    save_database(database, db_path)

    status = "habilitada" if enabled else "deshabilitada"
    console.print(f"[green]✓ App '{name}' {status}[/green]")


if __name__ == "__main__":
    app()
