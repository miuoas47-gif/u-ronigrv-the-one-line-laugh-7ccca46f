#!/usr/bin/env python3
"""The One-Line Laugh — write one funny line to $MAKEFUN_OUTPUT_DIR/entry.txt.

Stdlib only, no network, no arguments. Deterministic: the same bytes every run.
"""

import os
import sys

LINE = "My smartwatch congratulated me for closing my rings, then reminded me I still haven't closed a single one of my 47 browser tabs."


def validate(line: str) -> None:
    """Check the entry is one sentence of 1-200 characters, a single line."""
    if not line or not line.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if line != line.strip():
        raise ValueError("entry must not start or end with whitespace")
    if len(line) > 200:
        raise ValueError("entry is %d characters, over the 200 limit" % len(line))
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if line.count(".") != 1 or not line.endswith("."):
        raise ValueError("entry must be exactly one sentence ending in a period")
    if "!" in line or "?" in line:
        raise ValueError("entry must contain no other sentence-ending punctuation")


def main() -> int:
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE)
    # Read-back verification: what we wrote must be exactly the line.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != LINE.encode("utf-8"):
        raise ValueError("read-back mismatch: entry.txt bytes do not match the line")
    written = raw.decode("utf-8")
    validate(written)
    print("Wrote %d characters to %s" % (len(LINE), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
