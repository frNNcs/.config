Instalación de lsd, bat y atuin

Este repositorio contiene un script para instalar y configurar lsd (lsd-rs), bat, y atuin en macOS.

Requisitos
- Homebrew instalado (https://brew.sh/)
- Zsh (configurado en ~/.zshrc) o Fish (en ~/.config/fish/conf.d)

Uso
1. Abre una terminal zsh y ejecuta:

   ./install-tools.sh

2. El script realizará las siguientes acciones:
- Verifica que Homebrew esté instalado
- Instala lsd, bat y atuin usando Homebrew
- Añade un bloque a ~/.zshrc con:
  - alias ls="lsd"
  - alias cat="bat --paging=never --style=plain"
  - eval "$(atuin init zsh)"
- Crea un archivo Fish en ~/.config/fish/conf.d/ con alias equivalentes y `atuin` inicializado

Adicionalmente:
- Crea `~/.config/lsd/colors.yaml` con la paleta Catppuccin (Mocha) y activa el tema custom en `~/.config/lsd/config.yaml`. Esto aplica la paleta a los elementos de lsd (permits, git-status, fecha, etc.).
- Si quieres controlar los colores por tipo de archivo (por ejemplo: carpetas, ejecutables), lsd respeta `LS_COLORS` — puedes exportarla con `dircolors` o un valor en tu `~/.zshrc`.

Notas
- El script hace una copia de seguridad de tu ~/.zshrc antes de modificarlo.
- Puedes revisar los cambios en ~/.zshrc.bak-<timestamp> si quieres revertir.
- Si usas otra shell, añade manualmente la inicialización de atuin siguiendo la documentación oficial.

Notas sobre los colores
- El archivo `~/.config/lsd/colors.yaml` usa valores hex de la paleta Catppuccin Mocha.
- Algunos terminales no soportan 24-bit colores; si ves diferencias, habilita truecolor en tu terminal o usa una terminal compatible (iTerm2, Alacritty, Kitty, etc.).
- Para controlar colores por tipo de archivo (ej.: carpetas, ejecutables, etc.) puedes exportar `LS_COLORS` en tu shell, o usar `dircolors` y generar un `LS_COLORS` con el esquema que prefieras.
Aplicar LS_COLORS automáticamente
- Se añadió un script `./scripts/apply-catppuccin-lscolors.sh` que genera una variable `LS_COLORS` basada en `~/.config/lsd/colors.yaml` y puede aplicar la exportación automáticamente con `--apply`.

Ejemplo de uso:
```bash
./scripts/apply-catppuccin-lscolors.sh
# Verás la cadena LS_COLORS generada
./scripts/apply-catppuccin-lscolors.sh --apply
# Crea un backup de ~/.zshrc y añade el bloque con export LS_COLORS
source ~/.zshrc
```

Nota: El script preserva los valores previos de `LS_COLORS` (los concatena) para no perder mapeos por extensión que ya tengas.

Más información
- lsd: https://github.com/lsd-rs/lsd
- bat: https://github.com/sharkdp/bat
- atuin: https://github.com/atuinsh/atuin
