# Screenshots for tutorial0102-selection.md
INIT --width 100 --height 16
AWAIT "\$\s*$"
SEND "cd datasets" --enter
SEND "vd prizes.json" --enter
AWAIT "1 rows" --start-line -1

# Setup: the unfurled, expanded sheet from the nested-data chapter.
SEND "z"
ENTER
AWAIT "682 dicts" --start-line -1
SEND "c^category$"
ENTER
SEND "("
AWAIT "category\.en"
SEND "c^laureates$"
ENTER
SEND "zM"
AWAIT "1075 rows" --start-line -1
SEND "c^laureates_value$"
ENTER
SEND "z("
AWAIT "depth"
SEND "2" --enter
AWAIT "laureates_value\.id"
SEND "gh"

# Select the unawarded prizes by expression.
SEND "z|"
AWAIT "expr"
SEND "not laureates_value" --enter
AWAIT "•49 " --start-line -1
# Scroll to the First World War years, where the selected rows are.
SEND "zr"
SEND "91" --enter
AWAIT "1916"
CAPTURE selection-01-select-expr

# " opens the selected rows as their own sheet.
SEND "\""
AWAIT "49 rows" --start-line -1
CAPTURE selection-02-dup-selected
SEND "q"

# gt flips the selection: every real laureate row.
SEND "gt"
AWAIT "•1026 " --start-line -1
SEND "gu"

# Organizational laureates, found through the hidden parent dictionary.
SEND "z|"
AWAIT "expr"
SEND "laureates_value and laureates_value.get(\"orgName\")" --enter
AWAIT "•31 " --start-line -1
# Open them as their own sheet and look at the organization names.
SEND "\""
AWAIT "31 rows" --start-line -1
SEND "gl"
SEND "c^laureates_value.orgName.en$"
ENTER
# _ widens the column to fit the full names.
SEND "_"
AWAIT "Institute of International Law"
CAPTURE selection-03-select-orgs
SEND "q"
SEND "gu"

# Select by example: , on a Peace cell.
# category.en is the column right after awardYear.
SEND "gh"
SEND "l"
SEND "gg"
SEND "jj"
SEND ","
AWAIT "•162 " --start-line -1
CAPTURE selection-04-select-equal-cell
SEND "gu"

# The frequency sheet as a control panel: select Physics and Chemistry
# (s also moves the cursor down a row), then go back.
SEND "F"
AWAIT "6 bins" --start-line -1
SEND "gg"
SEND "j"
SEND "s"
SEND "s"
AWAIT "•2 " --start-line -1
PAUSE 0.5
CAPTURE selection-05-freq-select --trim
SEND "q"
AWAIT "•444 " --start-line -1
CAPTURE selection-06-freq-selected-source

# select-error on the 682-row sheet with the first-winner expression.
SEND "q"
AWAIT "682 dicts" --start-line -1
SEND "gh"
SEND "="
AWAIT "expr"
SEND "laureates[0][\"knownName\"][\"en\"]" --enter
AWAIT "laureates\[0\]\[\"knownName\"\]"
SEND " "
AWAIT "exec"
SEND "select-error" --enter
AWAIT "•74 " --start-line -1
SEND "zr"
SEND "84" --enter
AWAIT "1917"
CAPTURE selection-07-select-error
