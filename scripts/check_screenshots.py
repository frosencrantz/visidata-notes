#!/usr/bin/env python3
"""Check that the chapters and the capture scripts agree on screenshots.

Fails if a chapter embeds an image that no script captures, if a script
captures an image no chapter uses, or if screenshots/ holds a stale file.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def main():
    problems = []
    embedded = {}
    for md in sorted(REPO.glob("*.md")):
        if md.name == "README.md":  # documents the syntax with an example
            continue
        for name in re.findall(r"\]\(screenshots/([\w.-]+)\.svg\)", md.read_text()):
            embedded.setdefault(name, md.name)

    captured = {}
    for ts in sorted((REPO / "terminal" / "scripts").glob("*.ts")):
        for line in ts.read_text().splitlines():
            m = re.match(r"\s*CAPTURE\s+(\S+)", line)
            if m:
                if m.group(1) in captured:
                    problems.append(f"{ts.name}: {m.group(1)} is also captured by "
                                    f"{captured[m.group(1)]}")
                captured[m.group(1)] = ts.name

    on_disk = {p.stem for p in (REPO / "screenshots").glob("*.svg")}

    for name in sorted(embedded.keys() - captured.keys()):
        problems.append(f"{embedded[name]} embeds {name}.svg, but no script captures it")
    for name in sorted(captured.keys() - embedded.keys()):
        problems.append(f"{captured[name]} captures {name}, but no chapter embeds it")
    for name in sorted(captured.keys() - on_disk):
        problems.append(f"screenshots/{name}.svg is missing; run `make screenshots`")
    for name in sorted(on_disk - captured.keys()):
        problems.append(f"screenshots/{name}.svg is not captured by any script; delete it")

    for p in problems:
        print(p)
    if problems:
        sys.exit(1)
    print(f"{len(captured)} screenshots, all captured and embedded")


if __name__ == "__main__":
    main()
