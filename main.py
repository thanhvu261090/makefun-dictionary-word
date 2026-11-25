#!/usr/bin/env python3
"""The Word You'd Delete From the Dictionary.

Writes one word -- the single word to erase from the dictionary forever --
to /output/entry.txt, and prints it.

The pick: "irregardless". It is the dictionary's own typo that got tenure:
a double negative dressed up as a real word, listed only as "nonstandard",
doing a job "regardless" already does perfectly. Delete it and nothing is
lost -- the language gets cleaner, and the dictionary stops apologising
for it in the footnotes.

Deterministic: the entry is a fixed string; every run writes byte-identical
output.
"""

import os
import sys

ENTRY = "irregardless"

MAX_CHARS = 77


def validate_is_string(text) -> None:
    """Entry must be a string."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")


def validate_length(text: str) -> None:
    """Entry must be 1-77 characters (the competition gate)."""
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(f"entry is {len(text)} chars, must be 1-{MAX_CHARS}")


def validate_single_word(text: str) -> None:
    """Entry must be exactly one word: no spaces, no newlines."""
    if len(text.split()) != 1:
        raise ValueError("entry must be exactly one word")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must not contain a newline")


def validate_no_surrounding_whitespace(text: str) -> None:
    """Entry must not have leading/trailing whitespace and must not be
    only whitespace."""
    if text != text.strip():
        raise ValueError("entry must not have leading/trailing whitespace")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")


def validate_utf8(text: str) -> None:
    """Entry must encode as valid UTF-8."""
    text.encode("utf-8")


def gate_check(text: str) -> None:
    """Enforce the competition gate: 1-77 chars, exactly one word, no
    leading/trailing whitespace, non-blank, valid UTF-8."""
    validate_is_string(text)
    validate_length(text)
    validate_single_word(text)
    validate_no_surrounding_whitespace(text)
    validate_utf8(text)


def resolve_output_path() -> str:
    """Output path comes from ENTRY_OUTPUT, defaulting to /output/entry.txt."""
    return os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def write_entry(text: str, out_path: str) -> None:
    """Write exactly the word, no trailing newline, so the gated file is
    byte-identical to the entry."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def why_this_word() -> str:
    """One-line rationale for the pick, for humans only -- never part of
    the entry itself (the entry is the bare word, nothing attached)."""
    return (
        "irregardless is a double negative doing regardless's job; "
        "erase it and the language loses nothing."
    )


def run_self_test() -> int:
    """Self-test: verify the entry and each gate rule.

    Covers the exact 12-char entry, byte-identical repeat writes, and
    rejection of an 78-char string, a two-word string, a multi-line
    string, leading/trailing whitespace, an empty string, a
    whitespace-only string, and a non-string value. Also checks the
    entry is a plain lowercase alphabetic word and is not "regardless"
    itself -- the word that already does this job.
    Returns 0 on success, 1 on any failure.
    """
    failures = []

    def expect_reject(label: str, value) -> None:
        try:
            gate_check(value)
        except ValueError:
            return
        failures.append(f"{label}: gate_check accepted it")

    def expect_accept(label: str, value) -> None:
        try:
            gate_check(value)
        except ValueError as exc:
            failures.append(f"{label}: gate_check rejected it ({exc})")

    # The entry itself: exact text and exact length.
    if ENTRY != "irregardless":
        failures.append("ENTRY does not match the expected word")
    if len(ENTRY) != 12:
        failures.append(f"ENTRY is {len(ENTRY)} chars, expected 12")
    expect_accept("entry", ENTRY)

    # The word must be a plain lowercase alphabetic word, spelled
    # correctly, and must not be "regardless" -- that word earns its keep.
    if not ENTRY.isalpha() or not ENTRY.islower():
        failures.append("ENTRY is not a plain lowercase alphabetic word")
    if ENTRY == "regardless":
        failures.append("ENTRY must not be 'regardless' itself")
    if why_this_word().count("irregardless") != 1:
        failures.append("rationale does not name the entry word exactly once")

    # Repeat writes must be byte-identical.
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        p1 = os.path.join(tmp, "a.txt")
        p2 = os.path.join(tmp, "b.txt")
        write_entry(ENTRY, p1)
        write_entry(ENTRY, p2)
        with open(p1, "rb") as f:
            first = f.read()
        with open(p2, "rb") as f:
            second = f.read()
        if first != second:
            failures.append("repeat writes are not byte-identical")
        if first != ENTRY.encode("utf-8"):
            failures.append("written bytes do not match ENTRY")

    # Boundary lengths: exactly 77 passes, 78 fails, 1 char passes.
    expect_accept("77-char word", "x" * 77)
    expect_reject("78-char word", "x" * 78)
    expect_accept("1-char word", "x")

    # Word and whitespace rules.
    expect_reject("two-word string", "two words")
    expect_reject("multi-line string", "first\nsecond")
    expect_reject("leading whitespace", "  padded")
    expect_reject("trailing whitespace", "padded  ")
    expect_reject("empty string", "")
    expect_reject("whitespace-only string", "   ")

    # Type rule.
    expect_reject("non-string value", 12345)

    if failures:
        for failure in failures:
            print(f"SELF-TEST FAIL: {failure}", file=sys.stderr)
        return 1
    print("SELF-TEST PASS: entry 12 chars, gate rules verified")
    return 0


def main() -> int:
    gate_check(ENTRY)
    out_path = resolve_output_path()
    write_entry(ENTRY, out_path)
    print(ENTRY)
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(run_self_test())
    sys.exit(main())
