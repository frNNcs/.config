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
