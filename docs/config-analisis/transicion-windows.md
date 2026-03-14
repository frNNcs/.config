# Guía de Transición a Windows

## Objetivo
Adaptar configuración de desarrollo a Windows manteniendo funcionalidad similar mediante WSL2 y herramientas nativas.

## Estrategia: Enfoque Híbrido

### Opción 1: WSL2 (Recomendado para Desarrollo)
- Todo el environment de Linux en Windows
- Reutilizar configuraciones de Linux
- VS Code con WSL extension
- Terminal en WSL

### Opción 2: Nativo Windows
- Herramientas Windows-native
- PowerShell como shell principal
- Window management nativo

### Opción 3: Híbrido (Mejor)
- WSL2 para desarrollo y terminal
- Windows native para GUI y window management
- Integración entre ambos

## Configuración WSL2

### Instalación

```powershell
# PowerShell como Admin
wsl --install
# O específicamente Ubuntu
wsl --install -d Ubuntu-22.04

# Verificar versión
wsl --list --verbose

# Asegurar WSL2
wsl --set-default-version 2
```

### Configuración Básica

```bash
# Dentro de WSL
# Instalar todo igual que en Linux
sudo apt update && sudo apt upgrade -y

# Copiar configuraciones
ln -sf /mnt/c/Users/<user>/.config ~/.config
```

### Windows Terminal

**Instalación:**
- Desde Microsoft Store: "Windows Terminal"
- O via winget: `winget install Microsoft.WindowsTerminal`

**Configuración:**
```json
// settings.json
{
    "defaultProfile": "{Ubuntu-22.04-GUID}",
    "profiles": {
        "list": [
            {
                "guid": "{Ubuntu-22.04-GUID}",
                "name": "Ubuntu",
                "source": "Windows.Terminal.Wsl",
                "fontFace": "JetBrainsMono NF",
                "fontSize": 11,
                "colorScheme": "Catppuccin Mocha",
                "padding": "10, 10, 10, 10"
            }
        ]
    },
    "schemes": [
        {
            "name": "Catppuccin Mocha",
            "background": "#1E1E2E",
            "foreground": "#CDD6F4",
            // ... colores Catppuccin
        }
    ]
}
```

## Mapeo de Aplicativos

### Window Management

#### macOS: Yabai
**Alternativa: Komorebi**

```powershell
# Instalación con Scoop
scoop install komorebi

# O con winget
winget install LGUG2Z.komorebi
```

**Configuración:**
```json
// ~\komorebi\komorebi.json
{
  "app_specific_configuration_path": "~\\komorebi\\applications.yaml",
  "window_hiding_behaviour": "Minimize",
  "cross_monitor_move_behaviour": "Insert",
  "default_workspace_padding": 12,
  "default_container_padding": 12,
  "focus_follows_mouse": "Windows"
}
```

**Alternativas:**
- **bug.n**: Tiling WM en AutoHotkey
- **GlazeWM**: Tiling WM moderno para Windows
- **PowerToys FancyZones**: Zones para organizar ventanas (más simple)

### Hotkey Management

#### macOS: skhd
**Alternativa: AutoHotkey**

```ahk
; ~/.config/autohotkey/hotkeys.ahk
#NoEnv
SendMode Input

; Win + H/J/K/L para focus
#h::Send {Left}
#j::Send {Down}
#k::Send {Up}
#l::Send {Right}

; Win + Shift + H/J/K/L para move
#+h::WinMove, A,, -100, 0
#+j::WinMove, A,, 0, 100
#+k::WinMove, A,, 0, -100
#+l::WinMove, A,, 100, 0

; Win + Return para terminal
#Enter::Run, wt.exe
```

**Alternativa:**
- **PowerToys Keyboard Manager**: Remap keys (más simple)

### Launcher

#### macOS: Raycast
**Alternativa: PowerToys Run**

```powershell
# Instalación
winget install Microsoft.PowerToys

# Atajo por defecto: Alt+Space
```

**Alternativas:**
- **Wox**: Launcher type Alfred
- **Keypirinha**: Launcher ligero
- **Launchy**: Launcher simple

### Terminal

#### Opciones:
1. **Windows Terminal** + WSL2 (Recomendado)
2. **Alacritty** (Windows native, cross-platform)
3. **WezTerm** (Lua config, cross-platform)

**Alacritty en Windows:**
```yaml
# ~\AppData\Roaming\alacritty\alacritty.yml
font:
  normal:
    family: JetBrainsMono NF
  size: 11

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

### Shell

#### PowerShell (Windows Native)

**Setup:**
```powershell
# Install Oh My Posh
winget install JanDeDobbeleer.OhMyPosh

# Install PSReadLine
Install-Module -Name PSReadLine -Scope CurrentUser

# Profile: ~\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
oh-my-posh init pwsh --config ~\.config\ohmyposh\catppuccin.json | Invoke-Expression

# Aliases
Set-Alias -Name ls -Value lsd
Set-Alias -Name cat -Value bat
```

#### Zsh en WSL2
- Reutilizar configuración de Linux/macOS

### Shell Tools

```powershell
# Instalación via Scoop
scoop install lsd bat
scoop install ripgrep fd

# Atuin (via cargo)
cargo install atuin
atuin init powershell | Out-String | Invoke-Expression
```

### Editor

#### Neovim
```powershell
# Instalación
scoop install neovim

# Config location: ~\AppData\Local\nvim\
# O via symlink desde WSL
New-Item -ItemType SymbolicLink -Path ~\AppData\Local\nvim -Target \\wsl$\Ubuntu\home\user\.config\nvim
```

#### VS Code con WSL
```bash
# Instalar en Windows
winget install Microsoft.VisualStudioCode

# Extension: Remote - WSL
code --install-extension ms-vscode-remote.remote-wsl

# Usar desde WSL
code .
```

### Git

```powershell
# Instalación
winget install Git.Git

# Config
git config --global user.name "Name"
git config --global user.email "email"

# Credential Manager
git config --global credential.helper manager
```

### Fonts

```powershell
# Manual: Descargar de Nerd Fonts
# https://github.com/ryanoasis/nerd-fonts/releases

# O via Scoop
scoop bucket add nerd-fonts
scoop install JetBrains-Mono-NF
```

### Mouse Configuration

**Herramientas:**
- **X-Mouse Button Control**: Botones custom
- **Driver del mouse**: Configuración de aceleración

### Clipboard Manager

**PowerToys:**
- Built-in clipboard history: Win+V

**Alternativas:**
- **Ditto**: Clipboard manager potente
- **ClipClip**: Moderno y simple

## File System Integration

### Acceder a archivos Windows desde WSL

```bash
# Windows C:\ está en
/mnt/c/

# Ejemplo
cd /mnt/c/Users/<username>/Desktop
```

### Acceder a archivos WSL desde Windows

```
\\wsl$\Ubuntu\home\<username>\
```

### Symlinks

```bash
# Crear symlink de configs
ln -sf /mnt/c/Users/<user>/.config ~/.config
```

## Configuración Completa de Desarrollo

### VS Code + WSL

```json
// settings.json
{
  "terminal.integrated.defaultProfile.windows": "WSL",
  "remote.WSL.fileWatcher.polling": true,
  "editor.fontFamily": "JetBrainsMono NF",
  "workbench.colorTheme": "Catppuccin Mocha"
}
```

### SSH Keys

```bash
# Generar en WSL
ssh-keygen -t ed25519 -C "email@example.com"

# Usar en Windows
# Copiar a Windows
cp ~/.ssh/id_ed25519* /mnt/c/Users/<user>/.ssh/
```

## PowerToys Configuration

### Useful Modules:
1. **FancyZones**: Window layouts
2. **PowerToys Run**: Launcher
3. **Keyboard Manager**: Key remapping
4. **Color Picker**: Útil para themes
5. **File Explorer**: Preview de archivos

### FancyZones Setup
- Crear zones que simulen tiling
- Atajos: Win+Shift+Arrow para mover ventanas

## Package Management

### Scoop (Recomendado)

```powershell
# Instalación
iwr -useb get.scoop.sh | iex

# Buckets
scoop bucket add extras
scoop bucket add nerd-fonts

# Instalar herramientas
scoop install git neovim alacritty lsd bat ripgrep fd
```

### Winget (Built-in)

```powershell
# Buscar
winget search neovim

# Instalar
winget install Neovim.Neovim

# Actualizar todo
winget upgrade --all
```

### Chocolatey (Alternativa)

```powershell
# Instalación
Set-ExecutionPolicy Bypass -Scope Process -Force
iwr https://community.chocolatey.org/install.ps1 -UseBasicParsing | iex

# Usar
choco install git neovim
```

## Syncthing en Windows

```powershell
# Instalación
scoop install syncthing

# O descarga desde https://syncthing.net/

# Ejecutar
syncthing.exe

# Web UI: http://localhost:8384/
```

## Scripts de Automatización

### setup-windows.ps1

```powershell
# PowerShell Admin
# Setup de entorno completo

# Install WSL2
wsl --install -d Ubuntu-22.04

# Install Scoop
iwr -useb get.scoop.sh | iex

# Add buckets
scoop bucket add extras
scoop bucket add nerd-fonts

# Install tools
$tools = @(
    'git',
    'neovim',
    'alacritty',
    'lsd',
    'bat',
    'ripgrep',
    'fd',
    'JetBrains-Mono-NF',
    'komorebi',
    'syncthing'
)

foreach ($tool in $tools) {
    scoop install $tool
}

# Install PowerToys
winget install Microsoft.PowerToys

# Install Windows Terminal
winget install Microsoft.WindowsTerminal

# Install VS Code
winget install Microsoft.VisualStudioCode

Write-Host "Setup complete! Restart and configure WSL."
```

## Diferencias Windows vs macOS/Linux

| Aspecto | macOS/Linux | Windows |
|---------|-------------|---------|
| **Path Separator** | `/` | `\` |
| **Home** | `~` | `%USERPROFILE%` o `~` (PowerShell) |
| **Config Location** | `~/.config` | `~\AppData\Roaming` o `~\.config` |
| **Line Endings** | LF | CRLF (configurar Git) |
| **Case Sensitivity** | Sí | No (por defecto) |
| **Package Manager** | apt/brew | scoop/winget/choco |
| **Shell** | zsh/bash | PowerShell/cmd |

## Configurar Git para Line Endings

```bash
# En WSL
git config --global core.autocrlf input

# En Windows
git config --global core.autocrlf true
```

## Performance Tips

### WSL2 Performance

```
# .wslconfig en ~
[wsl2]
memory=8GB
processors=4
swap=2GB
```

### Exclude from Windows Defender

```powershell
# Excluir WSL de Defender para mejor performance
Add-MpPreference -ExclusionPath "C:\Users\<user>\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu22.04LTS_79rhkp1fndgsc"
```

## Recursos

- [WSL2 Documentation](https://docs.microsoft.com/en-us/windows/wsl/)
- [Windows Terminal Docs](https://docs.microsoft.com/en-us/windows/terminal/)
- [Komorebi Wiki](https://github.com/LGUG2Z/komorebi)
- [PowerToys Documentation](https://docs.microsoft.com/en-us/windows/powertoys/)
- [Scoop Documentation](https://scoop.sh/)

## Troubleshooting

### WSL2 no inicia
```powershell
# Verificar estado
wsl --status

# Actualizar kernel
wsl --update

# Reiniciar
wsl --shutdown
```

### Network issues en WSL2
```bash
# Reset networking
sudo rm /etc/resolv.conf
sudo bash -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf'
```

### Slow file access from Windows
- Evitar trabajar con archivos en `/mnt/c/` desde WSL
- Mejor trabajar en `~` de WSL y acceder desde Windows via `\\wsl$\`
