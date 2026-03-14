#!/bin/bash
# Unified Terminal UI Design: pane_apps.sh
# Determines icon based on active process using Rosé Pine colors

# Rosé Pine Palette
IRIS='#c4a7e7'
LOVE='#eb6f92'
FOAM='#9ccfd8'

# Symbols
VIM_ICON=''
GIT_ICON='󰊢'
TERM_ICON=''

# Get current command
cmd=$(tmux display-message -p "#{pane_current_command}")

case "$cmd" in
    *vim*|*nvim*)
        echo "#[fg=$IRIS]$VIM_ICON #[fg=default]$cmd"
        ;;
    *git*)
        echo "#[fg=$LOVE]$GIT_ICON #[fg=default]$cmd"
        ;;
    *)
        echo "#[fg=$FOAM]$TERM_ICON #[fg=default]$cmd"
        ;;
esac
