# skhd - Simple Hotkey Daemon

## Descripción General
skhd es un daemon de atajos de teclado para macOS que permite definir keybindings del sistema de manera declarativa.

## Estado Actual
- **Ubicación**: `~/.config/skhd/`
- **Archivo Principal**: `skhdrc`
- **Estado**: ✅ Configurado y funcional

## Atajos Configurados

### Navegación de Ventanas
```bash
# Focus en ventanas (vim-style)
alt - h/j/k/l          # Focus west/south/north/east

# Focus entre displays
alt - s                # Focus display west
alt - g                # Focus display east
```

### Modificación de Layout
```bash
shift + alt - r        # Rotar layout 270°
shift + alt - y        # Mirror en eje Y
shift + alt - x        # Mirror en eje X
shift + alt - t        # Toggle float (4x4 grid)
shift + alt - m        # Toggle zoom fullscreen
shift + alt - e        # Balance tree (resize igual)
shift + alt - f        # Toggle layout bsp/float
```

### Movimiento de Ventanas
```bash
# Swap windows
shift + alt - h/j/k/l  # Swap west/south/north/east

# Warp windows (move y split)
ctrl + alt - h/j/k/l   # Warp west/south/north/east

# Mover a displays
shift + alt - s        # Mover a display west
shift + alt - g        # Mover a display east

# Mover a espacios
shift + alt - p        # Mover a space prev
shift + alt - n        # Mover a space next
shift + alt - 1..7     # Mover a space específico
```

### Control de Yabai
```bash
# Start/Stop/Restart
ctrl + alt - q         # Stop yabai
ctrl + alt - s         # Start yabai
ctrl + alt - r         # Restart yabai
ctrl + cmd - q/s/r     # Alternativas con cmd

# Toggle padding
ctrl + alt - p         # Toggle padding espacio actual
```

## Integración con Otros Aplicativos
- **Yabai**: Todos los comandos ejecutan acciones de Yabai
- **macOS nativo**: Los atajos para spaces (Ctrl-1..7) se manejan nativamente

## Dependencias
```bash
# Instalación
brew install koekeishiya/formulae/skhd

# Servicio
skhd --start-service
skhd --stop-service
skhd --restart-service
```

## Portabilidad

### ✅ Portabilidad a Linux
- **Alternativas directas**:
  - `sxhkd`: Simple X Hotkey Daemon (muy similar)
  - i3 config: Keybindings nativos
  - sway config: Keybindings nativos
  - `xbindkeys`: Genérico para X11

### ⚠️ Portabilidad a Windows
- **Alternativas**:
  - `AutoHotkey`: Script de keybindings
  - `PowerToys Keyboard Manager`: Básico
  - `WinHotKey`: Gestor de hotkeys

## Recomendaciones

### Para Multiplataforma
1. **Mapeo de teclas**: Documentar equivalencias de modificadores
   - macOS `alt` → Linux `Mod1` / Windows `Alt`
   - macOS `cmd` → Linux `Mod4` (Super) / Windows `Win`
2. **Sintaxis común**: Crear un DSL o script generador
3. **Acciones abstractas**: Separar la acción del keybinding

### Para Nix
```nix
{
  # macOS
  homebrew.casks = [ "skhd" ];
  
  # Linux con i3
  xsession.windowManager.i3.config.keybindings = {
    "$mod+h" = "focus left";
    "$mod+j" = "focus down";
    # ... etc
  };
  
  # O con sxhkd
  services.sxhkd = {
    enable = true;
    keybindings = {
      "alt + h" = "bspc node -f west";
      # ... etc
    };
  };
}
```

## Listado de Transición

### De skhd a i3/sway config
| skhd | i3/sway | Notas |
|------|---------|-------|
| `alt - h : yabai -m window --focus west` | `bindsym $mod+h focus left` | Sintaxis directa |
| `shift + alt - r : yabai -m space --rotate 270` | `bindsym $mod+r exec --no-startup-id i3-msg layout toggle split` | Concepto diferente |
| `shift + alt - t : yabai -m window --toggle float` | `bindsym $mod+Shift+space floating toggle` | Similar |
| `ctrl + alt - q : yabai --stop-service` | `bindsym $mod+Shift+e exit` | Salir del WM |

### De skhd a sxhkd
```bash
# skhd
alt - h : yabai -m window --focus west

# sxhkd
alt + h
    bspc node -f west
```

### De skhd a AutoHotkey (Windows)
```ahk
; skhd: alt - h : yabai -m window --focus west
!h::Send {Left}  ; Simplified, real implementation would need WM integration
```

## Archivos de Configuración
```
~/.config/skhd/
└── skhdrc          # Configuración de keybindings
```

## Notas Especiales
- Los atajos `Ctrl-1..7` para cambiar de space están comentados porque se manejan con shortcuts nativos de macOS
- Existe duplicación de comandos con `ctrl+alt` y `ctrl+cmd` para flexibilidad
- Los comandos de yabai requieren que el servicio esté corriendo

## Estado de Sincronización
- **Repositorio Git**: frNNcs/.config (branch: main)
- **Syncthing**: Posiblemente sincronizado
