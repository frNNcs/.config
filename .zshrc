# Powerlevel10k
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
    source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi
ZSH_THEME="powerlevel10k/powerlevel10k"
[[ ! -f ~/.config/.p10k.zsh ]] || source ~/.config/.p10k.zsh

CASE_SENSITIVE="false"

plugins=(
    docker
    docker-compose
    git
    nvm
    virtualenv
    zsh-completions
    zsh-autosuggestions
    # zsh-syntax-highlighting
    gh
)

# Ohmyzsh plugins and settings
export ZSH="$HOME/.oh-my-zsh"
typeset -g POWERLEVEL9K_INSTANT_PROMPT=quiet
source $ZSH/oh-my-zsh.sh

# zsh-completions
autoload -U compinit && compinit
source /opt/homebrew/share/powerlevel10k/powerlevel10k.zsh-theme

# Python version manager
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]]
export PATH="$PYENV_ROOT/bin:$PATH"
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
export PATH="/opt/homebrew/opt/node@22/bin:$PATH"

. "$HOME/.local/bin/env"
alias spicetify-fix="~/.config/spicetify/auto-apply.sh"
export PATH="$HOME/economia-funciones-env/bin:$PATH"

# bun completions
[ -s "/Users/francisco/.bun/_bun" ] && source "/Users/francisco/.bun/_bun"

# bun
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

# Added by Antigravity
export PATH="/Users/francisco/.antigravity/antigravity/bin:$PATH"

# Aliases and Atuin initialization
# === Added by install-tools.sh: lsd, bat and atuin ===
if command -v lsd >/dev/null 2>&1; then
    alias ls='lsd'
fi
if command -v bat >/dev/null 2>&1; then
    alias cat='bat --paging=never --style=plain'
fi
if command -v atuin >/dev/null 2>&1;
    eval "$(atuin init zsh)"
fi
# === End of block ===
# === Catppuccin Mocha LS_COLORS ===
export LS_COLORS="di=38;2;137;180;250:ex=38;2;166;227;161:ln=38;2;203;166;247:ln=38;2;203;166;247:pi=38;2;148;226;213:so=38;2;148;226;213:cd=38;2;250;179;135:bd=38;2;250;179;135:or=38;2;243;139;168:no=38;2;235;160;172:di=1;36:ln=35:so=32:pi=33:ex=31:bd=34;46:cd=34;43:su=30;41:sg=30;46:tw=30;42:ow=30;43"
# === End Catppuccin LS_COLORS ===
export PATH="$HOME/bin:$PATH"

# Homebrew names the binary `fabric-ai`. Provide a compatibility alias so `fabric` works as in the docs.
if command -v fabric-ai >/dev/null 2>&1;
    alias fabric='fabric-ai'
fi

# Simple telos alias: prints TELOS.md so it can be piped into commands
# Example: telos | fabric -p t_red_team_thinking
TELOS_PATH="$HOME/projects/homelab/DATA/syncthing/obsidian/003 Resources/TELOS/TELOS.md"
if [ -f "$TELOS_PATH" ]; then
    alias telos="cat \"$TELOS_PATH\""
fi

# Configuración para usar Ollama en servidor remoto
# Apunta al servidor Ollama en 192.168.1.80 según https://github.com/ollama/ollama/issues/2941
export OLLAMA_HOST="http://192.168.1.80:11434"
# Para clientes OpenAI-compatible que usan la variable OPENAI_API_BASE
export OPENAI_API_BASE="http://192.168.1.80:11434/v1"

# opencode
export PATH=/Users/francisco/.opencode/bin:$PATH

# === TMUX Configuration & Auto-start ===
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
export TMUX_CONFIG="$XDG_CONFIG_HOME/tmux/tmux.conf"
alias tmux="tmux -f $TMUX_CONFIG"

# Auto-start tmux if not already inside one, and if it's an interactive shell
if [[ -z "$TMUX" ]] && [[ -n "$PS1" ]]; then
    # Try to attach to session 'main', or create it if it doesn't exist
    tmux -f "$TMUX_CONFIG" attach-session -t main 2>/dev/null || \
    tmux -f "$TMUX_CONFIG" new-session -s main
fi