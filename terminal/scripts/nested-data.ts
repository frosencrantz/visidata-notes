# Screenshots for tutorial0102-nested-data.md
INIT --width 100 --height 24
AWAIT "\$\s*$"
SEND "cd datasets" --enter
SEND "vd prizes.json" --enter
AWAIT "1 row" --start-line -1
# Any keystroke clears the startup messages; Ctrl+L (redraw) changes nothing else.
SEND "\x0c"
CAPTURE nested-data-00-envelope --trim
