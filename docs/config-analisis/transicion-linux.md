# Guía de Transición a Linux (Ubuntu)

## Objetivo
Migrar la configuración actual de macOS a Linux Ubuntu manteniendo funcionalidad equivalente y workflow similar.

## Mapeo de Aplicativos

### Window Management

#### macOS: Yabai + skhd
**Alternativa Recomendada: i3-gaps**

```bash
# Instalación
sudo apt install i3-gaps i3status i3lock

# O para i3 estándar
sudo apt install i3
```

**Configuración Equivalente:**
```
# ~/.config/i3/config
set $mod Mod4

# Vim-style focus
bindsym $mod+h focus left
bindsym $mod+j focus down
bindsym $mod+k focus up
bindsym $mod+l focus right

# Move windows
bindsym $mod+Shift+h move left
bindsym $mod+Shift+j move down
bindsym $mod+Shift+k move up
bindsym $mod+Shift+l move right

# Gaps
gaps inner 12
gaps outer 0

# Layout
workspace_layout default
```

**Alternativas:**
- **sway**: i3 para Wayland (más moderno)
- **bspwm**: BSP puro como Yabai
- **awesome**: WM con Lua scripting
- **herbstluftwm**: Manual tiling

### Status Bar

#### macOS: SketchyBar
**Alternativa Recomendada: polybar**

```bash
# Instalación
sudo apt install polybar
```

**Configuración:**
```ini
; ~/.config/polybar/config.ini
[bar/main]
height = 37
background = ${colors.background}
foreground = ${colors.foreground}

modules-left = i3
modules-center = date
modules-right = pulseaudio battery cpu memory

[module/i3]
type = internal/i3

[module/date]
type = internal/date
date = %Y-%m-%d %H:%M

[module/battery]
type = internal/battery
battery = BAT0

[module/cpu]
type = internal/cpu
```

**Alternativa:**
- **waybar**: Para Wayland/sway (más moderno, JSON config)
- **i3status/i3blocks**: Simple, built-in para i3
- **lemonbar**: Minimalista

### Launcher

#### macOS: Raycast
**Alternativa Recomendada: rofi**

```bash
# Instalación
sudo apt install rofi

# Uso
rofi -show drun  # Launcher de aplicaciones
rofi -show run   # Ejecutar comandos
rofi -show window # Cambiar de ventana
```

**Configuración:**
```
# ~/.config/rofi/config.rasi
configuration {
    modi: "drun,run,window";
    font: "JetBrains Mono 12";
    show-icons: true;
}
```

**Alternativas:**
- **albert**: Similar a Alfred/Raycast
- **ulauncher**: Launcher moderno con extensiones
- **dmenu**: Minimalista (usado con i3)

### Terminal

#### macOS: Ghostty
**Ghostty es la solución recomendada y está disponible en Linux**. Alternativas si es necesario:

```bash
# Alacritty (GPU-accelerated, cross-platform)
sudo apt install alacritty

# Kitty (GPU-accelerated, features-rich)
sudo apt install kitty

# WezTerm (Lua configurable)
# Descargar desde GitHub releases
```

**Configuración Alacritty:**
```yaml
# ~/.config/alacritty/alacritty.yml
font:
  normal:
    family: JetBrainsMonoNL Nerd Font Mono
  size: 12

colors:
  # Catppuccin Mocha
  primary:
    background: '#1e1e2e'
    foreground: '#cdd6f4'

window:
  padding:
    x: 10
    y: 10
  decorations: none
```

### Mouse Configuration

#### macOS: LinearMouse
**Alternativa: libinput configuration**

```bash
# Deshabilitar aceleración
xinput set-prop <device-id> 'libinput Accel Profile Enabled' 0, 1

# O permanente en /etc/X11/xorg.conf.d/40-libinput.conf
Section "InputClass"
    Identifier "My Mouse"
    MatchIsPointer "yes"
    Option "AccelProfile" "flat"
    Option "AccelSpeed" "0"
EndSection
```

### Clipboard Manager

**Recomendado: clipmenu o copyq**

```bash
sudo apt install clipmenu
# O
sudo apt install copyq
```

### Compositor (Effects)

**Recomendado: picom**

```bash
sudo apt install picom

# ~/.config/picom/picom.conf
# Blur, shadows, transparency
```

## Shell y Tools

### Shell Tools (100% Compatible)

```bash
# Todos funcionan igual
sudo apt install lsd bat
cargo install atuin

# bat a veces se llama batcat
alias cat='batcat --paging=never --style=plain'
```

### Neovim (100% Compatible)

```bash
sudo apt install neovim ripgrep fd-find

# Configuración idéntica
ln -s ~/.config/nvim ~/.config/nvim
```

### Tmux (100% Compatible)

```bash
sudo apt install tmux

# Configuración idéntica
```

## Display Management

### Multi-Monitor

```bash
# xrandr para X11
xrandr --output HDMI-1 --right-of eDP-1

# O usar arandr (GUI)
sudo apt install arandr
```

## Notification System

```bash
# dunst - notification daemon
sudo apt install dunst

# ~/.config/dunst/dunstrc
```

## Theme Management

### Catppuccin Theme

```bash
# GTK Theme
git clone https://github.com/catppuccin/gtk.git
cd gtk
./install.sh

# Icons
git clone https://github.com/catppuccin/papirus-folders.git
cd papirus-folders
./install.sh
```

## File Manager

```bash
# CLI
sudo apt install ranger nnn

# GUI
sudo apt install thunar pcmanfm
```

## Screenshot Tools

```bash
# Scrot + feh
sudo apt install scrot feh

# Flameshot (más avanzado)
sudo apt install flameshot

# maim (moderno)
sudo apt install maim
```

## Sistema de Sonido

```bash
# PulseAudio (probablemente ya instalado)
sudo apt install pavucontrol

# O PipeWire (más moderno)
sudo apt install pipewire pipewire-pulse
```

## Configuración Completa i3

### ~/.config/i3/config

```
# Mod key
set $mod Mod4

# Font
font pango:JetBrains Mono 10

# Gaps
gaps inner 12
gaps outer 0

# Window colors (Catppuccin Mocha)
client.focused          #89b4fa #89b4fa #1e1e2e #fab387
client.focused_inactive #45475a #45475a #cdd6f4 #45475a
client.unfocused        #313244 #313244 #cdd6f4 #313244
client.urgent           #f38ba8 #f38ba8 #1e1e2e #f38ba8

# Window rules
for_window [class="Calculator"] floating enable
for_window [class="Pavucontrol"] floating enable

# Key bindings
bindsym $mod+Return exec ghostty
bindsym $mod+d exec rofi -show drun
bindsym $mod+Shift+q kill

# Focus
bindsym $mod+h focus left
bindsym $mod+j focus down
bindsym $mod+k focus up
bindsym $mod+l focus right

# Move
bindsym $mod+Shift+h move left
bindsym $mod+Shift+j move down
bindsym $mod+Shift+k move up
bindsym $mod+Shift+l move right

# Split
bindsym $mod+v split h
bindsym $mod+s split v

# Fullscreen
bindsym $mod+f fullscreen toggle

# Layout
bindsym $mod+e layout toggle split
bindsym $mod+w layout tabbed
bindsym $mod+Shift+space floating toggle

# Workspaces
set $ws1 "1"
set $ws2 "2"
set $ws3 "3"
set $ws4 "4"
set $ws5 "5"
set $ws6 "6"
set $ws7 "7"

bindsym $mod+1 workspace $ws1
bindsym $mod+2 workspace $ws2
# ... etc

bindsym $mod+Shift+1 move container to workspace $ws1
bindsym $mod+Shift+2 move container to workspace $ws2
# ... etc

# Autostart
exec --no-startup-id picom
exec --no-startup-id polybar
exec --no-startup-id dunst
exec --no-startup-id nm-applet

# Reload/restart
bindsym $mod+Shift+c reload
bindsym $mod+Shift+r restart
```

## Scripts de Instalación Automatizada

### install-ubuntu.sh

```bash
#!/bin/bash

# Update system
sudo apt update && sudo apt upgrade -y

# Window Manager
sudo apt install -y i3-gaps i3status i3lock

# Status bar
sudo apt install -y polybar

# Launcher
sudo apt install -y rofi

# Terminal
sudo apt install -y alacritty

# Compositor
sudo apt install -y picom

# Notifications
sudo apt install -y dunst

# Tools
sudo apt install -y \
    lsd bat ripgrep fd-find \
    neovim tmux git curl wget \
    ranger feh scrot maim \
    pavucontrol

# Rust (for atuin)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
cargo install atuin

# Fonts
sudo apt install -y fonts-jetbrains-mono

# Copy configs
ln -sf ~/.config/i3 ~/.config/i3
ln -sf ~/.config/polybar ~/.config/polybar
ln -sf ~/.config/rofi ~/.config/rofi
# ... etc

echo "Installation complete! Reboot and select i3 at login."
```

## Diferencias Clave macOS vs Linux

| Aspecto | macOS | Linux |
|---------|-------|-------|
| **Window Manager** | Yabai (overlay) | i3 (native) |
| **Modifier Key** | Option/Command | Super (Windows key) |
| **Package Manager** | Homebrew | APT/Pacman/DNF |
| **Display Server** | Quartz | X11/Wayland |
| **Config Location** | `~/.config` | `~/.config` (igual) |
| **Launcher** | Raycast | rofi/albert |
| **Status Bar** | SketchyBar | polybar/waybar |

## Comandos Útiles Linux

```bash
# Reload i3
$mod+Shift+r

# Lock screen
i3lock -c 1e1e2e

# Screenshot
scrot ~/Pictures/screenshot.png
maim -s ~/Pictures/screenshot.png  # Selection

# Display info
xrandr
xdpyinfo

# Input devices
xinput list
xinput list-props <device-id>

# Logs
journalctl -xe
~/.local/share/xorg/Xorg.0.log
```

## Recursos

- [i3 User Guide](https://i3wm.org/docs/userguide.html)
- [polybar Wiki](https://github.com/polybar/polybar/wiki)
- [rofi Documentation](https://github.com/davatorium/rofi)
- [Catppuccin Ports](https://github.com/catppuccin/catppuccin)
- [Arch Wiki](https://wiki.archlinux.org/) (útil para Ubuntu también)

## Troubleshooting

### i3 no inicia
```bash
# Check logs
cat ~/.local/share/xorg/Xorg.0.log
journalctl -xe

# Test config
i3 -C ~/.config/i3/config
```

### Gaps no funcionan
```bash
# Asegurarse de tener i3-gaps, no i3 regular
sudo apt remove i3
sudo apt install i3-gaps
```

### Teclas no funcionan
```bash
# Ver keycodes
xev

# Reload i3 config
$mod+Shift+r
```
