# Yabai - Window Manager

## Descripción General
Yabai es un gestor de ventanas en mosaico (tiling window manager) para macOS que permite organizar automáticamente las ventanas en layouts eficientes.

## Estado Actual
- **Ubicación**: `~/.config/yabai/`
- **Archivo Principal**: `yabairc`
- **Scripts Auxiliares**: `setup_padding.sh`, `display_watcher.sh`, `lid_monitor.sh`
- **Estado**: ✅ Configurado y funcional

## Características Configuradas

### Layout y Comportamiento
- **Layout por defecto**: BSP (Binary Space Partitioning)
- **Colocación de ventanas**: `second_child` - nuevas ventanas a la derecha/abajo
- **Mouse follows focus**: Activado
- **Mouse modifier**: ALT para mover/redimensionar ventanas
- **Mouse actions**:
  - ALT + Click izquierdo: Mover ventana
  - ALT + Click derecho: Redimensionar ventana
  - Drop en centro: Intercambiar ventanas

### Padding y Espaciado
```bash
window_gap: 12px
top_padding: 12px
bottom_padding: 12px
left_padding: 12px
right_padding: 12px
```

### Monitoreo Multi-Display
- Script de configuración automática de padding por display
- Watchers para detectar cambios de estado de pantalla
- Eventos configurados:
  - `display_added`
  - `display_removed`
  - `display_changed`
- Monitor de lid (tapa del laptop)

### Aplicaciones Excluidas
Las siguientes aplicaciones no son gestionadas por Yabai:
- System Settings / Configuración del Sistema
- Calculator
- Karabiner-Elements
- QuickTime Player
- LinearMouse
- Docker Desktop
- Google Drive
- ColorSlurp
- Raycast
- Monitor de Actividad

## Integración con Otros Aplicativos
- **skhd**: Maneja todos los atajos de teclado para Yabai
- **sketchybar**: Barra de estado que muestra información de espacios
- **Karabiner-Elements**: Modificador de teclas (mencionado en exclusiones)

## Dependencias
```bash
# Instalación
brew install koekeishiya/formulae/yabai

# Servicio
yabai --start-service
yabai --stop-service
yabai --restart-service
```

## Portabilidad

### ✅ Portabilidad a Linux
- **Alternativas directas**:
  - `i3` / `i3-gaps`: Similar filosofía, muy maduro
  - `sway`: i3 para Wayland
  - `bspwm`: BSP puro como Yabai
  - `herbstluftwm`: Altamente configurable
  - `awesome`: WM con Lua scripting

### ❌ Portabilidad a Windows
- **No disponible**: Yabai es específico de macOS
- **Alternativas**:
  - `komorebi`: Tiling WM para Windows (similar a Yabai)
  - `bug.n`: Tiling WM en AutoHotkey
  - `GlazeWM`: Tiling WM moderno para Windows
  - PowerToys FancyZones (limitado)

## Estado de Características Avanzadas
Según `TODO_FUTURE.md`, hay características pendientes que requieren deshabilitar SIP:
- Cambio instantáneo de espacios
- Eliminación de sombras
- Transparencia
- Sticky windows
- Scripting Addition

## Recomendaciones

### Para Multiplataforma
1. **Configuración base común**: Extraer la configuración de layout, gaps y reglas
2. **Scripts de conversión**: Crear templates para convertir reglas de Yabai a i3/sway
3. **Archivo de transición**: Mapear aplicaciones macOS a sus equivalentes Linux/Windows

### Para Nix
```nix
{
  # macOS
  homebrew.casks = [ "yabai" ];
  
  # Linux
  environment.systemPackages = with pkgs; [
    i3-gaps  # o sway para Wayland
    i3status
  ];
}
```

## Listado de Transición

### De Yabai a i3/sway
| Concepto Yabai | Equivalente i3/sway | Notas |
|----------------|---------------------|-------|
| `yabai -m space --layout bsp` | modo por defecto | i3/sway son tiling por defecto |
| `window_gap` | `gaps inner` / `gaps outer` | Sintaxis diferente |
| `yabai -m window --focus` | `focus left/right/up/down` | Comando directo |
| `yabai -m window --swap` | `move left/right/up/down` | Similar |
| `yabai -m rule --add app=X manage=off` | `for_window [class="X"] floating enable` | Reglas por clase |
| Espacios (spaces) | Workspaces | Concepto equivalente |

### Scripts a Migrar
- `setup_padding.sh` → script de autostart para i3/sway
- `display_watcher.sh` → hooks de i3/sway para xrandr
- `lid_monitor.sh` → script systemd o i3 exec

## Archivos de Configuración
```
~/.config/yabai/
├── yabairc                 # Configuración principal
├── setup_padding.sh        # Setup inicial de padding
├── display_watcher.sh      # Monitor de displays
└── lid_monitor.sh          # Monitor de lid
```

## Estado de Sincronización
- **Repositorio Git**: frNNcs/.config (branch: main)
- **Syncthing**: Posiblemente sincronizado via Obsidian
