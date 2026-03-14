# Copilot Instructions
## Repo Scope
- This repo is the frNNcs macOS dotfiles monorepo; core subsystems are documented under [docs/config-analisis](docs/config-analisis).
- Catppuccin Mocha is the visual baseline; align new themes with [sketchybar/colors.sh](sketchybar/colors.sh), [ghostty/config](ghostty/config), [nvim/lua/plugins/catppuccin.lua](nvim/lua/plugins/catppuccin.lua), and [tmux/tmux.conf](tmux/tmux.conf).

## Window Management
- Tiling is orchestrated by yabai via [yabai/yabairc](yabai/yabairc); padding automation flows through [yabai/setup_padding.sh](yabai/setup_padding.sh), [yabai/display_watcher.sh](yabai/display_watcher.sh), and [yabai/lid_monitor.sh](yabai/lid_monitor.sh).
- Watcher scripts assume jq, bc, and yabai CLI are available; any structural changes must maintain their logging to display_watcher.log and lid_events.log for troubleshooting.
- Services are typically recycled with yabai --restart-service after config edits; padding toggles rely on space metadata so avoid clobbering the jq filters.

## Keyboard Shortcuts
- Global bindings live in [skhd/skhdrc](skhd/skhdrc) and call yabai -m commands; keep comment banners (# -- Section --) because [scripts/keybindings_cheatsheet.py](scripts/keybindings_cheatsheet.py) parses them.
- When adding bindings replicate the command style shift + alt - key : yabai ... to stay compatible with the textual TUI and future sxhkd migrations documented in [docs/config-analisis/02-skhd.md](docs/config-analisis/02-skhd.md).
- Use skhd --restart-service to reload; macOS handles space switching for ctrl-number so leave those lines commented unless workflow changes.

## Status Bar
- Sketchybar setup is defined in [sketchybar/sketchybarrc](sketchybar/sketchybarrc); items holds declarative slot definitions while plugins contains the executable scripts.
- Items reference PLUGIN_DIR env; when adding metrics ensure the script accepts NAME and INFO the same way as [sketchybar/plugins/cpu.sh](sketchybar/plugins/cpu.sh) and declare update_freq in items.
- Media and battery modules rely on jq; reuse the existing color exports from colors.sh for visual consistency.

## Terminal and Editor
- Ghostty profile in [ghostty/config](ghostty/config) controls fonts, padding, and theme; update in tandem with tmux to avoid mismatched fonts.
- Tmux uses TPM rooted at ~/.config/tmux/plugins; plugin references are documented in [tmux/tmux.conf](tmux/tmux.conf), so run tmux source-file ~/.config/tmux/tmux.conf or prefix I after edits.
- Neovim bootstraps lazy.nvim via [nvim/init.lua](nvim/init.lua) and imports plugin specs from [nvim/lua/plugins](nvim/lua/plugins); keep plugin configs stateless since [scripts/keybindings_cheatsheet.py](scripts/keybindings_cheatsheet.py) greps for vim.keymap.set with desc.

## Shell and Tooling
- [install-tools.sh](install-tools.sh) installs lsd, bat, atuin and appends guarded blocks to ~/.zshrc and fish/conf.d/lsd-bat-atuin.fish; maintain the marker comments so reruns stay idempotent.
- Shell helpers assume set -euo pipefail and mapcat style seen in [scripts/apply-catppuccin-lscolors.sh](scripts/apply-catppuccin-lscolors.sh); preserve that pattern when adding scripts under scripts/.
- uv.env.fish sources ~/.local/bin/env.fish; verify cross references before renaming environment files.

## Helper Applications
- The keybindings cheatsheet TUI lives in [scripts/keybindings_cheatsheet.py](scripts/keybindings_cheatsheet.py); it expects textual installed and category headings in configs, so sync new shortcuts there.
- Use [scripts/cheatsheet.sh](scripts/cheatsheet.sh) as the launcher; drop a virtualenv inside scripts/.venv if extra dependencies are needed.

## Documentation
- Deep dives for each component are curated in [docs/config-analisis](docs/config-analisis); update the matching markdown file when altering behaviour to keep the knowledge base aligned.
- TODO level work around SIP and advanced yabai features is tracked in [TODO_FUTURE.md](TODO_FUTURE.md); flag structural changes there when they impact prerequisites.

## Workflow Tips
- After modifying yabai or skhd, run yabai --restart-service and skhd --restart-service inside a terminal; monitor logs under ~/.config/yabai for regressions.
- Sketchybar modules can be reloaded individually via sketchybar --update NAME; use that instead of restarting the entire bar when iterating on plugins.
- For Neovim plugin updates, run :Lazy sync and commit the resulting [nvim/lazy-lock.json](nvim/lazy-lock.json) diff to lock versions.

## Testing and Validation
- Shell changes should pass shellcheck locally; the repo does not store CI but manual shellcheck script.sh is expected before commit.
- Python utilities target Python 3.11+ on macOS; run python3 scripts/keybindings_cheatsheet.py to confirm the textual UI loads without tracebacks.
- Validate tmux changes by running prefix I to reinstall plugins and ensure catppuccin theme still renders as configured.
