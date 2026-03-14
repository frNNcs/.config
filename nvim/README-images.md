# Imágenes en Neovim (image.nvim)

Guía rápida para habilitar `3rd/image.nvim` y `render-markdown.nvim`.

## Requisitos

- Terminal con soporte gráfico (recomendado): **Kitty** o **WezTerm** (iTerm2 en macOS también funciona).
- ImageMagick instalado en el sistema:
  - macOS: `brew install imagemagick`
  - Ubuntu/Debian: `sudo apt install libmagickwand-dev`
  - Arch: `sudo pacman -S imagemagick`

> Nota: `image.nvim` usará bindings `magick` que se compilan via `luarocks`, por eso incluimos `luarocks.nvim` como dependencia del plugin.

## Instalación (con `lazy.nvim`)

1. He añadido `/lua/plugins/image.lua` con la configuración recomendada (backend `kitty`, integración con Markdown y Neorg).
2. También ajusté `/lua/plugins/render-markdown.lua` para asegurar `nvim-web-devicons` como dependencia.
3. Ejecuta en Neovim:

   :Lazy sync

   Esto descargará `3rd/image.nvim`, `luarocks.nvim` y el resto de dependencias.

4. Instala ImageMagick en tu sistema (ver requisitos arriba).
5. Reinicia Neovim y abre un archivo Markdown con imágenes para probar.

## Verificación

- Usa una terminal con soporte gráfico (ej. Kitty): abre un `README.md` con una imagen y verifica que la imagen renderice.
- Si algo falla, revisa `:checkhealth image` (si el plugin lo proporciona) y que `magick` esté en el PATH (`magick -version`).

## Tips

- Si usas `tmux`, activa `set -g escape-time 0` y asegúrate de que el terminal de tmux soporte gráficos o configurar `tmux` para dejar pasar las secuencias.
- Para Markdown, `render-markdown.nvim` y `image.nvim` trabajan bien juntos: `render-markdown` embellece el texto; `image.nvim` muestra las imágenes en el buffer.
