# Selection Beyond the Basics

The intro tutorial covered the essentials of selecting: s, t, and u on single rows, their g\-prefixed all-row versions, and | to select by regex. (If you ever blank on which key is which, there's a built-in mnemonic: select, toggle, unselect — the actions in alphabetical order, sitting on three neighboring letters.) That was enough when selection mostly meant "highlight some rows."  
This chapter promotes selection to what it really is in VisiData: a query language you operate one keystroke at a time. The nested-data chapter kept surfacing interesting subsets — the unawarded years, the organizational laureates, the shared prizes — and selection is the bridge between *noticing* a subset and *doing something* with it. We'll keep working with the unfurled, expanded Nobel Prize sheet from that chapter.

## First, the verbs: what selection is for

Once rows are selected, three commands do most of the work:

| Keystroke | Command | What it does |
| :---- | :---- | :---- |
| " | dup-selected | Open a new sheet containing only the selected rows |
| gd | delete-selected | Delete the selected rows |
| g= | setcol-expr | Set the current column *for selected rows only* to an expression's result |

" is the one to internalize: select, then dup, and you have a clean sub-sheet to analyze — while the original stays intact one q away. Selection plus " is VisiData's answer to WHERE.  
g= is the quiet powerhouse. "Set this column, but only for the rows I've selected" turns selection into the *scope* of an edit — clean up the misparsed dates in just the 1968 rows, backfill a label on just the rows missing one. If you've ever written df.loc\[mask, "col"\] \= … in pandas, this is that, interactively.  
Note: dup-selected gives the new sheet *references* to the same rows — an edit made on the duplicate is an edit to the underlying data, which is usually what you want. When it isn't — say you're about to experimentally mangle nested values — z" (dup-selected-deep) copies the rows outright, so the original sheet is insulated from your experiments.

## Selecting by expression

Regex selection (|) works on displayed values, and nested cells display as {7} and \[3\] — not much for a regex to grab. What you want is z| (select-expr), which selects by Python expression, with column names available as variables. On the unfurled sheet, try:  
not laureates\_value

The status bar reports 49 rows selected — the unawarded prizes, found in one stroke. Press " to isolate them, or z\\ (unselect-expr) to release them.  
Because select and unselect are separate commands, you can *sculpt* a selection incrementally: select a broad set with one expression, then carve pieces away with z\\, add more with a second z|, and only then act. Nothing commits until you use a verb.  
One member of the basic trio deserves a promotion here: gt, the global toggle, which flips the selection state of every row at once. Its superpower is indirection — sometimes the set you want is awkward to describe, but its *complement* is easy. "Every real laureate row" needs a guarded expression; its complement is just not laureates\_value. Select the easy negative, press gt, and you're holding the 1,026 rows you actually wanted. Once you start looking for it, the describe-the-negative-then-flip move comes up constantly.  
Here's the part that makes expressions and expansion work *together*. Remember from the nested-data chapter that expanding a column hides the parent rather than deleting it — that's why ) can bring it back. A pleasant consequence: hidden parents remain in scope for expressions. On the fully expanded sheet, this selects every organizational laureate:  
laureates\_value and laureates\_value.get("orgName")

31 rows — the Red Cross, the UNHCR, and friends — selected by reaching into the intact parent dictionary, even though the visible sheet shows only the flattened columns. (The laureates\_value and … guard skips the 49 empty rows instead of erroring on them.)

## Selecting by example

Sometimes the row you want more of is right under the cursor, and writing an expression is a detour. The , family selects by *matching what's already there*:

| Keystroke | Command | What it does |
| :---- | :---- | :---- |
| , | select-equal-cell | Select rows matching the current cell's displayed value, in this column |
| g, | select-equal-row | Select rows matching the entire current row's displayed values |
| z, | select-exact-cell | Like ,, but matches the typed value instead of the displayed one |
| gz, | select-exact-row | Row-wise version of z, |

Cursor on any Peace cell in category.en, press ,, and every Peace prize is selected. No expression, no regex, no typing.  
The displayed-vs-typed distinction starts to matter once you've typed your columns. Two cells can display identically but hold different underlying values (a float 1 and an int 1, a date and its string) — or display differently while being equal underneath, thanks to a format string. , matches what you *see*; z, matches what the cell *is*. When a selection comes back with a count that surprises you, this distinction is the first thing to check.

## Commands without keys: meet the longname

Not every command earns a keybinding, and the selection family has some of the best unbound ones. Press Space and type a command's longname to run it. Three worth knowing by name:

* select-error — select every row with an error in any column (select-error-col for just the current column). Remember the red error cells from the first-winner expression in the nested-data chapter? On that sheet, select-error rounds up 74 rows in one move: the 49 unawarded prizes plus 25 whose first-listed laureate is an organization. Errors stop being a nuisance and become a query.  
* select-equal-selected — select every row whose value in the current column appears among the *already-selected* rows. This is a semi-join, and it composes beautifully: select the unawarded rows with z|, put the cursor on awardYear, run select-equal-selected, and now you've grown the selection to *every* prize from a year in which some prize went unawarded — awarded and unawarded alike, ready for comparison.  
* select-random — select a random sample of N rows. The honest way to spot-check a cleaning step on a big sheet: sample, ", eyeball.

## Selection travels between sheets

The most advanced selection trick doesn't add a keystroke — it changes where you press the ones you know. Summary sheets aren't just for reading; they're control panels for selecting on the sheet below.

* On a frequency table (Shift+F), s on a bin selects that bin's underlying source rows. Want all the Physics and Chemistry laureate-rows selected? Frequency on category.en, s on two rows, q back — done.  
* The Describe sheet (Shift+I) goes further: put the cursor on any summary cell — say, the errors count for a column, or its nulls — and z s selects exactly those rows back on the source sheet.

This inverts the usual flow. Instead of "scroll the data looking for problems," it's "read the summary, select the problem from above, dive down to the culprits already highlighted." On a million-row sheet, that inversion is the difference between minutes and seconds.

## Try it

On the unfurled, expanded Nobel sheet:

1. The lost years. Select the rows with an empty laureates\_value using z|, isolate them with ", and build a frequency table on category.en. Which category was skipped most often? (Then try awardYear — the two World Wars are unmistakable.)  
2. Organizations only. Select the 31 organizational laureates via the hidden-parent expression above, " them into their own sheet, and sort by awardYear. What's the earliest organization to win?  
3. Semi-join. Using select-equal-selected as sketched above, build the sheet of all prizes from years with at least one unawarded prize. Frequency-table it by category: which categories *kept* being awarded during the war years?  
4. Spot-check. select-random 20 rows, ", and audit your knownName/orgName columns by eye. Sampling before trusting is a habit worth practicing even when — especially when — everything looks fine.
