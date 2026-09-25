# If not running interactively, don't do anything
[[ $- != *i* ]] && return
export BAT_THEME=tokyonight_night
source ~/.local/share/tokyonight/extras/fzf/tokyonight_night.sh

alias ls='eza -la --color=always --icons=auto'
alias vi='nvim'
alias vim='nvim'
alias cat='bat'
alias grep='grep --color=auto'
PS1='\[\e[38;5;189m\]\u\[\e[0m\] \[\e[38;5;189m\]in\[\e[0m\] \[\e[38;5;210m\]\W\[\e[0m\] \[\e[38;5;188m\]\\$\[\e[0m\] '
fastfetch -c /examples/13
