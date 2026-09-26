# Minimal, deterministic shell for screenshot capture (see scripts/termscript.py).
export LANG=C.UTF-8
export LC_ALL=C.UTF-8
export TZ=UTC
export TERM=xterm-256color
export NCURSES_NO_UTF8_ACS=1
export PROMPT_COMMAND=""
export PS1="\[\033[38;5;37m\]\$\[\033[00m\] "
unset HISTFILE

SCRIPT_DIR=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
# termscript.py points HOME at a throwaway directory, so VisiData's own state
# (~/.visidata, ~/.local/share/visidata) never leaks between runs.
alias vd="vd --config $SCRIPT_DIR/visidatarc.py"
