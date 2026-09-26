# Screenshots for tutorial0102-nested-data.md
INIT --width 100 --height 16
AWAIT "\$\s*$"
SEND "cd datasets" --enter
SEND "vd prizes.json" --enter
AWAIT "1 rows" --start-line -1
# Any keystroke clears the startup messages; Ctrl+L (redraw) changes nothing else.
SEND "\x0c"
CAPTURE nested-data-00-envelope --trim

# Dive into the nobelPrizes cell (cursor starts on that column).
SEND "z"
ENTER
AWAIT "682 dicts" --start-line -1
CAPTURE nested-data-01-open-cell

# Expand the category dictionary.
SEND "c^category$"
ENTER
SEND "("
AWAIT "category\.se"
CAPTURE nested-data-02-expand-category

# The trap: expanding a list column gives one column per position.
SEND "c^laureates$"
ENTER
SEND "("
AWAIT "laureates\[0\]"
# Step right so all three positional columns are on screen.
SEND "ll"
AWAIT "laureates\[2\]"
CAPTURE nested-data-03-expand-list

# Contract it again, then unfurl: one row per laureate.
SEND ")"
# contract-col leaves the cursor on a hidden column; jump back to laureates.
SEND "c^laureates$"
ENTER
AWAIT "laureates +│"
SEND "zM"
AWAIT "1075 rows" --start-line -1
# Walk right from the first column, so the new laureates_key/laureates_value
# columns end up on screen next to the prize columns they were unfurled from.
SEND "gh"
SEND "llllllllll"
AWAIT "laureates_key +│ laureates_value"
CAPTURE nested-data-04-unfurl

# Expand each laureate's dictionary two levels deep.
SEND "c^laureates_value$"
ENTER
SEND "z("
AWAIT "depth"
SEND "2" --enter
AWAIT "laureates_value\.id"
# Scroll so the new columns fill the screen: go far right, then jump back.
SEND "gl"
SEND "c^laureates_value.id$"
ENTER
AWAIT "laureates_value\.id +│ laureates_value\.kn"
CAPTURE nested-data-05-expand-depth-2

# Back on the 682-row sheet, pluck one value out with an expression.
SEND "q"
AWAIT "682 dicts" --start-line -1
# = adds the new column right after the cursor; start from awardYear so
# the year is visible next to the result.
SEND "gh"
SEND "="
AWAIT "expr"
SEND "laureates[0][\"knownName\"][\"en\"]" --enter
AWAIT "laureates\[0\]\[\"knownName\"\]"
# Scroll to the First World War years: unawarded prizes and the Red Cross
# (an organization, so no knownName) both show up as errors.
SEND "zr"
SEND "84" --enter
AWAIT "1917"
CAPTURE nested-data-06-expression-errors
