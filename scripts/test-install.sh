#!/usr/bin/env bash
# Simple tests to validate configuration
set -euo pipefail

errors=0

check_cmd() {
  cmd="$1"
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "OK: $cmd present"
  else
    echo "MISSING: $cmd not found in PATH"
    errors=$((errors+1))
  fi
}

check_cmd lsd
check_cmd bat
check_cmd atuin

# Check zshrc snippet
if grep -q "# === Added by install-tools.sh: lsd, bat and atuin ===" "$HOME/.zshrc"; then
  echo "OK: zshrc snippet found"
else
  echo "MISSING: zshrc lines not found. Run ./install-tools.sh or add the block manually."
  errors=$((errors+1))
fi

# Optional: fish conf
if [[ -f "$HOME/.config/fish/conf.d/lsd-bat-atuin.fish" ]]; then
  echo "OK: fish conf.d present"
else
  echo "MISSING: fish conf file not present"
fi

# Check lsd color theme
if [[ -f "$HOME/.config/lsd/colors.yaml" ]]; then
  echo "OK: lsd colors.yaml present"
else
  echo "MISSING: ~/.config/lsd/colors.yaml - run ./install-tools.sh to create it"
  errors=$((errors+1))
fi

if [[ -f "$HOME/.config/lsd/config.yaml" ]]; then
  echo "OK: lsd config.yaml present"
else
  echo "MISSING: ~/.config/lsd/config.yaml - run ./install-tools.sh to create it"
  errors=$((errors+1))
fi

if ((errors > 0)); then
  echo "$errors checks failed"
  exit 1
fi

echo "All done — basic checks passed."
