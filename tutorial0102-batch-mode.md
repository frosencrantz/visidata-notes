# The Command Log and Batch Mode

Here is the payoff the last three chapters have been building toward: everything you did in them was being recorded. Every dive, every expand, every unfurl, every selection — VisiData kept a structured log of all of it, and that log can be edited, saved, parameterized, and replayed without you at the keyboard.  
This changes what kind of tool VisiData is. An interactive session stops being a one-off exploration that you'd have to re-click next month; it becomes a *rough draft of a script* that you refine by doing. By the end of this chapter, the entire Nobel Prize pipeline — download, dive, unfurl, expand, save — will be one shell command you can rerun the morning after next year's prizes are announced.

## Reading the log

Work through the nested-data chapter's flow again — open prizes.json, dive into nobelPrizes, unfurl laureates, expand laureates\_value. Then press Shift+D (cmdlog-sheet).  
You get a sheet where each row is a command you ran, with columns that should look familiar by now:

| Column | What it holds |
| :---- | :---- |
| sheet | Which sheet the command ran on |
| col, row | Where the cursor was, when the command cares |
| longname | The command's true name — open-cell, unfurl-col, expand-col-depth |
| input | What you typed at the prompt — a filename, a depth, an expression |
| keystrokes | The keys you pressed to invoke it |

Two things worth noticing. First, the longname column: those names you've been running with Space since the selection chapter aren't an obscure alternative interface — they're the *primary* names of every command, and the keystrokes are just bindings to them. The log is written in longnames because longnames are what VisiData actually speaks.  
Second, what's *missing*: your navigation. Cursor movement, scrolling, paging through sheets to look around — none of it is logged, because none of it changed anything. The log records intent, not fidgeting.  
There are three views of the log, and the differences matter:

| Keystroke | Command | What you see |
| :---- | :---- | :---- |
| Shift+D | cmdlog-sheet | The commands that produced the *current sheet* — dead ends already removed |
| g Shift+D | cmdlog-all | Everything you've done this session, dead ends and all |
| z Shift+D | cmdlog-sheet-only | Only commands run on this exact sheet, without its parents' history |

Shift+D is the one you'll usually want, and its pruning is the quiet star of this chapter: it answers "how did I *get* here?" with just the steps that mattered. Open g Shift+D after a real exploration session and compare — the difference between the two is a record of every rabbit hole you went down. (No judgment. That's what exploration looks like. It's just not what you want to replay.)

## The log is a sheet, so you already know how to edit it

The command log is an ordinary VisiData sheet, which means every skill from this tutorial applies to it. Deleted a row with d? That command won't replay. Want to change which file gets opened, or tweak an expression you typed three commands ago? Edit the input cell with e, like any other cell.  
This is the workflow that makes logs worth keeping: do the analysis interactively, then prune the log down to its essence. A trimmed log for our Nobel pipeline needs only four rows: open the file, dive into the cell, unfurl, expand.  
Save it from the log sheet with Ctrl+D (save-cmdlog), which writes a .vdj file. Here's ours, in full:  
\#\!/usr/bin/env \-S vd \-p  
{"longname": "open-file", "input": "prizes.json"}  
{"col": "nobelPrizes", "row": "0", "longname": "open-cell"}  
{"col": "laureates", "longname": "unfurl-col"}  
{"col": "laureates\_value", "longname": "expand-col-depth", "input": "2"}

Look at what a .vdj file *is*: one JSON object per line. That's JSONL — the format from the first page of the nested-data chapter. Your session history is itself a dataset, and yes, vd opens it like any other. Of course it does.  
Note: A saved log includes more fields per row than the hand-trimmed version above (sheet, keystrokes, comment, …). Most are optional. As the minimal example shows, a row needs little more than a longname — and leaner rows are actually *more* robust, as we'll see below.

## Replaying

Play a log back inside the interface with:  
vd \-p flatten-prizes.vdj

VisiData opens and re-executes each command, sheet by sheet, ending exactly where your session ended. Add \-w 1 (\--replay-wait) to pause a second between steps — watching your own analysis replay itself is both a decent demo and a surprisingly good way to spot a step you didn't mean to keep. Ctrl+K cancels a running replay.  
You can also replay *from* the log sheet itself: x re-executes the current row, gx replays the whole log. Editing a cmdlog and x\-ing your way down it row by row is the closest thing VisiData has to stepping through a script in a debugger — because that's what it is.

## Batch mode: no interface at all

Add \--batch (or \-b) and the interface never opens: VisiData replays the log headlessly and exits. Add \-o to save whatever sheet the replay ends on:  
vd \--batch \-p flatten-prizes.vdj \-o laureates.csv

That's the whole Nobel pipeline, terminal to CSV, in one line. Some useful variations:

* \-o out.json — the output format follows the extension, same as Ctrl+S.  
* \-o \- — write the final sheet to stdout (as TSV), ready to pipe onward.  
* \-i (\--interactive) — run the batch replay, then open the interface on the result. The best of both: scripted setup, interactive finish.

If a step fails in batch mode, the replay aborts and says which command it died on — it does not shrug and continue with half a pipeline. When next year's API response renames a column, you'll get a loud replay aborted during unfurl-col, not a quietly wrong CSV. For data work, loud is a feature.

## Parameterizing: one log, many inputs

A hard-coded filename makes a log a recording. A parameter makes it a *tool*. In a .vdj file, write $name placeholders — this is Python string.Template syntax — and supply values as name=value arguments at the command line:  
\#\!/usr/bin/env \-S vd \-p  
{"longname": "open-file", "input": "$infile"}  
{"col": "nobelPrizes", "row": "0", "longname": "open-cell"}  
{"col": "laureates", "longname": "unfurl-col"}  
{"col": "laureates\_value", "longname": "expand-col-depth", "input": "2"}

vd \-b \-p flatten-prizes.vdj infile=prizes2026.json \-o laureates2026.csv

One subtlety makes parameterized logs work, and it's worth understanding rather than cargo-culting: rows without a sheet field run on whatever sheet is current. VisiData names sheets after their source file, so a log that says "sheet": "prizes" breaks the moment the input is called prizes2026.json. The hand-trimmed log above omits sheet everywhere — each command simply runs on the sheet the previous command produced, so the same four lines work on any conforming input file, whatever its name. When you're editing a log for reuse, deleting the sheet values is usually the first and best simplification.  
Parameters aren't limited to filenames — any input cell can hold one. A log with {"longname": "select-expr", "input": "category.get(\\"en\\") \== \\"$category\\""} becomes a per-category extractor: category=Peace today, category=Physics tomorrow.

## Logs as executables

Look again at the first line VisiData writes when saving a .vdj:  
\#\!/usr/bin/env \-S vd \-p

That's a real shebang. chmod \+x flatten-prizes.vdj and it runs as a command in its own right:  
./flatten-prizes.vdj infile=prizes.json

And because both ends of the pipeline speak stdin/stdout, a cmdlog slots into shell pipelines like any other tool — VisiData reads data from stdin with \- as the filename (plus \-f to name the format), and \-p \- even reads the *log itself* from stdin:  
curl \-s "https://api.nobelprize.org/2.1/nobelPrizes?limit=1000" \> prizes.json  
vd \-b \-p flatten-prizes.vdj infile=prizes.json \-o \- | grep 1972

## From log to keystroke: macros

A saved log is a script you run from the shell. Sometimes what you want instead is a new *command* — "unfurl and expand to depth 2" as a single keystroke, available in every future session. That's m (macro-record): press it, perform the commands, press m again, and give the recording a keystroke. From then on, that key replays the sequence on whatever sheet you're on. gm (macro-sheet) lists the macros you've defined.  
The mental model is tidy: a cmdlog packages commands for the shell; a macro packages them for your fingers.

## The craft of a durable log

Replay is by *name* — sheet names, column names, command longnames. That gives replays their power (they adapt to new data of the same shape) and defines their limits (they abort when the shape changes). A few habits produce logs that keep working:

* Trim hard. Every kept row is a dependency. The four-line pipeline survives contact with new data better than a forty-line session transcript ever will.  
* Drop sheet fields from hand-edited logs, as above.  
* Prefer expressions to positions. A select-expr row says *what* you meant; a hand-edited row that depends on where the cursor happened to be says only *where you were pointing*. The selection chapter's z| habits pay off again here.  
* Let it abort. Resist the urge to make a brittle log "work" by hand-editing outputs. An aborted replay is your data telling you its shape changed — investigate interactively, fix the log, rerun.

## Try it

1. Archaeology. After your next real VisiData session, open g Shift+D and count the dead ends. Then open Shift+D and admire the pruning. Save the pruned version.  
2. The full pipeline. Build flatten-prizes.vdj yourself — interactively, then trim the log. Batch-run it. Confirm the output has 1,075 rows, and that you know why it isn't 1,026.  
3. Parameterize. Add a select-expr row with a $category placeholder and dup-selected after it, so the pipeline emits one category's laureates. Run it twice with different categories.  
4. A keystroke of your own. Record a macro that unfurls the current column and expands the result to depth 2\. Spend it on the next nested dataset you meet.  
5. Stretch. chmod \+x your pipeline and chain it: pipe its \-o \- output into grep, wc \-l, or — why not — another vd.
