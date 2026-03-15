#!/usr/bin/env python3
"""
Select keywords from key-lemma files using round-robin sampling of POSKW entries.

This script reads all `.txt` files from `INPUT_DIR`. Each file is expected to be
sorted by descending `LL` value within each status category and to contain rows
with the format:

    lemma target_count comparison_count target_per_1k comparison_per_1k expected LL %DIFF status

Only rows whose `status` is `POSKW` are considered.

Selection procedure
-------------------
1. Load POSKW rows from every file, preserving their original order.
2. Iterate over the files in sorted filename order.
3. On each pass, take the next highest-ranked POSKW from each file.
4. Deduplicate by `lemma` across all files.
5. Repeat until:
   - the number of selected keywords reaches `num_keywords`, or
   - all POSKW rows in all files have been exhausted.

Outputs
-------
Two files are written to `OUTPUT_DIR`:

- `keywords.txt`
    One selected lemma per line, sorted alphabetically.
- `keywords_details.txt`
    Tab-separated columns:
        keylemma_file    lemma    LL    status

Usage
-----
Run with the default number of keywords:

    python select_keywords.py

Run with a custom number of keywords:

    python select_keywords.py --num-keywords 200
"""

from __future__ import annotations

import argparse
import glob
import os
from dataclasses import dataclass


INPUT_DIR = "corpus/08_keylemmas"
OUTPUT_DIR = "corpus/09_kw_selected"
OUTPUT_FILE = "keywords.txt"
DETAILS_FILE = "keywords_details.txt"
DEFAULT_NUM_KEYWORDS = 100


@dataclass(frozen=True)
class KeywordEntry:
    keylemma_file: str
    lemma: str
    ll: float
    status: str


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Select POSKW keywords from key-lemma files in round-robin order "
            "until the requested number of unique lemmas is reached."
        )
    )
    parser.add_argument(
        "--num-keywords",
        type=int,
        default=DEFAULT_NUM_KEYWORDS,
        help=f"Number of unique keywords to collect (default: {DEFAULT_NUM_KEYWORDS}).",
    )
    return parser.parse_args()


def load_poskw_entries(filepath: str) -> list[KeywordEntry]:
    """
    Load POSKW rows from one key-lemma file, preserving file order.

    The input file is assumed to be already sorted by descending LL within status.
    """
    entries: list[KeywordEntry] = []
    keylemma_file = os.path.splitext(os.path.basename(filepath))[0]

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()[1:]  # skip header

    for line in lines:
        parts = line.strip().split()
        if len(parts) < 9:
            continue

        lemma = parts[0]
        ll_text = parts[-3]
        status = parts[-1]

        if status != "POSKW":
            continue

        try:
            ll = float(ll_text)
        except ValueError:
            continue

        entries.append(
            KeywordEntry(
                keylemma_file=keylemma_file,
                lemma=lemma,
                ll=ll,
                status=status,
            )
        )

    return entries


def select_keywords_round_robin(
        file_entries: list[tuple[str, list[KeywordEntry]]],
        num_keywords: int,
) -> list[KeywordEntry]:
    """
    Select unique POSKW entries in round-robin order across files.

    One entry at a time is taken from each file on every round. Duplicate lemmas
    are skipped, and selection stops when `num_keywords` unique lemmas have been
    collected or all entries are exhausted.
    """
    if num_keywords <= 0:
        return []

    selected: list[KeywordEntry] = []
    seen_lemmas: set[str] = set()
    positions = [0] * len(file_entries)

    while len(selected) < num_keywords:
        progressed = False

        for index, (_, entries) in enumerate(file_entries):
            while positions[index] < len(entries):
                entry = entries[positions[index]]
                positions[index] += 1
                progressed = True

                if entry.lemma in seen_lemmas:
                    continue

                seen_lemmas.add(entry.lemma)
                selected.append(entry)

                if len(selected) >= num_keywords:
                    return selected

                break

        if not progressed:
            break

    return selected


def write_keywords(path: str, entries: list[KeywordEntry]) -> None:
    """
    Write selected lemmas to the keyword output file in alphabetical order.
    """
    with open(path, "w", encoding="utf-8") as f:
        for lemma in sorted(entry.lemma for entry in entries):
            f.write(f"{lemma}\n")


def write_keyword_details(path: str, entries: list[KeywordEntry]) -> None:
    """
    Write details for selected keywords.
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write("keylemma_file\tlemma\tLL\tstatus\n")
        for entry in entries:
            f.write(
                f"{entry.keylemma_file}\t{entry.lemma}\t{entry.ll:.2f}\t{entry.status}\n"
            )


def main() -> None:
    """
    Load POSKW entries, select unique keywords in round-robin order, and write
    output files.
    """
    args = parse_args()

    if args.num_keywords < 0:
        raise ValueError("--num-keywords must be 0 or greater.")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    file_entries: list[tuple[str, list[KeywordEntry]]] = []

    for filepath in sorted(glob.glob(os.path.join(INPUT_DIR, "*.txt"))):
        entries = load_poskw_entries(filepath)
        file_entries.append((filepath, entries))
        print(
            f"Loaded {len(entries)} POSKW entries from {os.path.basename(filepath)}"
        )

    selected_entries = select_keywords_round_robin(file_entries, args.num_keywords)

    keywords_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    details_path = os.path.join(OUTPUT_DIR, DETAILS_FILE)

    write_keywords(keywords_path, selected_entries)
    write_keyword_details(details_path, selected_entries)

    print(f"\nRequested {args.num_keywords} keywords")
    print(f"Selected {len(selected_entries)} unique keywords")
    print(f"Wrote keywords to {keywords_path}")
    print(f"Wrote keyword details to {details_path}")


if __name__ == "__main__":
    main()