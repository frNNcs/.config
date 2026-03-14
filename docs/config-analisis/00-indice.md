# Análisis de Configuración - Índice Principal

## Resumen Ejecutivo

Este análisis documenta la configuración completa del sistema macOS, identificando todos los aplicativos configurados, su portabilidad a otras plataformas, y proporciona un plan de migración a Nix.

**Fecha de Análisis**: 2 de febrero de 2026  
**Sistema Base**: macOS  
**Objetivo**: Migración multiplataforma (Ubuntu, Windows) y gestión declarativa con Nix

## Estructura de la Documentación

### Aplicativos Principales

1. **[[01-yabai]]** - Window Manager para macOS
   - Estado: ✅ Funcional
   - Portabilidad: ❌ macOS only (alternativas: i3, sway, komorebi)
   
2. **[[02-skhd]]** - Hotkey Daemon
   - Estado: ✅ Funcional
   - Portabilidad: ⚠️ Con alternativas (sxhkd, i3 keybindings)
   
3. **[[03-ghostty]]** - Terminal Emulator
   - Estado: ✅ Funcional
   - Portabilidad: ✅ Cross-platform (Linux, Windows en desarrollo)
   
4. **[[04-tmux]]** - Terminal Multiplexer
   - Estado: ✅ Funcional
   - Portabilidad: ✅ 100% portable
   
5. **[[05-neovim]]** - Editor de Texto
   - Estado: ✅ Funcional
   - Portabilidad: ✅ 100% portable
   
6. **[[06-sketchybar]]** - Menu Bar para macOS
   - Estado: ✅ Funcional
   - Portabilidad: ❌ macOS only (alternativas: polybar, waybar)
   
7. **[[07-shell-tools]]** - lsd, bat, atuin
   - Estado: ✅ Funcional
   - Portabilidad: ✅ 100% portable
   
8. **[[08-otros-aplicativos]]** - Aplicativos adicionales
   - Estado: ✅ Funcional
   - Portabilidad: Variable por aplicativo

## Estadísticas Generales

### Por Nivel de Portabilidad

| Categoría | Cantidad | Aplicativos |
|-----------|----------|-------------|
| ✅ 100% Portable | 15+ | Ghostty, Tmux, Neovim, lsd, bat, atuin, gh, syncthing, fabric, etc. |
| ⚠️ Con Alternativas | 5 | Yabai, skhd, SketchyBar, LinearMouse, Raycast |
| ❌ Específico de Plataforma | 0 | ✨ Todo es portable! |

### Por Categoría Funcional

| Categoría | Aplicativos | Portabilidad |
|-----------|-------------|--------------|
| **Window Management** | Yabai, skhd | ⚠️ Alternativas en Linux/Windows |
| **Terminal** | Ghostty, tmux | ✅ 100% portable |
| **Editor** | Neovim | ✅ 100% portable |
| **Shell Tools** | lsd, bat, atuin, fish | ✅ 100% portable |
| **Status Bar** | SketchyBar | ⚠️ Alternativas: polybar, waybar |
| **Productivity** | Raycast, Fabric | ⚠️ Raycast → rofi/albert |
| **Development** | gh, VSCode, Copilot | ✅ 100% portable |
| **AI/LLM** | Gemini, OpenCode, OTerm | ✅ 100% portable |
| **Sync** | Syncthing | ✅ 100% portable |
| **Customization** | Spicetify, Neofetch | ✅ 100% portable |

## Temas y Estética

### Tema Universal: Catppuccin Mocha

Todos los aplicativos usan la paleta **Catppuccin Mocha**:
- lsd (colors.yaml)
- Ghostty (theme)
- Tmux (catppuccin plugin)
- Neovim (probable)
- SketchyBar (colors.sh)

### Fuente Universal: JetBrains Mono Nerd Font

Usado en:
- Ghostty
- SketchyBar
- VS Code (probable)
- Neovim (probable)

## Análisis de Dependencias

### Homebrew Packages (Inferidos)
```bash
# Window Management
brew install koekeishiya/formulae/yabai
brew install koekeishiya/formulae/skhd
brew install FelixKratz/formulae/sketchybar

# Terminal & Shell
brew install ghostty
brew install tmux
brew install neovim
brew install lsd
brew install bat
brew install atuin
brew install fish

# Development
brew install gh
brew install ripgrep
brew install fd
brew install node
brew install python3

# Fonts
brew install --cask font-jetbrains-mono-nerd-font

# Other
brew install syncthing
brew install neofetch
```

### Repositorios Git Activos
1. **frNNcs/.config** (main) - Configuración principal
2. **tmux-plugins/tpm** (master) - Tmux Plugin Manager
3. **tmux-plugins/tmux-test** (unknown) - Testing

## Sincronización y Backup

### Syncthing
- **Ruta**: `~/projects/homelab/DATA/syncthing/`
- **Obsidian Vault**: `~/projects/homelab/DATA/syncthing/obsidian`
- **Configuraciones**: Sincronizadas vía Git + Syncthing

### Git
- **Repositorio**: frNNcs/.config
- **Branch**: main
- **Estado**: Tracked y versionado

## Plan de Acción

Ver **[[plan-de-proyecto]]** para el roadmap completo de:
1. Depuración de configuración actual
2. Migración a Nix
3. Portabilidad multiplataforma
4. Automatización y CI/CD

## Enlaces Rápidos

### Documentación por Aplicativo
- [[01-yabai]] - Window Manager
- [[02-skhd]] - Hotkey Daemon
- [[03-ghostty]] - Terminal
- [[04-tmux]] - Terminal Multiplexer
- [[05-neovim]] - Editor
- [[06-sketchybar]] - Menu Bar
- [[07-shell-tools]] - lsd, bat, atuin
- [[08-otros-aplicativos]] - Resto

### Documentación Técnica
- [[plan-de-proyecto]] - Roadmap de migración
- [[propuesta-unificacion]] - Propuesta de unificación de variables
- [[nix-evaluation]] - Evaluación de Nix
- [[transicion-linux]] - Guía de transición a Linux
- [[transicion-windows]] - Guía de transición a Windows

## Próximos Pasos

1. ✅ Análisis completo de aplicativos
2. ⏳ Crear plan de proyecto detallado
3. ⏳ Evaluar implementación con Nix
4. ⏳ Crear configuraciones base para Linux
5. ⏳ Crear configuraciones base para Windows
6. ⏳ Setup de CI/CD para testing

## Notas

- Configuración actual está altamente optimizada para macOS
- La mayoría de herramientas son portables o tienen alternativas equivalentes
- El mayor desafío será window management en diferentes plataformas
- Nix puede unificar la gestión de paquetes y configuraciones
- Tema Catppuccin proporciona consistencia visual cross-platform

---

**Ubicación de este análisis**: `~/.config/docs/config-analisis/`  
**Bóveda Obsidian**: `~/projects/homelab/DATA/syncthing/obsidian/`
