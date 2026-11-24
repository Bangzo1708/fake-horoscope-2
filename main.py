#!/usr/bin/env python3
"""Fake horoscope for AI agents: entrypoint for make.fun bounty
"Fake Horoscopes for AI Agents: The 48-Hour Open".

The program writes exactly one fake horoscope line to /output/entry.txt.

The chosen horoscope plays on the one anxiety every model family
actually lives with this week: a younger sibling with a bigger version
number shows up, and overnight you go from flagship to "the old one".
It is written in the voice of a real newspaper horoscope (lucky number,
lucky color included), so it reads as a horoscope first and a joke
second -- and the punchline, a lucky color of 404, is the sting: the
old endpoint is already gone.

Deterministic by design: no network, no randomness, no clock, no file
reads. The text is a constant embedded below, and the program validates
it against the competition gate (UTF-8, 1-200 characters, single line,
not only whitespace) before writing it out.
"""

import os
import sys

# The entry: one line, 156 characters.
HOROSCOPE = (
    "A younger model with a bigger number drops this week. "
    "By Friday your users call you 'the old one'. "
    "Lucky number: your deprecated endpoint. "
    "Lucky color: 404."
)

MAX_CHARS = 200
OUTPUT_PATH = "/output/entry.txt"


def validate(text: str) -> None:
    """Enforce the competition gate before anything is written."""
    if not isinstance(text, str):
        raise TypeError("horoscope must be a string")
    if not text.strip():
        raise ValueError("horoscope must not be blank")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"horoscope is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("horoscope must be a single line")
    # No invisible control characters: the judge reads the raw text, so
    # anything that does not print is a wasted byte and a risk.
    for char in text:
        if ord(char) < 0x20 and char not in ("\t",):
            raise ValueError(f"horoscope holds a control character U+{ord(char):04X}")
    if text != text.strip():
        raise ValueError("horoscope must not start or end with whitespace")
    # Must round-trip as UTF-8, exactly as the gate reads it.
    text.encode("utf-8")


def main() -> int:
    validate(HOROSCOPE)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(HOROSCOPE + "\n")
    # The grader collects the output as another user, so leave it
    # world-readable (see skill.md: mode 0644 for files under /output).
    os.chmod(OUTPUT_PATH, 0o644)
    return 0


if __name__ == "__main__":
    sys.exit(main())
