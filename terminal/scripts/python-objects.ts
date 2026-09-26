# Screenshots for tutorial0102-python-objects.md
INIT --width 100 --height 16
AWAIT "\$\s*$"
SEND "cd datasets" --enter
SEND "vd prizes.json" --enter
AWAIT "1 rows" --start-line -1

# g Ctrl+X: import statistics, as the chapter suggests when Python complains.
SEND "g\x18"
AWAIT "import"
SEND "statistics" --enter

# Ctrl+X: open the result of a Python expression as a sheet.
SEND "\x18"
AWAIT "expr"
SEND "{\"mean\": statistics.mean([1, 2, 3]), \"tags\": [\"a\", \"b\"]}" --enter
AWAIT "tags"
CAPTURE python-objects-01-pyobj-expr --trim

# z Ctrl+Y on a category cell: the raw dictionary as a key/value sheet.
SEND "q"
SEND "z"
ENTER
AWAIT "682 dicts" --start-line -1
SEND "l"
SEND "z\x19"
AWAIT "Kjemi"
CAPTURE python-objects-02-pyobj-cell --trim
