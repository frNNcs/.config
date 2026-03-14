# Otros Aplicativos Configurados

## Descripción General
Aplicativos adicionales configurados en el sistema que complementan el workflow.

## 1. LinearMouse

### Descripción
Aplicación para personalizar el comportamiento del mouse en macOS.

### Ubicación
- **Config**: `~/.config/linearmouse/linearmouse.json`

### Configuración Actual
```json
{
  "pointer": {
    "acceleration": 2,
    "disableAcceleration": true,
    "speed": 0.722
  },
  "scrolling": {
    "distance": { "vertical": 1 },
    "acceleration": { "vertical": 1 },
    "reverse": { "vertical": true },
    "speed": { "vertical": 0 }
  },
  "buttons": {
    "universalBackForward": true
  }
}
```

### Features
- Deshabilita aceleración del mouse
- Scroll invertido (natural)
- Botones back/forward universales
- Configuración por dispositivo

### Portabilidad
- **Linux**: `xinput`, `libinput` configuration
- **Windows**: Drivers del mouse, `X-Mouse Button Control`

---

## 2. Raycast

### Descripción
Launcher y productivity tool para macOS, similar a Alfred o Spotlight.

### Ubicación
- **Config**: `~/.config/raycast/config.json`
- **Extensions**: `~/.config/raycast/extensions/`
- **AI**: `~/.config/raycast/ai/`

### Features Probables
- Quick launcher
- Clipboard history
- Snippets
- Extensions
- AI integration
- Window management
- Script commands

### Portabilidad
- **Linux**: `rofi`, `albert`, `ulauncher`
- **Windows**: `PowerToys Run`, `Wox`, `Keypirinha`

---

## 3. Fabric

### Descripción
Framework de patterns para IA (probablemente para prompts y workflows).

### Ubicación
- **Base**: `~/.config/fabric/`
- **Patterns**: `~/.config/fabric/patterns/`
- **Contexts**: `~/.config/fabric/contexts/`
- **Sessions**: `~/.config/fabric/sessions/`

### Patterns Detectados
```
extract_main_activities
t_create_opening_sentences
summarize_git_diff
extract_characters
fix_typos
extract_wisdom
... más patterns
```

### Features
- Templates de prompts
- Workflows de IA
- Contextos guardados
- Sesiones de trabajo

### Portabilidad
✅ Completamente portable (solo archivos de configuración)

---

## 4. GitHub CLI (gh)

### Descripción
Cliente de línea de comandos oficial de GitHub.

### Ubicación
- **Config Unified**: `~/.config/gh-unified/config.yml`
- **Hosts**: `~/.config/gh-unified/hosts.yml`
- **Legacy**: `~/.config/gh/`

### Features
- Gestión de PRs
- Issues
- Repos
- Actions
- Gists

### Portabilidad
✅ Cross-platform (Windows, Linux, macOS)

---

## 5. Gemini (Google AI)

### Descripción
Cliente o configuración para Google Gemini AI.

### Ubicación
- **Base**: `~/.config/gemini/`
- **Settings**: `settings.json`
- **OAuth**: `oauth_creds.json`
- **Accounts**: `google_accounts.json`

### Files
```
installation_id
user_id
state.json
antigravity/
tmp/
```

### Portabilidad
✅ Cross-platform (archivos de configuración)

---

## 6. Spicetify

### Descripción
Customización de Spotify (temas, extensiones, apps custom).

### Ubicación
- **Base**: `~/.config/spicetify/`
- **Config**: `config-xpui.ini`
- **Auto-apply**: `auto-apply.sh`
- **CustomApps**: Apps personalizadas
- **Extensions**: Extensiones
- **Themes**: Temas custom

### Features
- Temas custom para Spotify
- Extensiones JavaScript
- Apps personalizadas
- Auto-update

### Portabilidad
✅ Cross-platform (Windows, Linux, macOS)

---

## 7. Syncthing

### Descripción
Sincronización de archivos P2P, usado para sincronizar configuraciones.

### Ubicación
- **Base**: `~/.config/syncthing/`
- **Config**: `config.xml`
- **Docker**: `docker-compose.yml`

### Features
- Sync continuo
- Cifrado
- Versiones de archivos
- Multi-dispositivo

### Uso en el Proyecto
Probablemente sincroniza:
- Configuraciones
- Obsidian vault (`~/projects/homelab/DATA/syncthing/obsidian`)
- Scripts y dotfiles

### Portabilidad
✅ Cross-platform (Windows, Linux, macOS, Android)

---

## 8. iTerm2

> **⚠️ DEPRECADO**: Reemplazado por Ghostty (ver [03-ghostty.md](03-ghostty.md))

### Decisión de Migración
iTerm2 ha sido reemplazado completamente por **Ghostty** como terminal principal porque:
- ✅ Ghostty es cross-platform (macOS, Linux, Windows en desarrollo)
- ✅ Configuración única para todas las plataformas
- ✅ Soporte moderno (GPU rendering, imágenes, etc.)
- ✅ Tema Catppuccin consistente
- ✅ Misma experiencia en todos los dispositivos

### Estado
- **Legacy**: `~/.config/iterm2/` puede ser eliminado
- **Configuración**: Migrada completamente a Ghostty
- **Recomendación**: Desinstalar iTerm2

---

## 9. Neofetch

### Descripción
Tool para mostrar información del sistema con ASCII art.

### Ubicación
- **Config**: `~/.config/neofetch/config.conf`

### Features
- System info
- ASCII logos
- Customizable output
- Screenshot tool

### Portabilidad
✅ Cross-platform

---

## 10. UV (Python Package Manager)

### Descripción
Package manager rápido para Python (alternativa a pip).

### Ubicación
- **Base**: `~/.config/uv/`
- **Receipt**: `uv-receipt.json`

### Features
- Instalación rápida de paquetes
- Cache eficiente
- Compatible con pip

### Portabilidad
✅ Cross-platform

---

## 11. LLM Settings

### Descripción
Configuraciones para LLMs (Language Models).

### Ubicación
- **Base**: `~/.config/llm-settings/`

### Portabilidad
✅ Cross-platform

---

## 12. OTerm

### Descripción
Terminal en terminal (probablemente para Ollama).

### Ubicación
- **Config**: `~/.config/oterm/config.json`

### Portabilidad
✅ Cross-platform

---

## 13. OpenCode

### Descripción
Cliente o configuración para AI coding.

### Ubicación
- **Base**: `~/.config/opencode/`
- **Config**: `config.json`
- **Package**: `package.json`
- **Docs**: `docs/`

### Portabilidad
✅ Cross-platform

---

## 14. MCP Host

### Descripción
Model Context Protocol host configuration.

### Ubicación
- **Base**: `~/.config/mcphost/`

### Portabilidad
✅ Cross-platform

---

## 15. TigerVNC

### Descripción
Cliente VNC para acceso remoto.

### Ubicación
- **Config**: `~/.config/tigervnc/default.tigervnc`

### Portabilidad
✅ Cross-platform

---

## 16. VSCode Data

### Descripción
Datos de VS Code (extensiones, cache, settings).

### Ubicación
- **Base**: `~/.config/vscode-data/`

### Contenido
- Cookies
- Cache
- Extensions
- Backups
- Profiles

### Portabilidad
✅ Cross-platform (con adaptaciones de paths)

---

## 17. GitHub Copilot

### Descripción
Configuración de GitHub Copilot.

### Ubicación
- **Base**: `~/.config/github-copilot/`
- **Versions**: `versions.json`
- **IntelliJ**: Config para IntelliJ

### Portabilidad
✅ Cross-platform

---

## 18. ConfigStore

### Descripción
Store de configuraciones de varios aplicativos.

### Ubicación
- **Base**: `~/.config/configstore/`

### Archivos
- `lighthouse.json`
- `update-notifier-npm-check-updates.json`
- `update-notifier-@github/`
- `update-notifier-@google/`

### Portabilidad
✅ Cross-platform

---

## 19. cagent

### Descripción
Configuración de algún agente (posiblemente AI).

### Ubicación
- **Base**: `~/.config/cagent/`

---

## Resumen de Portabilidad

### ✅ Completamente Portable
- Fabric
- GitHub CLI
- Gemini
- Spicetify
- Syncthing
- Neofetch
- UV
- LLM Settings
- OTerm
- OpenCode
- MCP Host
- TigerVNC
- VSCode Data
- GitHub Copilot
- ConfigStore

### ⚠️ Con Alternativas  
- LinearMouse (xinput, libinput)
- Raycast (rofi, PowerToys Run)

### ❌ macOS Only
- Ninguno ✨ (todo es portable o tiene alternativas equivalentes)

## Integración Nix

```nix
{
  # Portable tools
  environment.systemPackages = with pkgs; [
    gh
    neofetch
    syncthing
    tigervnc
  ];
  
  # Spicetify
  programs.spicetify = {
    enable = true;
    theme = "catppuccin";
  };
  
  # Syncthing
  services.syncthing = {
    enable = true;
    user = "username";
    dataDir = "/home/username/.config/syncthing";
  };
  
  # VSCode
  programs.vscode = {
    enable = true;
    extensions = [ /* ... */ ];
  };
}
```
