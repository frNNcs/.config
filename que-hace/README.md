# Que hace?

Central de shortcuts para tu dotfiles. Una TUI moderna con tema Catppuccin Mocha que centraliza todos los atajos de teclado de tus aplicativos.

## Características

- **TUI Moderna**: Construida con Textual y tema Catppuccin Mocha
- **Multi-app**: Soporta tmux, skhd, nvim, yabai, ghostty y más
- **Búsqueda fuzzy**: Encuentra shortcuts rápidamente
- **Extracción inteligente**: Usa Ollama (servidor remoto) para parsear configuraciones
- **Base de datos centralizada**: Todo en un JSON versionable
- **Copia al clipboard**: Selecciona un shortcut y se copia automáticamente
- **Arquitectura extensible**: Fácil agregar nuevas apps

## Instalación

```bash
# Clonar el repositorio
git clone <repo> ~/.config/que-hace
cd ~/.config/que-hace

# Instalar dependencias
pip install -e .

# Inicializar base de datos
que-hace init

# Extraer shortcuts (requiere Ollama)
que-hace update
```

## Configuración de Ollama

Por defecto, el sistema busca Ollama en `192.168.1.80:11434`. Puedes configurar esto con variables de entorno:

```bash
export OLLAMA_HOST=192.168.1.80
export OLLAMA_PORT=11434
```

## Uso

### TUI Interactivo

```bash
# Abrir popup con todos los shortcuts
que-hace popup

# O desde tmux (ver configuración abajo)
```

### Comandos CLI

```bash
# Listar apps registradas
que-hace list-apps

# Ver shortcuts de una app específica
que-hace show tmux

# Buscar shortcuts
que-hace search split

# Actualizar desde archivos de configuración
que-hace update
que-hace update --app tmux  # Solo una app

# Añadir nueva app
que-hace add-app myapp "My App" nvim ~/.config/myapp/config

# Gestionar apps
que-hace enable tmux
que-hace disable yabai

# Ver configuración
que-hace config
```

## Integración con Tmux

### Opción 1: Añadir a tmux.conf

```bash
# Añadir a ~/.config/tmux/tmux.conf
bind-key ? run-shell "cd ~/.config/que-hace && python3 -m que_hace popup"
```

### Opción 2: Usar el script de configuración

```bash
chmod +x ~/.config/que-hace/que-hace.tmux
~/.config/que-hace/que-hace.tmux
```

Luego en tmux:
```
Prefix + ?  # Abre el popup de Que hace?
```

## Atajos de la TUI

| Tecla | Acción |
|-------|--------|
| `↑/↓` | Navegar shortcuts |
| `Enter` o `c` | Copiar shortcut al clipboard |
| `a` | Filtrar por app (cicla entre apps) |
| `r` | Refrescar base de datos |
| `?` | Mostrar ayuda |
| `q` o `Esc` o `Ctrl+C` | Salir |

## Estructura del Proyecto

```
que-hace/
├── que_hace/
│   ├── __init__.py
│   ├── __main__.py          # Entry point
│   ├── models.py            # Pydantic models
│   ├── database.py          # JSON storage
│   ├── ui.py                # TUI con Textual
│   ├── cli.py               # CLI con typer
│   ├── ollama_client.py     # Cliente Ollama remoto
│   └── extractors/          # Extractores de shortcuts
│       ├── __init__.py
│       ├── base.py          # Base extractor
│       ├── tmux.py          # Tmux extractor
│       ├── skhd.py          # SKHD extractor
│       ├── nvim.py          # Neovim extractor
│       └── yabai.py         # Yabai extractor
├── data/
│   └── shortcuts.json       # Base de datos centralizada
├── pyproject.toml
├── que-hace.tmux            # Script de integración tmux
└── README.md
```

## Agregar Nuevas Apps

1. Crear un nuevo extractor en `que_hace/extractors/`:

```python
from .base import BaseExtractor
from ..models import Shortcut

class MyAppExtractor(BaseExtractor):
    async def extract(self) -> list[Shortcut]:
        # Tu lógica de extracción aquí
        pass
```

2. Registrar el extractor en `que_hace/extractors/__init__.py`:

```python
from .myapp import MyAppExtractor

EXTRACTOR_REGISTRY["myapp"] = MyAppExtractor
```

3. Añadir la app a la base de datos:

```bash
que-hace add-app myapp "My App" terminal ~/.config/myapp/config
```

4. Extraer shortcuts:

```bash
que-hace update --app myapp
```

## Desarrollo

```bash
# Instalar en modo desarrollo
pip install -e ".[dev]"

# Ejecutar tests
pytest

# Linting
ruff check .
mypy que_hace/
```

## Licencia

MIT
