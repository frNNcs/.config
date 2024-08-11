# Powerlevel10k
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
    source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi
ZSH_THEME="powerlevel10k/powerlevel10k"
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

CASE_SENSITIVE="false"

plugins=(
    docker
    docker-compose
    git
    nvm
    virtualenv
    zsh-completions
    zsh-autosuggestions
    zsh-syntax-highlighting
    gh
)

# Ohmyzsh plugins and settings
export ZSH="$HOME/.oh-my-zsh"
source $ZSH/oh-my-zsh.sh

# zsh-completions
autoload -U compinit && compinit

# Python version manager
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]]
export PATH="$PYENV_ROOT/bin:$PATH"
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"

# Node Version Manager
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

export PATH="$PATH:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"


test -e "${HOME}/.iterm2_shell_integration.zsh" && source "${HOME}/.iterm2_shell_integration.zsh"


# bun completions
[ -s "/Users/frnn/.bun/_bun" ] && source "/Users/frnn/.bun/_bun"

# bun
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"

# forgit
[ -f $HOMEBREW_PREFIX/share/forgit/forgit.plugin.zsh ] && source $HOMEBREW_PREFIX/share/forgit/forgit.plugin.zsh


# heroku autocomplete setup
HEROKU_AC_ZSH_SETUP_PATH=/Users/frnn/Library/Caches/heroku/autocomplete/zsh_setup && test -f $HEROKU_AC_ZSH_SETUP_PATH && source $HEROKU_AC_ZSH_SETUP_PATH;

# pnpm
export PNPM_HOME="/Users/frnn/Library/pnpm"
case ":$PATH:" in
  *":$PNPM_HOME:"*) ;;
  *) export PATH="$PNPM_HOME:$PATH" ;;
esac
# pnpm end

alias dockerps='docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"'

export PATH="/opt/homebrew/opt/jpeg/bin:$PATH"

# Created by `pipx` on 2024-05-30 15:13:04
export PATH="$PATH:/Users/frnn/.local/bin"
if [ -f "/Users/frnn/.config/fabric/fabric-bootstrap.inc" ]; then . "/Users/frnn/.config/fabric/fabric-bootstrap.inc"; fi