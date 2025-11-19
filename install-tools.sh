#!/usr/bin/env bash
# Install lsd, bat and atuin on macOS using Homebrew and configure shell aliases
set -euo pipefail

BREW=$(command -v brew || true)
if [[ -z "$BREW" ]]; then
  echo "Homebrew not found. Please install Homebrew first: https://brew.sh/"
  exit 1
fi

echo "Updating Homebrew..."
brew update

install_or_skip() {
  PKG="$1"
  if brew list "$PKG" >/dev/null 2>&1; then
    echo "$PKG already installed. Skipping."
  else
    echo "Installing $PKG..."
    brew install "$PKG"
  fi
}

install_or_skip lsd
install_or_skip bat
install_or_skip atuin || {
  # If brew install fails, try tapping
  echo "Trying to tap atuinsh/atuin and install..."
  brew tap atuinsh/atuin || true
  brew install atuin
}

ZSHRC="$HOME/.zshrc"
BACKUP_ZSHRC="$ZSHRC.bak-$(date +%s)"

echo "Backing up $ZSHRC to $BACKUP_ZSHRC"
cp -f "$ZSHRC" "$BACKUP_ZSHRC" || true

add_if_missing() {
  TARGET="$1"
  PATTERN="$2"
  if [[ -f "$TARGET" ]]; then
    if ! grep -q -F "$PATTERN" "$TARGET"; then
      echo "$PATTERN" >> "$TARGET"
      echo "Added to $TARGET: $PATTERN"
    else
      echo "$TARGET already contains: $PATTERN"
    fi
  else
    echo "$PATTERN" > "$TARGET"
    echo "Created $TARGET and added: $PATTERN"
  fi
}

# zsh aliases and atuin init
ZSH_SNIPPET="# === Added by install-tools.sh: lsd, bat and atuin ===\nif command -v lsd >/dev/null 2>&1; then\n  alias ls='lsd'\nfi\nif command -v bat >/dev/null 2>&1; then\n  alias cat='bat --paging=never --style=plain'\nfi\nif command -v atuin >/dev/null 2>&1; then\n  eval \"\$(atuin init zsh)\"\nfi\n# === End of block ==="

if [[ -f "$ZSHRC" ]]; then
  if ! grep -q "# === Added by install-tools.sh: lsd, bat and atuin ===" "$ZSHRC"; then
    echo -e "\n$ZSH_SNIPPET\n" >> "$ZSHRC"
    echo "zsh configured: aliases and atuin initialization added to $ZSHRC"
  else
    echo "$ZSHRC already contains the lsd/bat/atuin snippet."
  fi
else
  echo -e "$ZSH_SNIPPET" > "$ZSHRC"
  echo "Created $ZSHRC with aliases and atuin initialization."
fi

echo "Configuring fish (if present) under ~/.config/fish/conf.d..."
FISH_CONF_DIR="$HOME/.config/fish/conf.d"
mkdir -p "$FISH_CONF_DIR"
FISH_FILE="$FISH_CONF_DIR/lsd-bat-atuin.fish"
cat > "$FISH_FILE" << 'FISH'
# === Added by install-tools.sh: lsd, bat and atuin ===
if type -q lsd
  alias ls lsd
end
if type -q bat
  alias cat 'bat --paging=never --style=plain'
end
if type -q atuin
  if status --is-interactive
    eval (atuin init fish)
  end
end
# === End of block ===
FISH

LSD_CONFIG_DIR="$HOME/.config/lsd"
mkdir -p "$LSD_CONFIG_DIR"

# Add config.yaml to set theme usage for lsd and link catppuccin colors.yaml
cat > "$LSD_CONFIG_DIR/config.yaml" <<'YAML'
color:
  when: auto
  theme: custom
YAML

if [[ ! -f "$LSD_CONFIG_DIR/colors.yaml" ]]; then
  echo "Installing Catppuccin Mocha colors for lsd: $LSD_CONFIG_DIR/colors.yaml"
  cat > "$LSD_CONFIG_DIR/colors.yaml" <<'COLORS'
user: "#cdd6f4"
group: "#bac2de"
permission:
  read: "#a6e3a1"
  write: "#f9e2af"
  exec: "#a6e3a1"
  exec-sticky: "#74c7ec"
no-access: "#f38ba8"
octal: "#6c7086"
acl: "#94e2d5"
context: "#94e2d5"
date:
  hour-old: "#b4befe"
  day-old: "#bac2de"
  older: "#7f849c"
size:
  none: "#a6adc8"
  small: "#bac2de"
  medium: "#cdd6f4"
  large: "#fab387"
inode:
  valid: "#cba6f7"
  invalid: "#6c7086"
links:
  valid: "#a6e3a1"
  invalid: "#6c7086"
tree-edge: "#6c7086"
git-status:
  default: "#a6adc8"
  unmodified: "#a6adc8"
  ignored: "#585b70"
  new-in-index: "#a6e3a1"
  new-in-workdir: "#a6e3a1"
  typechange: "#f9e2af"
  deleted: "#f38ba8"
  renamed: "#a6e3a1"
  modified: "#f9e2af"
  conflicted: "#f38ba8"

file-types:
  dir: "#89b4fa"
  symlink-file: "#cba6f7"
  symlink-dir: "#cba6f7"
  executable: "#a6e3a1"
  non-executable: "#cdd6f4"
  pipe: "#94e2d5"
  socket: "#94e2d5"
  char-device: "#fab387"
  block-device: "#fab387"
  archive: "#fab387"
  compressed: "#fab387"
  broken-symlink: "#f38ba8"
  unusual: "#eba0ac"
COLORS
else
  echo "$LSD_CONFIG_DIR/colors.yaml already exists. Skipping creation."
fi

echo "lsd theme configured to use Catppuccin Mocha colors in $LSD_CONFIG_DIR/colors.yaml"

echo "Done. Please reload your shell or open a new terminal session to pick up changes."
echo "If you use zsh, run: source $ZSHRC"
exit 0
