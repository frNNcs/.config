# Tmux - Terminal Multiplexer

## Descripción General
Tmux es un multiplexor de terminal que permite ejecutar múltiples sesiones, ventanas y paneles dentro de una sola terminal.

## Estado Actual
- **Ubicación**: `~/.config/tmux/`
- **Archivo Principal**: `tmux.conf`
- **Plugins**: `~/.config/tmux/plugins/`
- **Estado**: ✅ Configurado y funcional

## Configuración Actual

### General
```bash
default-terminal: "tmux-256color"
terminal-overrides: ",xterm-256color:RGB"  # True color support
mouse: on
base-index: 1
pane-base-index: 1
renumber-windows: on
status-position: bottom
```

### Prefix Key
```bash
Prefix: Ctrl-Space  (unbind Ctrl-b)
```

### Keybindings de Navegación
```bash
Prefix + |    # Split horizontal (mantiene directorio actual)
Prefix + -    # Split vertical (mantiene directorio actual)
Prefix + h    # Select pane left
Prefix + j    # Select pane down
Prefix + k    # Select pane up
Prefix + l    # Select pane right
```

### Tema Catppuccin
```bash
@catppuccin_flavor: 'mocha'
@catppuccin_window_status_style: "rounded"
@catppuccin_window_text: " #W"
@catppuccin_window_current_text: " #W"
```

### Status Bar
```bash
# Left
status-left: "#{E:@catppuccin_status_session} #{E:@catppuccin_status_directory}"

# Right
status-right: "#{E:@catppuccin_status_user} #{E:@catppuccin_status_application} #{E:@catppuccin_status_uptime}"
```

### Soporte de Imágenes (Neovim)
```bash
allow-passthrough: on
update-environment: TERM TERM_PROGRAM
```

## Plugins Instalados (TPM)
```bash
1. tmux-plugins/tpm              # TPM manager
2. tmux-plugins/tmux-cpu         # CPU status
3. tmux-plugins/tmux-battery     # Battery status
4. catppuccin/tmux               # Catppuccin theme
```

### Instalación de Plugins
```bash
Prefix + I    # Install plugins
Prefix + U    # Update plugins
Prefix + alt + u    # Uninstall plugins
```

## Integración con Otros Aplicativos
- **Ghostty**: Compatible con image passthrough
- **Neovim**: Soporta imágenes dentro de tmux
- **zsh/fish**: Shell principal dentro de tmux
- **Catppuccin**: Tema consistente con otros apps

## Dependencias
```bash
# Instalación
brew install tmux

# TPM (Plugin Manager)
git clone https://github.com/tmux-plugins/tpm ~/.config/tmux/plugins/tpm
```

## Portabilidad

### ✅ Portabilidad a Linux
- **100% Compatible**: Misma configuración funciona en Linux
- Sin cambios necesarios
- Solo verificar paths de plugins

### ✅ Portabilidad a Windows
- **WSL**: Funciona perfectamente en WSL1/WSL2
- **Git Bash / Cygwin**: Compatible con adaptaciones
- **PowerShell**: No directamente compatible
- **Alternativa**: Usar dentro de WSL

## Recomendaciones

### Para Multiplataforma
1. **Configuración única**: Tmux es altamente portable
2. **Paths relativos**: Usar `~/.config/tmux` funciona en todas las plataformas Unix
3. **Plugins via TPM**: Sistema de plugins universal

### Para Nix
```nix
{
  programs.tmux = {
    enable = true;
    terminal = "tmux-256color";
    prefix = "C-Space";
    baseIndex = 1;
    mouse = true;
    
    plugins = with pkgs.tmuxPlugins; [
      {
        plugin = catppuccin;
        extraConfig = ''
          set -g @catppuccin_flavor 'mocha'
          set -g @catppuccin_window_status_style "rounded"
        '';
      }
      cpu
      battery
    ];
    
    extraConfig = ''
      set -ag terminal-overrides ",xterm-256color:RGB"
      set -g renumber-windows on
      
      # Keybindings
      bind | split-window -h -c "#{pane_current_path}"
      bind - split-window -v -c "#{pane_current_path}"
      bind h select-pane -L
      bind j select-pane -D
      bind k select-pane -U
      bind l select-pane -R
      
      # Image support
      set -g allow-passthrough on
      set -ga update-environment TERM
      set -ga update-environment TERM_PROGRAM
    '';
  };
}
```

## Listado de Transición

### Configuración Universal (Sin cambios entre OS)
| Opción | macOS | Linux | Windows (WSL) | Notas |
|--------|-------|-------|---------------|-------|
| `prefix` | ✅ | ✅ | ✅ | Universal |
| `mouse` | ✅ | ✅ | ✅ | Universal |
| `base-index` | ✅ | ✅ | ✅ | Universal |
| Keybindings | ✅ | ✅ | ✅ | Universal |
| TPM Plugins | ✅ | ✅ | ✅ | Universal |
| True Color | ✅ | ✅ | ⚠️ | Depende del terminal en Windows |

### Comandos Esenciales
```bash
# Sesiones
tmux                    # Nueva sesión
tmux new -s name        # Nueva sesión con nombre
tmux ls                 # Listar sesiones
tmux attach -t name     # Attachar a sesión
Prefix + d              # Detach de sesión

# Ventanas
Prefix + c              # Nueva ventana
Prefix + ,              # Renombrar ventana
Prefix + n              # Siguiente ventana
Prefix + p              # Ventana anterior
Prefix + 0-9            # Ir a ventana N

# Paneles
Prefix + |              # Split horizontal
Prefix + -              # Split vertical
Prefix + h/j/k/l        # Navegar paneles
Prefix + x              # Cerrar panel
Prefix + z              # Zoom panel

# Plugins
Prefix + I              # Instalar plugins
Prefix + U              # Actualizar plugins
```

## Features Destacables
1. **Persistencia de Sesiones**: Las sesiones sobreviven desconexiones
2. **Multiplexing**: Múltiples ventanas y paneles
3. **Scrollback**: Buffer de scroll infinito
4. **Copy Mode**: Modo de copia con navegación vim
5. **Status Bar Customizable**: Información del sistema
6. **Plugin System**: Extensible via TPM

## Estructura de Directorios
```
~/.config/tmux/
├── tmux.conf           # Configuración principal
└── plugins/
    ├── tpm/            # Plugin manager
    ├── tmux-cpu/       # CPU plugin
    ├── tmux-battery/   # Battery plugin
    └── catppuccin/     # Theme plugin
```

## Integración con Workflow
1. **Session Management**: Múltiples proyectos en sesiones separadas
2. **Window per Task**: Ventanas para diferentes tareas
3. **Panel Layouts**: Layouts predefinidos para workflows comunes
4. **Status Info**: CPU, battery, time en status bar

## Scripts de Automatización Potenciales

### Session Manager
```bash
#!/bin/bash
# tmux-session-manager.sh
session_name="$1"
if tmux has-session -t $session_name 2>/dev/null; then
    tmux attach -t $session_name
else
    tmux new -s $session_name
fi
```

### Layout Presets
```bash
# Desarrollo: Editor + Terminal + Logs
tmux split-window -h -p 30
tmux split-window -v -p 50
tmux select-pane -t 0
```

## Estado de Sincronización
- **Repositorio Git**: frNNcs/.config (branch: main)
- **Syncthing**: Posiblemente sincronizado
- **TPM Plugins**: Gestionados via TPM (requieren instalación en cada máquina)
