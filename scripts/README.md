# Screenshot tooling

The tutorial chapters include screenshots of VisiData. They're generated from
keystroke scripts rather than taken by hand, so they can be regenerated
whenever the text or the VisiData version changes.

## Layout

- `terminal/scripts/*.ts` — one keystroke script per chapter, in the same
  format as [intro-to-visidata](https://github.com/jsvine/intro-to-visidata)'s
  (see the top of `termscript.py` for the commands)
- `screenshots/*.svg` — the images the chapters embed
- `terminal/output/*.txt` — plain-text copies of each screenshot, so diffs
  show what changed on screen
- `terminal/misc/` — the clean shell and capture-only VisiData config the
  scripts run under
- `datasets/prizes.json` — a saved copy of the Nobel Prize API response, so
  screenshots don't change when the live data does
- `requirements.txt` — pins the VisiData version the screenshots are taken with
  (a commit on VisiData's `develop` branch)
- `scripts/termscript.py` — runs the keystroke scripts and writes the captures
- `scripts/check_screenshots.py` — checks the chapters and scripts agree

## Commands

Run from the repository root:

```sh
pip install -r requirements.txt
make screenshots      # regenerate all screenshots
make check            # chapters and capture scripts agree
make refresh-data     # re-download datasets/prizes.json
```

To add a screenshot, add a `CAPTURE name` step to the chapter's script and
embed `![alt text](screenshots/name.svg)` in the chapter.

## Automatic updates

- **Screenshots** (`.github/workflows/screenshots.yml`): on every push that
  touches a chapter, script, dataset or `requirements.txt`, regenerates the
  screenshots and commits any that changed back to the same branch.
- **Update VisiData** (`.github/workflows/update-visidata.yml`): every Monday,
  checks VisiData's `develop` branch for new commits. If there are any, it
  pins the latest one, regenerates the screenshots and opens a pull request
  (or updates the one already open). If a script no longer
  works with the new version, the PR says so and includes the error. This
  needs "Allow GitHub Actions to create and approve pull requests" turned on
  under Settings → Actions → General.
