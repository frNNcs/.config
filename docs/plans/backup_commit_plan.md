# Plan de Commits: Backup de Configuración

Este plan organiza los cambios pendientes en el repositorio `.config` utilizando el prefijo `backup` para mantener la consistencia.

## Resumen de Commits (14)

1. **backup: update tmux configuration and scripts**
   - Cambios en `tmux/tmux.conf` y nuevos scripts en `tmux/scripts/`.
2. **backup: update zsh and p10k configuration**
   - Cambios en `.zshrc`, `.p10k.zsh` y directorio `zsh_p10k`.
3. **backup: update neovim plugins and core config**
   - Cambios en `nvim/init.lua`, `nvim/lua/plugins/neo-tree.lua` y gestión de `image.lua`.
4. **backup: update sketchybar items and styling**
   - Cambios en `sketchybarrc`, `colors.sh` y scripts de items (battery, calendar, cpu, volume).
5. **backup: update skhd keybindings**
   - Cambios en `skhd/skhdrc`.
6. **backup: update yabai display state**
   - Cambios en `yabai/.display_state`.
7. **backup: update spicetify theme and config**
   - Cambios en `spicetify/config-xpui.ini` y nuevos temas en `spicetify/Themes/RosePine/`.
8. **backup: update ghostty configuration**
   - Inclusión de archivos en la carpeta `ghostty/`.
9. **backup: update ai-tools and agent configs**
   - Cambios en `.agents/`, `.claude/`, `.codex/`, `.copilot/`, `gemini/`, `github-copilot/`, `oterm/`.
10. **backup: update opencode and mcp settings**
    - Cambios en `.opencode/`, `opencode/`, `mcphost/`, `temp_mcp_catalog.yaml`.
11. **backup: update scripts and utilities**
    - `draw_pua.py`, `restart_wacom.sh`, `scripts/`, `update_config.js`.
12. **backup: update documentation and notes**
    - `GEMINI.md`, `TODO_FUTURE.md`, `docs/`, `que-hace/`, `shortcuts-config.comparison.md`, `todo-qwen3_8b.md`.
13. **backup: update git and gh configuration**
    - `.gitignore`, `gh/hosts.yml`, `gh-unified/`.
14. **backup: update miscellaneous system configs**
    - `tigervnc/`, `syncthing/`, `configstore/`, `local/`, `vscode_copilot_settings.json`.

## Instrucciones de Ejecución
Para cada grupo, ejecutar:
```bash
git add <archivos_del_grupo>
git commit -m "backup: <mensaje_correspondiente>"
```
