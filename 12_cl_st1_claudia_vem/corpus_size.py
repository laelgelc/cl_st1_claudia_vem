#!/usr/bin/env python3
"""
Calculate corpus size for the tagged VEm corpus.

Expected input structure:
    corpus/07_tagged/vem_ed_XX/*.txt

Example:
    corpus/07_tagged/vem_ed_01/t001.txt
    corpus/07_tagged/vem_ed_02/t012.txt

Expected tagged-file format:
    token<TAB>lemma<TAB>pos<TAB>is_alpha<TAB>is_stop

Output:
    corpus_size/corpus_size.tsv

Output format:
    Header included
    Tab-separated
    Columns:
        Strata
        Text Count
        Word Count
"""

import re
from pathlib import Path
from collections import defaultdict


# --- Configuration ---
CORPUS_ROOT = Path("corpus/07_tagged")
OUTPUT_DIR = Path("corpus_size")
OUTPUT_FILE = OUTPUT_DIR / "corpus_size.tsv"

EDITION_PATTERN = re.compile(r"^vem_ed_(\d+)$")


# --- Counters ---
total_files = 0
total_words = 0

file_counts_edition = defaultdict(int)
word_counts_edition = defaultdict(int)


def natural_sort_key(text):
    """Return a natural-sort key that treats digit runs as integers."""
    parts = re.split(r"(\d+)", str(text))
    return [int(part) if part.isdigit() else part.lower() for part in parts]


def edition_sort_key(path: Path):
    """Sort VEm edition folders by numeric edition number."""
    match = EDITION_PATTERN.match(path.name)

    if not match:
        return natural_sort_key(path.name)

    return int(match.group(1))


def count_tokens_in_tagged_file(path: Path) -> int:
    """
    Count alphabetic token lines in a tagged corpus file.

    Expected format:
        token    lemma    pos    is_alpha    is_stop

    A row counts as one word/token when:
        - it is not the header row;
        - it has at least five tab-separated columns;
        - is_alpha is True.
    """
    words = 0

    with path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.rstrip("\n")

            if not line:
                continue

            parts = line.split("\t")

            if len(parts) < 5:
                continue

            token, lemma, pos, is_alpha, is_stop = parts[:5]

            # Skip header row.
            if line_number == 1 and (
                    token == "token"
                    and lemma == "lemma"
                    and pos == "pos"
            ):
                continue

            if is_alpha == "True":
                words += 1

    return words


def main():
    global total_files, total_words

    if not CORPUS_ROOT.exists():
        raise FileNotFoundError(f"Corpus directory does not exist: {CORPUS_ROOT}")

    if not CORPUS_ROOT.is_dir():
        raise NotADirectoryError(f"Corpus path is not a directory: {CORPUS_ROOT}")

    edition_dirs = sorted(
        [
            path for path in CORPUS_ROOT.iterdir()
            if path.is_dir() and EDITION_PATTERN.match(path.name)
        ],
        key=edition_sort_key,
    )

    if not edition_dirs:
        raise FileNotFoundError(
            f"No VEm edition folders found under {CORPUS_ROOT}. "
            "Expected folders such as vem_ed_01, vem_ed_02, etc."
        )

    for edition_dir in edition_dirs:
        edition = edition_dir.name

        text_files = sorted(
            edition_dir.glob("*.txt"),
            key=lambda path: natural_sort_key(path.name),
        )

        for text_file in text_files:
            words = count_tokens_in_tagged_file(text_file)

            file_counts_edition[edition] += 1
            word_counts_edition[edition] += words

            total_files += 1
            total_words += words

    OUTPUT_DIR.mkdir(exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        f.write("Strata\tText Count\tWord Count\n")

        for edition in sorted(file_counts_edition, key=natural_sort_key):
            f.write(
                f"{edition}\t"
                f"{file_counts_edition[edition]}\t"
                f"{word_counts_edition[edition]}\n"
            )

        f.write("\n")
        f.write(f"overall\t{total_files}\t{total_words}\n")

    print(f"Corpus sizes saved to {OUTPUT_FILE}")
    print(f"Total texts: {total_files}")
    print(f"Total words: {total_words}")


if __name__ == "__main__":
    main()