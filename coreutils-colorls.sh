# color-ls initialization
if [ -z "$LS_COLORS" ]; then
  #do not override user LS_COLORS, so perform only for zero sized LS_COLORS
  alias ll='ls -l' 2>/dev/null
  alias l.='ls -d .*' 2>/dev/null

  COLORS=/etc/DIR_COLORS
  [ -e "/etc/DIR_COLORS.$TERM" ] && COLORS="/etc/DIR_COLORS.$TERM"
  [ -e "/etc/DIR_COLORS.256color" ] && \
     [ "`tput colors 2>/dev/null`" == "256" ] && \
     COLORS="/etc/DIR_COLORS.256color"
  [ -e "$HOME/.dircolors" ] && COLORS="$HOME/.dircolors"
  [ -e "$HOME/.dir_colors" ] && COLORS="$HOME/.dir_colors"
  [ -e "$HOME/.dircolors.$TERM" ] && COLORS="$HOME/.dircolors.$TERM"
  [ -e "$HOME/.dir_colors.$TERM" ] && COLORS="$HOME/.dir_colors.$TERM"
  [ -e "$COLORS" ] || return

  eval `dircolors --sh "$COLORS" 2>/dev/null`
  [ -z "$LS_COLORS" ] && return
  egrep -qi "^COLOR.*none" $COLORS >/dev/null 2>/dev/null && return
fi

alias ll='ls -l --color=tty' 2>/dev/null
alias l.='ls -d .* --color=tty' 2>/dev/null
alias ls='ls --color=tty' 2>/dev/null
