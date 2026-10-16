#!/usr/bin/env python3
"""Redact common email addresses, phone numbers and selected secret formats from a UTF-8 text file entirely offline."""

import argparse
import re
from pathlib import Path

PATTERNS = [
    ("EMAIL", r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    ("SECRET", r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,})\b"),
    ("PHONE", r"(?<!\w)(?:\+?86[- ]?)?1[3-9]\d{9}(?!\w)"),
    ("PHONE", r"(?<!\w)(?:\+?1[- .]?)?\(?\d{3}\)?[- .]\d{3}[- .]\d{4}(?!\w)"),
]


def redact(text, extra=()):
    counts = {}
    for label, pattern in [*PATTERNS, *(("CUSTOM", p) for p in extra)]:
        text, count = re.subn(pattern, f"[REDACTED_{label}]", text)
        counts[label] = counts.get(label, 0) + count
    return text, counts


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("file", type=Path)
    p.add_argument("--output", type=Path, required=True, help="New file; existing files are never overwritten")
    p.add_argument("--pattern", action="append", default=[], help="Additional Python regular expression")
    a = p.parse_args()
    try:
        if a.file.resolve() == a.output.resolve():
            p.error("Output must differ from input")
        result, counts = redact(a.file.read_text(encoding="utf-8"), a.pattern)
        with a.output.open("x", encoding="utf-8") as f:
            f.write(result)
    except (OSError, UnicodeError, re.error) as exc:
        p.exit(2, f"Input/output error: {exc}\n")
    print("Redaction counts: " + str(counts))


if __name__ == "__main__":
    main()
