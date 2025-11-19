#!/usr/bin/env bash
set -euo pipefail

LS_COLORS_SCRIPT_NAME="apply-catppuccin-lscolors.sh"
LS_COLORS_BACKUP_SUFFIX=".bak-$(date +%s)"

DEFAULT_CONFIG="$HOME/.config/lsd/colors.yaml"
if [[ ! -f "$DEFAULT_CONFIG" ]]; then
  echo "No colors.yaml found at $DEFAULT_CONFIG"
  echo "Run install-tools.sh or create $DEFAULT_CONFIG first"
  exit 2
fi

hex2rgb() {
  local hex="$1"
  hex="${hex#\#}" # strip leading # if present
  printf '%d %d %d' "0x${hex:0:2}" "0x${hex:2:2}" "0x${hex:4:2}"
}

get_yaml_value(){
  # usage: get_yaml_value <yaml-file> <key-path>
  # key-path supports simple dotted keys like "file-types.dir"
  local yaml="$1" keypath="$2"
  # We'll search by the final key component (e.g. 'dir' from 'file-types.dir')
  local ykey="${keypath##*.}"
  local val
  val=$(grep -E "^[[:space:]]*${ykey}:[[:space:]]*\"?#?[0-9A-Fa-f]{6}\"?" "$yaml" -m 1 || true)
  if [[ -z "$val" ]]; then
    echo ""
    return
  fi
  # Extract hex
  echo "$val" | sed -E 's/^[[:space:]]*[^:]+:[[:space:]]*"?(#?[0-9A-Fa-f]{6})"?.*/\1/'
}

# Use a simple list of mappings: "yaml.key:ls_key"
MAPPINGS=(
  "file-types.dir:di"
  "file-types.executable:ex"
  "file-types.symlink-file:ln"
  "file-types.symlink-dir:ln"
  "file-types.pipe:pi"
  "file-types.socket:so"
  "file-types.char-device:cd"
  "file-types.block-device:bd"
  "file-types.broken-symlink:or"
  "file-types.unusual:no"
)

LS_PAIRS=()
for mapping in "${MAPPINGS[@]}"; do
  yaml_key="${mapping%%:*}"
  ls_key="${mapping##*:}"
  val="$(get_yaml_value "$DEFAULT_CONFIG" "$yaml_key")"
  if [[ -n "$val" ]]; then
    rgb=$(hex2rgb "$val")
    # read into r g b
    r=$(echo $rgb | awk '{print $1}')
    g=$(echo $rgb | awk '{print $2}')
    b=$(echo $rgb | awk '{print $3}')
    LS_PAIRS+=("${ls_key}=38;2;${r};${g};${b}")
  fi
done

NEW_LS_COLORS=""
if (( ${#LS_PAIRS[@]} > 0 )); then
  NEW_LS_COLORS=$(IFS=':'; echo "${LS_PAIRS[*]}")
fi

usage(){
  cat <<EOF
Usage: $LS_COLORS_SCRIPT_NAME [--apply]

Generates an LS_COLORS string from ~/.config/lsd/colors.yaml (Catppuccin Mocha) and prints it.
If --apply is set, appends a safe export of LS_COLORS to ~/.zshrc (backup created).
EOF
}

if [[ ${#@} -gt 0 && "$1" == "--help" ]]; then
  usage
  exit 0
fi

if [[ -z "$NEW_LS_COLORS" ]]; then
  echo "No mappings found in $DEFAULT_CONFIG. Nothing to generate."
  exit 0
fi

echo "Generated LS_COLORS fragment from $DEFAULT_CONFIG:"
echo
echo "$NEW_LS_COLORS"
echo

if [[ ${#@} -gt 0 && "$1" == "--apply" ]]; then
  ZSHRC="$HOME/.zshrc"
  BACKUP="$ZSHRC$LS_COLORS_BACKUP_SUFFIX"
  echo "Backing up $ZSHRC to $BACKUP"
  cp -f "$ZSHRC" "$BACKUP" || true
  # Remove any previous catppuccin LS_COLORS block
  if grep -q "# === Catppuccin Mocha LS_COLORS ===" "$ZSHRC"; then
    awk 'BEGIN{skip=0} /# === Catppuccin Mocha LS_COLORS ===/{skip=1; next} /# === End Catppuccin LS_COLORS ===/{skip=0; next} !skip{print $0}' "$ZSHRC" > "$ZSHRC.tmp" && mv "$ZSHRC.tmp" "$ZSHRC"
  fi
  # Append new block
  cat >> "$ZSHRC" <<EOF
# === Catppuccin Mocha LS_COLORS ===
export LS_COLORS="${NEW_LS_COLORS}${LS_COLORS:+:${LS_COLORS}}"
# === End Catppuccin LS_COLORS ===
EOF
  echo "Appended catppuccin LS_COLORS to $ZSHRC";
  echo "You can reload with: source $ZSHRC";
fi

exit 0
