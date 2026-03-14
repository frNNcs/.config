# Ghostty - Terminal Emulator

## Descripción General
Ghostty es un emulador de terminal moderno y rápido, escrito en Zig, con soporte nativo para GPU rendering y características modernas.

## Estado Actual
- **Ubicación**: `~/.config/ghostty/`
- **Archivo Principal**: `config`
- **Themes**: `~/.config/ghostty/themes/`
- **Estado**: ✅ Configurado y funcional

## Configuración Actual

### Fuentes
```
Font Family: JetBrainsMonoNL Nerd Font Mono
- Regular: JetBrainsMonoNL Nerd Font Mono
- Bold: JetBrainsMonoNL NFM Bold
- Italic: JetBrainsMonoNL NFM Italic
- Bold Italic: JetBrainsMonoNL NFM Bold Italic

font-thicken: true
font-thicken-strength: 80
```

### Tema
```
theme: catppuccin-mocha.conf
```

### Apariencia macOS
```
macos-titlebar-style: hidden      # Sin barra de título
window-padding-x: 10
window-padding-y: 10
```

### Transparencia (Opcional - Comentado)
```
# background-opacity: 0.95
# background-blur-radius: 20
```

### Comportamiento
```
mouse-hide-while-typing: true
copy-on-select: true
cursor-style: block
cursor-style-blink: false
shell-integration: zsh
```

## Integración con Otros Aplicativos
- **zsh**: Shell integration habilitada
- **tmux**: Compatible con passthrough de imágenes
- **nvim**: Soporte para imágenes en Neovim
- **Nerd Fonts**: JetBrains Mono con glyphs

## Dependencias
```bash
# Instalación en macOS
brew install --cask ghostty

# Fuente requerida
brew tap homebrew/cask-fonts
brew install --cask font-jetbrains-mono-nerd-font
```

## Portabilidad

### ✅ Portabilidad a Linux
- **Ghostty está disponible en Linux**
- Misma configuración puede ser usada
- Ajustes necesarios:
  - Remover `macos-titlebar-style`
  - Verificar disponibilidad de fuentes

### ✅ Portabilidad a Windows
- **En desarrollo**: Ghostty tiene planes para Windows
- **Alternativas actuales**:
  - `Windows Terminal`: Moderno y configurable
  - `Alacritty`: Cross-platform, similar performance
  - `WezTerm`: Cross-platform, Lua configurable
  - `Kitty`: Cross-platform (Linux/macOS, Windows experimental)

## Recomendaciones

### Para Multiplataforma
1. **Configuración condicional por OS**:
```bash
# config-macos
macos-titlebar-style = hidden

# config-linux
# (Linux-specific settings)

# config-windows
# (Windows-specific settings)
```

2. **Template base común**:
```
font-family = JetBrainsMonoNL Nerd Font Mono
theme = catppuccin-mocha
window-padding-x = 10
window-padding-y = 10
copy-on-select = true
```

### Para Nix
```nix
{
  programs.ghostty = {
    enable = true;
    settings = {
      font-family = "JetBrainsMonoNL Nerd Font Mono";
      theme = "catppuccin-mocha";
      window-padding-x = 10;
      window-padding-y = 10;
      copy-on-select = true;
      cursor-style = "block";
      cursor-style-blink = false;
    };
  };
  
  # Fuentes
  fonts.packages = with pkgs; [
    (nerdfonts.override { fonts = [ "JetBrainsMono" ]; })
  ];
}
```

## Listado de Transición

### Configuración Cross-Platform
| Opción | macOS | Linux | Windows | Notas |
|--------|-------|-------|---------|-------|
| `font-family` | ✅ | ✅ | ✅ | Universal |
| `theme` | ✅ | ✅ | ✅ | Universal |
| `macos-titlebar-style` | ✅ | ❌ | ❌ | Solo macOS |
| `window-padding-x/y` | ✅ | ✅ | ✅ | Universal |
| `copy-on-select` | ✅ | ✅ | ⚠️ | Windows behavior may differ |
| `shell-integration` | zsh | bash/zsh/fish | powershell/cmd | Shell específica |

### Alternativas por Plataforma
| Feature | macOS (Ghostty) | Linux | Windows |
|---------|-----------------|-------|---------|
| Terminal | Ghostty | Ghostty / Alacritty / Kitty | Windows Terminal / Alacritty / WezTerm |
| GPU Rendering | ✅ | ✅ | ✅ (con alternativas) |
| Image Support | ✅ | ✅ | ⚠️ (limitado) |
| Ligatures | ✅ | ✅ | ✅ |

## Features Destacables
1. **GPU Rendering**: Rendering acelerado por GPU para mejor performance
2. **Image Support**: Soporte nativo para mostrar imágenes (útil con nvim)
3. **Shell Integration**: Integración profunda con la shell
4. **Nerd Font Support**: Glyphs e iconos en la terminal
5. **Modern Config**: Configuración simple y declarativa

## Temas Disponibles
```bash
~/.config/ghostty/themes/
# Actualmente usando: catppuccin-mocha.conf
```

## Archivos de Configuración
```
~/.config/ghostty/
├── config              # Configuración principal
└── themes/
    └── catppuccin-mocha.conf
```

## Migraciones Potenciales

### A Alacritty (Cross-platform)
```yaml
# ~/.config/alacritty/alacritty.yml
font:
  normal:
    family: JetBrainsMonoNL Nerd Font Mono
  size: 12
  
colors:
  # Import Catppuccin Mocha

window:
  padding:
    x: 10
    y: 10
  decorations: none
```

### A WezTerm (Cross-platform)
```lua
-- ~/.wezterm.lua
return {
  font = wezterm.font 'JetBrainsMonoNL Nerd Font Mono',
  color_scheme = 'Catppuccin Mocha',
  window_padding = {
    left = 10,
    right = 10,
    top = 10,
    bottom = 10,
  },
  hide_tab_bar_if_only_one_tab = true,
}
```

## Estado de Sincronización
- **Repositorio Git**: frNNcs/.config (branch: main)
- **Syncthing**: Posiblemente sincronizado
