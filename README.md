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
make check            # chapters and capture scripts agree
make refresh-data     # re-download datasets/prizes.json
```

To add a screenshot, add a `CAPTURE name` step to the chapter's script and
embed `![alt text](screenshots/name.svg)` in the chapter.

### Automatic updates

- **Screenshots** (`.github/workflows/screenshots.yml`): on every push that
  touches a chapter, script, dataset or `requirements.txt`, regenerates the
  screenshots and commits any that changed back to the same branch.
- **Update VisiData** (`.github/workflows/update-visidata.yml`): every Monday,
  checks PyPI for a newer VisiData. If there is one, it bumps the pin,
  regenerates the screenshots and opens a pull request. If a script no longer
  works with the new version, the PR says so and includes the error.
