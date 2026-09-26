# visidata-notes
My notes on VisiData.

## Screenshots

The tutorial chapters include screenshots of VisiData, generated from keystroke
scripts rather than taken by hand, so they can be regenerated whenever the
text or the VisiData version changes.

- `terminal/scripts/*.ts` — one keystroke script per chapter (same format as
  [intro-to-visidata](https://github.com/jsvine/intro-to-visidata)'s; see the
  top of `scripts/termscript.py`)
- `screenshots/*.svg` — the images the chapters embed
- `terminal/output/*.txt` — plain-text copies, so diffs show what changed on screen
- `datasets/prizes.json` — a saved copy of the Nobel Prize API response, so
  screenshots don't change when the live data does
- `requirements.txt` — pins the VisiData version the screenshots are taken with

```sh
pip install -r requirements.txt
make screenshots      # regenerate all screenshots
make refresh-data     # re-download datasets/prizes.json
```
