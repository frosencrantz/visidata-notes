#!/usr/bin/env python3
"""Drive a terminal program from a keystroke script and capture screenshots.

Reads the same script format as the termrunner tool used by
https://github.com/jsvine/intro-to-visidata, so the scripts there work as
examples. One command per line; blank lines and lines starting with # are
ignored. Arguments are shell-quoted, and backslash escapes (\\n, \\t, \\x13,
\\x1b) in quoted strings are decoded, so Ctrl+S can be sent as "\\x13".

    INIT [--shell CMD] [--width N] [--height N]
        Start CMD (default: bash with terminal/misc/clean-bash.bashrc)
        in a WIDTHxHEIGHT terminal. Must come first.
    SEND TEXT [--enter]
        Type TEXT, optionally followed by Enter.
    ENTER
        Press Enter.
    AWAIT REGEX [--start-line N] [--end-line N] [--timeout SECS]
        Wait until REGEX matches the screen text (or the given slice of
        lines, Python-style, so --start-line -1 is the status bar).
        Fails with a dump of the screen if it never matches.
    PAUSE SECS
        Keep reading output for SECS seconds.
    CAPTURE NAME [--start-line N] [--end-line N]
        Wait for the screen to settle, then write screenshots/NAME.svg and
        terminal/output/NAME.txt (optionally only a slice of lines).

Usage: scripts/termscript.py terminal/scripts/nested-data.ts [...]
"""

import argparse
import html
import os
import re
import shlex
import sys
import tempfile
import time
from pathlib import Path

import pexpect
import pyte

REPO = Path(__file__).resolve().parent.parent
SVG_DIR = REPO / "screenshots"
TEXT_DIR = REPO / "terminal" / "output"
DEFAULT_SHELL = "bash --noprofile --rcfile terminal/misc/clean-bash.bashrc"

# How long the screen must be unchanged before CAPTURE takes the picture.
SETTLE_SECS = 0.4
DEFAULT_TIMEOUT = 15


class ScriptError(Exception):
    pass


def decode_escapes(s):
    return s.encode("latin-1", "backslashreplace").decode("unicode_escape")


# --- Terminal session ---------------------------------------------------------

class Session:
    def __init__(self, shell, width, height):
        self.width, self.height = width, height
        self.screen = pyte.Screen(width, height)
        self.stream = pyte.ByteStream(self.screen)
        self.state_dir = tempfile.TemporaryDirectory(prefix="vd-state-")
        env = {
            "PATH": os.environ["PATH"],
            "HOME": self.state_dir.name,
            "TERM": "xterm-256color",
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
        }
        argv = shlex.split(shell)
        self.child = pexpect.spawn(argv[0], argv[1:], cwd=str(REPO), env=env,
                                   dimensions=(height, width))

    def pump(self, secs):
        """Feed any output produced within `secs` into the virtual screen.
        Returns True if anything arrived."""
        got = False
        deadline = time.monotonic() + secs
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return got
            try:
                data = self.child.read_nonblocking(65536, timeout=remaining)
            except pexpect.TIMEOUT:
                return got
            except pexpect.EOF:
                raise ScriptError("the terminal program exited")
            self.stream.feed(data)
            got = True

    def settle(self, quiet=SETTLE_SECS, timeout=DEFAULT_TIMEOUT):
        deadline = time.monotonic() + timeout
        while self.pump(quiet):
            if time.monotonic() > deadline:
                raise ScriptError("screen never stopped changing")

    def send(self, text):
        self.child.send(text.encode("utf-8"))
        self.pump(0.05)

    def lines(self, start=None, end=None):
        return self.screen.display[start:end]

    def await_(self, pattern, start, end, timeout):
        rx = re.compile(pattern)
        deadline = time.monotonic() + timeout
        while True:
            if rx.search("\n".join(self.lines(start, end))):
                return
            if time.monotonic() > deadline:
                raise ScriptError(f"timed out after {timeout}s waiting for "
                                  f"{pattern!r}; screen was:\n" + self.dump())
            self.pump(0.1)

    def dump(self):
        return "\n".join(f"{i:3}| {l}" for i, l in enumerate(self.lines()))

    def close(self):
        self.child.terminate(force=True)
        self.state_dir.cleanup()


# --- Rendering ------------------------------------------------------------------

# Colors for the 16 named ANSI colors (a dark, GitHub-friendly theme).
PALETTE = {
    "black": "#1e1e1e", "red": "#e06c75", "green": "#98c379", "brown": "#e5c07b",
    "blue": "#61afef", "magenta": "#c678dd", "cyan": "#56b6c2", "white": "#d0d0d0",
    "brightblack": "#5c6370", "brightred": "#ff7b86", "brightgreen": "#b5e890",
    "brightbrown": "#ffd68a", "brightblue": "#7cc5ff", "brightmagenta": "#de9bf2",
    "bfightmagenta": "#de9bf2",  # sic: pyte's typo for bright magenta
    "brightcyan": "#7fd6e0", "brightwhite": "#ffffff",
}
DEFAULT_FG, DEFAULT_BG = "#d0d0d0", "#1e1e1e"
CELL_W, CELL_H, FONT_SIZE, PAD = 8.4, 17, 14, 12
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'DejaVu Sans Mono', monospace"


def color(value, default):
    if value == "default":
        return default
    if value in PALETTE:
        return PALETTE[value]
    if re.fullmatch(r"[0-9a-fA-F]{6}", value):
        return "#" + value.lower()
    return default


def cell_style(ch):
    fg, bg = color(ch.fg, DEFAULT_FG), color(ch.bg, DEFAULT_BG)
    if ch.reverse:
        fg, bg = bg, fg
    return fg, bg, ch.bold, ch.underscore, ch.italics


def render_svg(screen, start, end):
    rows = list(range(screen.lines))[start:end]
    width = screen.columns * CELL_W + 2 * PAD
    height = len(rows) * CELL_H + 2 * PAD
    bgs, texts = [], []
    for y, row in enumerate(rows):
        line = screen.buffer[row]
        ty = PAD + y * CELL_H
        x = 0
        while x < screen.columns:
            # Group consecutive cells with identical styling into one run.
            style = cell_style(line[x])
            run_start, chars = x, []
            while x < screen.columns and cell_style(line[x]) == style:
                chars.append(line[x].data)
                x += 1
            fg, bg, bold, underline, italic = style
            n = x - run_start
            px = PAD + run_start * CELL_W
            if bg != DEFAULT_BG:
                bgs.append(f'<rect x="{px:.1f}" y="{ty}" width="{n * CELL_W:.1f}" '
                           f'height="{CELL_H}" fill="{bg}"/>')
            text = "".join(chars)  # wide chars are followed by an empty cell
            if not text.strip():
                continue
            # SVG collapses ordinary spaces even with xml:space, which would
            # squeeze the run's glyphs out of their cells.
            text = text.replace(" ", "\u00a0")
            attrs = [f'x="{px:.1f}"', f'y="{ty + CELL_H - 4}"',
                     f'textLength="{n * CELL_W:.1f}"']
            if fg != DEFAULT_FG:
                attrs.append(f'fill="{fg}"')
            if bold:
                attrs.append('font-weight="bold"')
            if italic:
                attrs.append('font-style="italic"')
            if underline:
                attrs.append('text-decoration="underline"')
            texts.append(f'<text {" ".join(attrs)}>{html.escape(text, quote=False)}</text>')
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.1f} {height}" role="img">',
        f'<rect width="100%" height="100%" rx="6" fill="{DEFAULT_BG}"/>',
        *bgs,
        f'<g font-family="{FONT}" font-size="{FONT_SIZE}" fill="{DEFAULT_FG}" '
        f'lengthAdjust="spacingAndGlyphs" xml:space="preserve">',
        *texts,
        "</g>",
        "</svg>",
        "",
    ])


def capture(session, name, start, end):
    session.settle()
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    (SVG_DIR / f"{name}.svg").write_text(render_svg(session.screen, start, end))
    text = "\n".join(l.rstrip() for l in session.lines(start, end)).rstrip("\n") + "\n"
    (TEXT_DIR / f"{name}.txt").write_text(text)
    print(f"  captured {name}")


# --- Script interpreter -----------------------------------------------------------

# Per command: (number of positional args, {option: type}). A bool option is a flag.
COMMANDS = {
    "INIT": (0, {"--shell": str, "--width": int, "--height": int}),
    "SEND": (1, {"--enter": bool}),
    "ENTER": (0, {}),
    "AWAIT": (1, {"--start-line": int, "--end-line": int, "--timeout": float}),
    "PAUSE": (1, {}),
    "CAPTURE": (1, {"--start-line": int, "--end-line": int}),
}


def parse_line(line):
    """Split a script line into (command, positional args, options)."""
    cmd, *words = shlex.split(line)
    if cmd not in COMMANDS:
        raise ScriptError(f"unknown command {cmd}")
    npos, opts = COMMANDS[cmd]
    # Positional args come first, so keystrokes like "--" are never options.
    args, words, kw = words[:npos], words[npos:], {}
    if len(args) < npos:
        raise ScriptError(f"{cmd} needs {npos} argument(s)")
    while words:
        opt = words.pop(0)
        if opt not in opts:
            raise ScriptError(f"unknown option {opt} for {cmd}")
        kind = opts[opt]
        key = opt[2:].replace("-", "_")
        if kind is bool:
            kw[key] = True
        elif not words:
            raise ScriptError(f"{opt} needs a value")
        else:
            kw[key] = kind(words.pop(0))
    return cmd, args, kw


def run_script(path):
    print(path)
    session = None
    try:
        for lineno, raw in enumerate(Path(path).read_text().splitlines(), 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            try:
                cmd, args, kw = parse_line(line)
                if cmd == "INIT":
                    session = Session(kw.get("shell", DEFAULT_SHELL),
                                      kw.get("width", 100), kw.get("height", 30))
                elif session is None:
                    raise ScriptError("the script must start with INIT")
                elif cmd == "SEND":
                    session.send(decode_escapes(args[0]) + ("\r" if kw.get("enter") else ""))
                elif cmd == "ENTER":
                    session.send("\r")
                elif cmd == "AWAIT":
                    session.await_(args[0], kw.get("start_line"), kw.get("end_line"),
                                   kw.get("timeout", DEFAULT_TIMEOUT))
                elif cmd == "PAUSE":
                    session.pump(float(args[0]))
                elif cmd == "CAPTURE":
                    capture(session, args[0], kw.get("start_line"), kw.get("end_line"))
            except (ScriptError, ValueError) as e:
                raise ScriptError(f"{path}:{lineno}: {line}\n{e}") from None
    finally:
        if session:
            session.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("scripts", nargs="+")
    args = ap.parse_args()
    try:
        for path in args.scripts:
            run_script(path)
    except ScriptError as e:
        sys.exit(f"error: {e}")


if __name__ == "__main__":
    main()
