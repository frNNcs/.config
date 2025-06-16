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
