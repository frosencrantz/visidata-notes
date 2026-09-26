# Screenshots for tutorial0102-batch-mode.md
INIT --width 100 --height 16
AWAIT "\$\s*$"
SEND "cd datasets" --enter

# The nested-data flow: open, dive, unfurl, expand.
SEND "vd prizes.json" --enter
AWAIT "1 rows" --start-line -1
SEND "z"
ENTER
AWAIT "682 dicts" --start-line -1
# Move with l, not c: plain cursor movement is not logged (c jumps are).
SEND "lllllll"
AWAIT "laureates +│"
SEND "zM"
AWAIT "1075 rows" --start-line -1
# unfurl-col leaves the cursor on laureates_value.
SEND "z("
AWAIT "depth"
SEND "2" --enter
AWAIT "laureates_value\.id"

# Shift+D: the commands that produced this sheet.
SEND "D"
AWAIT "expand-col-depth"
CAPTURE batch-mode-01-cmdlog --trim

# Batch mode: replay the chapter's flatten-prizes.vdj without the interface.
# pyte has no alternate screen, so the prompt reappears on the last line.
SEND "gq"
AWAIT "^\$ " --start-line -1
SEND "clear" --enter
SEND "vd -b -p flatten-prizes.vdj infile=prizes.json -o - | grep 1972 | cut -f 1,10" --enter
AWAIT "\$\s*$" --timeout 60
CAPTURE batch-mode-02-batch-pipeline --trim
