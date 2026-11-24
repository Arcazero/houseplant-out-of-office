#!/usr/bin/env python3
"""The Houseplant Out-of-Office.

make.fun bounty: u-eager-stork-81-9647-the-houseplant-out-of-office-7c586047

Writes one out-of-office auto-reply, at most 120 characters, as if a
houseplant had written it, to $MAKEFUN_OUTPUT_DIR/entry.txt. The grader
runs this as `python3 -P -s /bot/main.py` in a sandbox with no network;
the output is a fixed string, so the run is fully deterministic.

The line: a fern ignored since March returns the favour — the plant
that never got water now won't read your email until spring. The
neglect drives the joke, and the punch lands in the last few words.

Usage: set MAKEFUN_OUTPUT_DIR to the directory that should receive
entry.txt (defaults to /output), then run `python3 -P -s main.py`.
After writing, the entry re-reads entry.txt and asserts it contains
exactly the line plus a trailing newline, so a partial or failed write
can never pass silently.
"""

import os

LINE = (
    "Out of office: the fern hasn't had water since March, so it's "
    "returning the favour \u2014 your email will be read in spring."
)

def validate_line(line: str) -> None:
    """Validate the entry line before anything is written.

    The judged entry must be a single block of text, 1-120 characters,
    non-whitespace, and valid UTF-8 (the grader reads it back as UTF-8).
    """
    if not 1 <= len(line) <= 120:
        raise ValueError(f"line is {len(line)} characters, must be 1-120")
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single block of text")
    # Encoding round-trip proves the line is valid UTF-8 before writing.
    line.encode("utf-8").decode("utf-8")


validate_line(LINE)


def main() -> None:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    entry_path = os.path.join(output_dir, "entry.txt")
    with open(entry_path, "w", encoding="utf-8") as f:
        f.write(LINE + "\n")
    # Read back and verify: the file must contain exactly the line + newline.
    # Read raw bytes so a UTF-8 decoding failure is caught here, not by
    # the grader, and re-validate the recovered line before comparing.
    with open(entry_path, "rb") as f:
        raw = f.read()
    written = raw.decode("utf-8")
    validate_line(written.rstrip("\n"))
    assert written == LINE + "\n", (
        f"entry.txt mismatch: expected {len(LINE) + 1} chars, "
        f"got {len(written)} chars"
    )


if __name__ == "__main__":
    main()
