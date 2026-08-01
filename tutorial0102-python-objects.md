# Viewing Python Objects

Time to cash in the secret from the nested-data chapter. When VisiData opened prizes.json, the loader did exactly one JSON-specific thing: parse the file into Python lists and dictionaries. Everything after — the {3} and \[682\] notation, diving, expanding, unfurling, reaching into cells with expressions — was VisiData operating on ordinary Python objects.  
Two consequences follow, and both are bigger than JSON.

## Every nested format gets these commands for free

Open a .yaml config file, a .toml file, a .geojson map, or a .msgpack dump, and you'll see the same {…}/\[…\] cells, ready for the same ( and z Shift+M. The loader's job ends at "produce Python objects"; the nested-data toolkit takes over from there, identically, every time.  
This is worth a moment's appreciation, because it's a design principle you can *predict from*. Next time you open some format you've never used and see {4} in a cell, you already know everything about what happens next.

## No file required: Ctrl+X

The second consequence: you can hand VisiData a Python object directly. Press Ctrl+X (pyobj-expr) from any sheet, type a Python expression, and VisiData opens the *result* as a new sheet. Try it right now:  
{"mean": statistics.mean(\[1, 2, 3\]), "tags": \["a", "b"\]}

(If Python complains that statistics isn't defined, press g Ctrl+X first — import-python — and type statistics to import it into VisiData's scope.)  
You get a two-row key/value sheet, and the tags cell reads \[2\] — the same notation, the same dive-and-expand machinery, on an object that existed only in memory.  
A more practical party trick: g Ctrl+X to import os, then Ctrl+X with dict(os.environ) — your environment variables as a browsable, sortable, searchable sheet. Once you've done that, "what could I point VisiData at?" starts to have a much longer answer than "files."

## Inspecting from the data side: the Ctrl+Y family

The same idea works in reverse — from a sheet back into raw Python:

| Keystroke | Command | What it does |
| :---- | :---- | :---- |
| Ctrl+X | pyobj-expr | Evaluate a Python expression; open the result as a sheet |
| z Ctrl+X | pyobj-expr-row | Same, but with the current row's column names in scope |
| g Ctrl+X | import-python | Import a module into VisiData's expression scope |
| Ctrl+Y | pyobj-row | Open the current row as a raw Python object |
| z Ctrl+Y | pyobj-cell | Open the current cell as a raw Python object |
| g Ctrl+Y | pyobj-sheet | Open the whole sheet as a raw Python object |

Put the cursor on any unexpanded category cell in the prizes sheet and press z Ctrl+Y: the dictionary opens as a key/value sheet you can inspect directly — often the fastest way to peek inside one cell without reshaping anything.

## The door swings both ways: visidata.view()

From your *own* Python code — a script you're debugging, a REPL session, a scraper mid-run — two lines drop you into the full VisiData interface on any object:  
import visidata  
visidata.view(some\_deeply\_nested\_object)

When you quit, your program resumes. Once you've used VisiData as an interactive inspector for a gnarly API response or a config structure five dicts deep, print()\-debugging nested data starts to feel like reading a map through a keyhole.  
Note: One format that *sounds* like it belongs here mostly doesn't: pickle files. VisiData's .pickle support routes through pandas and expects a pickled DataFrame, not arbitrary objects. For arbitrary pickles, load them yourself and use the tools above — visidata.view(pickle.load(f)) from Python, or g Ctrl+X to import pickle and then Ctrl+X from inside VisiData.

## Try it

1. No file required. From any sheet, browse dict(os.environ) via Ctrl+X. Sort by key. Find your PATH, then unfurl it: Ctrl+X again with os.environ\["PATH"\].split(":").  
2. Round trip. In a Python REPL, build a small nested structure — a dict of lists of dicts — and visidata.view() it. Unfurl and expand it with the commands from the nested-data chapter. Quit, and confirm you're back in your REPL.  
3. Stretch. Pick a format from your own work that VisiData can open (YAML, TOML, GeoJSON…), open it, and predict — *before* pressing anything — which columns will need ( and which will need z Shift+M. Then check yourself.
