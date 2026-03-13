#!/usr/bin/env python3
"""
Collect all positive key lemmas from corpus/08_keylemmas, deduplicate them,
and write the result to corpus/09_kw_selected/keywords.txt.
"""

import glob
import os


INPUT_DIR = "corpus/08_keylemmas"
OUTPUT_DIR = "corpus/09_kw_selected"
OUTPUT_FILE = "keywords.txt"


def load_poskw(filepath: str) -> set[str]:
    """
    Load all lemmas marked as POSKW from one key-lemma file.
    """
    lemmas = set()

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()[1:]  # skip header

    for line in lines:
        parts = line.strip().split()
        if len(parts) < 2:
            continue

        lemma = parts[0]
        status = parts[-1]

        if status == "POSKW":
            lemmas.add(lemma)

    return lemmas


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_lemmas: set[str] = set()

    for filepath in sorted(glob.glob(os.path.join(INPUT_DIR, "*.txt"))):
        lemmas = load_poskw(filepath)
        all_lemmas.update(lemmas)
        print(f"Loaded {len(lemmas)} POSKW lemmas from {os.path.basename(filepath)}")

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    with open(output_path, "w", encoding="utf-8") as f:
        for lemma in sorted(all_lemmas):
            f.write(f"{lemma}\n")

    print(f"\nWrote {len(all_lemmas)} unique keywords to {output_path}")


if __name__ == "__main__":
    main()