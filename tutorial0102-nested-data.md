# Working With Nested Data

Every dataset in this tutorial so far has been a table: rows and columns, one value per cell. But a lot of modern data — especially data from web APIs — doesn't arrive that way. It arrives as JSON, where a "cell" might contain an entire dictionary of values, or a list of dictionaries, nested several levels deep.  
The good news: VisiData is *unusually* good at this. In this chapter, we'll use a family of commands — open-cell, expand-col, contract-col, and unfurl-col — to navigate, flatten, and reshape nested data without leaving the terminal, and without writing a parsing script.  
We'll work through a JSON dataset, but keep a secret in mind as you go: none of these commands actually know anything about JSON. They operate on *Python objects* — a fact we'll cash in properly in the next chapter.

## The data: every Nobel Prize ever awarded

The Nobel Foundation publishes a free, no-registration-required API. One command downloads every prize since 1901:  
curl "https://api.nobelprize.org/2.1/nobelPrizes?limit=1000" \> prizes.json

This gets you 682 prizes as of mid-2026 — about 770 KB of JSON. It's a great teaching dataset because a single prize record contains every kind of nesting you'll meet in the wild:

* Plain values, like awardYear and prizeAmount  
* Dictionaries, like category, which holds translations: {"en": "Chemistry", "no": "Kjemi", "se": "Kemi"}  
* Lists of dictionaries, like laureates — one entry per winner, and each winner is itself a nested structure

And, like almost every real API response, the records you actually want are wrapped inside an "envelope" of metadata. Let's start there.

## Opening JSON files

Open the file the usual way:  
vd prizes.json

You might expect 682 rows. Instead, you'll see a sheet with one row and three columns: nobelPrizes, meta, and links.  
That single row *is* the top level of the JSON file. The API wrapped our prizes in an envelope: meta holds paging information, links holds navigation URLs, and nobelPrizes holds the list we care about.  
Look closely at how VisiData displays the cells. The nobelPrizes cell reads \[682\], and the meta cell reads something like {7}. This notation is worth memorizing, because it tells you which command to reach for later:

| Cell display | Meaning |
| :---- | :---- |
| \[682\] | A list containing 682 items |
| {7} offset=0 limit=1000 … | A dictionary with 7 keys (with a preview of its contents) |

Note: This chapter uses a .json file, but everything in it applies equally to .jsonl / .ndjson files (one JSON record per line, common for logs and data dumps). Those skip the envelope problem entirely — each line becomes a row — but their cells can still contain dictionaries and lists.

## Diving into a cell

We want the 682 records inside that \[682\] cell. Move the cursor to the nobelPrizes column and press z Enter (the command is called open-cell).  
VisiData opens the contents of that one cell as a brand-new sheet: 682 rows, one per prize, with columns awardYear, category, categoryFullName, dateAwarded, prizeAmount, prizeAmountAdjusted, links, laureates, and topMotivation.  
This is the general pattern for API responses: open the file, look at the envelope, and dive into the cell that holds the actual records. As always, q closes the current sheet and takes you back up a level — you can dive in and out freely without changing anything.  
Note: Enter by itself (open-row) dives into the entire current *row* rather than one cell. On a one-row envelope sheet like this one, either works — but open-cell says exactly what you mean, so it's the habit worth building.  
Before moving on, take stock of the new sheet with the notation you just learned. awardYear, dateAwarded, and the two prize-amount columns are plain values — you could set their types right now (\# for the amounts, @ for the date) just as you did in the earlier chapters. But category shows {3}, links shows \[1\], and laureates shows \[1\], \[2\], or \[3\] depending on the row. Those need flattening before they'll sort, filter, or aggregate.

## Expanding dictionary columns

Move the cursor to the category column. Every cell is a three-key dictionary of translations. Press ( (expand-col).  
The category column disappears, replaced by three new columns:  
category.en    category.no    category.se  
Chemistry      Kjemi          Kemi  
Literature     Litteratur     Litteratur  
…

Each key became a column, named with a dot: parent.key. These are ordinary columns now — you can sort by category.en, build a frequency table on it with Shift+F, whatever you like.  
Now press ) (contract-col) with the cursor on any of the three: the dotted columns collapse back into the original category column. Expansion is completely reversible, and nothing you do here touches the file on disk. This is worth internalizing early — you can expand, look around, and contract with no consequences, so explore freely.  
Two variants handle the "lots of columns at once" cases:

| Keystroke | Command | What it does |
| :---- | :---- | :---- |
| ( | expand-col | Expand current column, one level |
| g( | expand-cols | Expand *all* visible columns, one level |
| z( | expand-col-depth | Expand current column to a depth you specify (0 \= fully) |
| gz( | expand-cols-depth | Expand all visible columns to a depth you specify |
| ) | contract-col | Collapse the current column back into its parent |
| g) | contract-cols | Collapse all expanded columns one level |

Try g( on this sheet, just to see it. It works — but notice how much noise appears: links\[0\].rel, links\[0\].href, translation columns you'll never use. Press g) (a few times, if needed) to put things back. Full expansion is rarely what you want; the craft is expanding *only* the columns your question needs. (And for the columns you do expand: the ones you don't need, you already know how to hide with \-.)

## Lists are different — and here's the trap

So far so good: dictionaries expand into columns naturally, because every row has the same keys. Now let's try the same move on a list column and watch it go wrong.  
Put the cursor on laureates and press (.  
You get three new columns: laureates\[0\], laureates\[1\], and laureates\[2\] — the first, second, and third entries of each row's list, by *position*. Scroll around. Since 362 prizes went to a single winner, laureates\[1\] and laureates\[2\] are mostly empty. And every cell that isn't empty is still an unexpanded {7} dictionary.  
Think about what you'd have to do to answer a question as simple as *"list every laureate's name"*: expand all three positional columns, then somehow combine laureates\[0\].knownName, laureates\[1\].knownName, and laureates\[2\].knownName into one. The shape is fighting you.  
The problem isn't VisiData — it's that we asked for the wrong reshaping. A dictionary's keys want to become columns. A list's items want to become rows. A prize with three winners shouldn't be one row with three column-families; it should be three rows.  
Press ) to contract the list back, and let's do it properly.

## Unfurling: one row per list item

With the cursor on laureates, press z Shift+M (unfurl-col).  
VisiData opens a new sheet — note the \_unfurled suffix in the sheet name — with 1,075 rows. Each prize row has been repeated once per laureate: the 1901 Chemistry prize (one winner) is still one row, while the 2025 Physics prize (three winners) is now three rows, each carrying identical values for awardYear, category, prizeAmount, and the other prize-level columns.  
The laureates column is gone, replaced by two new ones:

* laureates\_value — the individual list item (here, one laureate's {7} dictionary)  
* laureates\_key — that item's position in its original list (0, 1, 2\)

If you've used pandas, this is explode; in SQL it's closest to UNNEST. But there's a subtlety worth doing the arithmetic for. Those 682 prizes contain 1,026 laureates total — so where do 1,075 rows come from?  
49 prizes were never actually awarded — mostly during the two World Wars, when categories like Peace were suspended. Their records have no laureates at all. Unfurl keeps them: each becomes a single row with an empty laureates\_value. That's 1,026 \+ 49 \= 1,075.  
This is a deliberate kindness. A reshaping that silently dropped 49 rows would be a subtle data-integrity bug waiting to happen. If your analysis is about laureates, select the empty rows and delete them — but VisiData makes that *your* explicit decision, not a side effect. (The selection chapter turns exactly this into a two-keystroke move.)  
Note: Unfurl also works on a column of dictionaries — you'd get one row per key, with the key in \_key and the value in \_value. That's occasionally exactly what you want, for instance when a "dictionary" is really a lookup table in disguise (say, a medals cell like {"gold": 3, "silver": 1} that you want as one row per medal type).

## Putting it together

Now finish the job. On the unfurled sheet, put the cursor on laureates\_value and press z(, then enter a depth of 2.  
Each laureate dictionary blooms into ordinary, analysis-ready columns:  
laureates\_value.id  
laureates\_value.knownName.en  
laureates\_value.fullName.en  
laureates\_value.portion  
laureates\_value.sortOrder  
laureates\_value.motivation.en  
laureates\_value.orgName.en  
laureates\_value.acronym  
…

(Depth 2, because fields like knownName are themselves dictionaries of translations — one level would leave {1} cells behind. If you'd rather not guess the depth, z( with 0 expands fully; it just brings some extra translation columns along.)  
Notice something curious: there's both a knownName.en column and an orgName.en column, and no row fills in both. That's because Peace Prizes can go to *organizations* — the Red Cross, the UN — whose records have orgName and acronym where a person's record has knownName. When VisiData expands a column, it takes the union of every row's keys, so both varieties get columns, and each row simply leaves blank the ones it doesn't have. An empty cell after an expansion doesn't mean missing data — it can just mean "this row's dictionary doesn't have that key." Real-world JSON does this constantly, and now you'll recognize it on sight.  
From here, everything you know from the earlier chapters applies, because this is now just a table. Two quick payoffs:

1. Shared prizes over time. The laureates\_value.portion column holds each winner's share — 1, 1/2, 1/3, 1/4. Build a frequency table on it with Shift+F and you can see, instantly, how often prizes are split.  
2. Rename as you go. Column names like laureates\_value.knownName.en are precise but clunky. The renaming and hiding skills from the Columns-sheet chapter are how you turn a freshly flattened sheet into something pleasant to work with.

## When you only want one value: skip the reshaping

Expanding and unfurling restructure the whole sheet. Sometimes that's overkill — you want a single nested value pulled out, and nothing else moved. Column expressions from the earlier chapters reach *into* nesting just fine, because each cell is a live Python object.  
Back on the 682-row prizes sheet, press \= and enter:  
laureates\[0\]\["knownName"\]\["en"\]

You get a new column holding each prize's first-listed winner, with everything else untouched.  
You'll also see red error cells — and by now you can predict exactly which rows they are. The 49 unawarded prizes have no laureates list, so laureates\[0\] fails; organizational laureates have no knownName, so those fail too. The errors aren't a mess to clean up; they're the same information the empty cells carried above, and Python's conditional expressions can absorb them whenever you want a tidier column:  
laureates\[0\]\["knownName"\]\["en"\] if laureates else None

(Or leave the errors in place and round them up with select-error, covered in the selection chapter — sometimes the error rows *are* the interesting ones.)  
Rule of thumb: expand/unfurl when the nested data *is* the analysis; use an expression when you just need to pluck a value out.

## Saving nested sheets

Save the unfurled, expanded sheet with Ctrl+S, as usual. The format you choose decides what happens to the structure:

* .csv / .tsv — a flattened snapshot. Dotted column names become ordinary headers; any still-unexpanded {…}/\[…\] cells are stringified. Perfect for handing off to a spreadsheet or a colleague.  
* .json / .jsonl — columns whose cells still hold dictionaries or lists are written back as real nested JSON, not strings. Handy when the output feeds another program that expects structure.

One caveat worth knowing: saving is a one-way flattening of whatever the sheet looks like *now*. Expanded columns stay expanded in the output; contract first if you want the original shape back.

## Try it

Using prizes.json:

1. Warm-up. Dive into the envelope, expand category, and build a frequency table (Shift+F) on category.en. Which category has the most prizes? (Careful — is Economic Sciences what you expected? It started in 1969.)  
2. Solo vs. shared. Unfurl, expand, and use laureates\_value.portion to answer: has splitting the prize become more common over time? (Hint: a new column for decade — int(awardYear) // 10 \* 10 — plus a pivot, both from earlier chapters.)  
3. Stretch. Type prizeAmountAdjusted as numeric with \#, then plot it against awardYear. There's a visible story in the prize's real value across the 20th century.
