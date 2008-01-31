#! /bin/csh -f
# color-ls initialization
if ( "$LS_COLORS" != '' ) then
   #do not override user specified LS_COLORS and use them
   alias ll 'ls -l --color=tty'
   alias l. 'ls -d .* --color=tty'
   alias ls 'ls --color=tty'
   exit
endif

alias ll 'ls -l'
alias l. 'ls -d .*'

set COLORS=/etc/DIR_COLORS
if ($?TERM) then
    if ( -e "/etc/DIR_COLORS.$TERM" ) then 
       set COLORS="/etc/DIR_COLORS.$TERM"
    endif
endif
if ( -f ~/.dircolors ) then 
   set COLORS=~/.dircolors
endif
if ( -f ~/.dir_colors ) then 
   set COLORS=~/.dir_colors
endif
if ($?TERM) then
    if ( -f ~/.dircolors."$TERM" ) then 
       set COLORS=~/.dircolors."$TERM"
    endif
    if ( -f ~/.dir_colors."$TERM" ) then 
       set COLORS=~/.dir_colors."$TERM"
    endif
endif

if ( ! -e "$COLORS" ) then 
   exit
endif

eval `dircolors -c $COLORS`

if ( "$LS_COLORS" == '' ) then
   exit
endif

set color_none=`sed -n '/^COLOR.*none/Ip' < $COLORS`
if ( "$color_none" == '' ) then
   alias ll 'ls -l --color=tty'
   alias l. 'ls -d .* --color=tty'
   alias ls 'ls --color=tty'
endif
unset color_none
