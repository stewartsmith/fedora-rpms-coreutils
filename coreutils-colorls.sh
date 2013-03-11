# color-ls initialization

#when USER_LS_COLORS defined do not override user LS_COLORS, but use them.
if [ -z "$USER_LS_COLORS" ]; then

  alias ll='ls -l' 2>/dev/null
  alias l.='ls -d .*' 2>/dev/null


  # Skip the rest for noninteractive shells.
  [ -z "$PS1" ] && return

  INCLUDE=
  COLORS=
  TMP="`mktemp .colorlsXXX`"

  for colors in "$HOME/.dir_colors.$TERM" "$HOME/.dircolors.$TERM" \
      "$HOME/.dir_colors" "$HOME/.dircolors"; do
    [ -e "$colors" ] && COLORS="$colors" && \
    INCLUDE="`cat "$COLORS" | grep '^INCLUDE' | cut -d ' ' -f2-`" && \
    break
  done

  [ -z "$COLORS" ] && [ -e "/etc/DIR_COLORS.256color" ] && \
      [ "x`tty -s && tput colors 2>/dev/null`" = "x256" ] && \
      COLORS="/etc/DIR_COLORS.256color"

  if [ -z "$COLORS" ]; then
    for colors in "/etc/DIR_COLORS.$TERM" "/etc/DIR_COLORS" ; do
      [ -e "$colors" ] && COLORS="$colors" && break
    done
  fi

  # Existence of $COLORS already checked above.
  [ -n "$COLORS" ] || return

  [ -e "$INCLUDE" ] && cat "$INCLUDE" > $TMP
  cat "$COLORS" | grep -v '^INCLUDE' >> $TMP

  eval "`dircolors --sh $TMP 2>/dev/null`"
  [ -z "$LS_COLORS" ] && return
  grep -qi "^COLOR.*none" $COLORS >/dev/null 2>/dev/null && return
  rm -f $TMP
fi

alias ll='ls -l --color=auto' 2>/dev/null
alias l.='ls -d .* --color=auto' 2>/dev/null
alias ls='ls --color=auto' 2>/dev/null
