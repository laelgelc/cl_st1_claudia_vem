#!/usr/bin/env python3
"""
Generate plaintext example files for each factor pole.

Aligned with examples.py selection logic:
    - reads the same scores table (<project>_scores_only.tsv)
    - uses VEm edition as the grouping variable
    - ranks editions using means_edition_f<n>.tsv
    - selects: top edition -> 20 examples, other editions -> 10 each
    - skips rows where the factor score is 0
    - uses tagged corpus existence checks to keep selection stable with examples.py
    - reconstructs plaintext from tagged TSV files using the token column

The project name is inferred from the current working directory unless supplied
explicitly with --project.

Expected inputs:
    sas/output_<project>/<project>_scores_only.tsv
    sas/output_<project>/means_edition_f<n>.tsv
    file_ids.txt
    examples/score_details.txt
    corpus/07_tagged/vem_ed_XX/<Text ID>.txt

Expected file_ids.txt format:
    No header
    Space-separated
    Columns:
        file_id path

Example:
    t000001 vem_ed_01/t001.txt

Expected tagged-file format:
    token<TAB>lemma<TAB>pos<TAB>is_alpha<TAB>is_stop

Outputs:
    examples_txt/f<n>_<pole>/f<n>_<pole>_001.txt
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd


# ============================================================
# DEFAULTS
# ============================================================

DEFAULT_PROJECT = Path.cwd().name
DEFAULT_TAGGED_BASE = Path("corpus/07_tagged")
DEFAULT_FILE_IDS_PATH = Path("file_ids.txt")
DEFAULT_SCORE_DETAILS = Path("examples/score_details.txt")
DEFAULT_OUT_ROOT = Path("examples_txt")


# ============================================================
# ARGUMENTS
# ============================================================

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate plaintext examples for factor poles by VEm edition."
    )

    parser.add_argument(
        "--project",
        default=DEFAULT_PROJECT,
        help=(
            "Project name, e.g. cl_st1_claudia_vem. "
            "Default: current directory name."
        ),
    )
    parser.add_argument(
        "--sas-output-dir",
        default=None,
        help=(
            "Directory containing SAS outputs. "
            "Default: sas/output_<project>."
        ),
    )
    parser.add_argument(
        "--tagged-base",
        default=str(DEFAULT_TAGGED_BASE),
        help="Tagged corpus root. Default: corpus/07_tagged.",
    )
    parser.add_argument(
        "--file-ids",
        default=str(DEFAULT_FILE_IDS_PATH),
        help="Path to file_ids.txt.",
    )
    parser.add_argument(
        "--score-details",
        default=str(DEFAULT_SCORE_DETAILS),
        help="Path to examples/score_details.txt.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUT_ROOT),
        help="Output directory. Default: examples_txt.",
    )
    parser.add_argument(
        "--top-edition-examples",
        type=int,
        default=20,
        help="Number of examples for the top-ranked VEm edition.",
    )
    parser.add_argument(
        "--other-edition-examples",
        type=int,
        default=10,
        help="Number of examples for each other VEm edition.",
    )

    return parser.parse_args()


def resolve_sas_output_dir(project: str, sas_output_dir_arg: str | None) -> Path:
    """Resolve SAS output directory."""
    if sas_output_dir_arg is None:
        return Path("sas") / f"output_{project}"

    return Path(sas_output_dir_arg)


# ============================================================
# HELPERS
# ============================================================

def natural_sort_key(text: str) -> list[int | str]:
    """Return a natural-sort key that treats digit runs as integers."""
    parts = re.split(r"(\d+)", str(text))
    return [int(part) if part.isdigit() else part.lower() for part in parts]


def load_id_map(path: Path) -> dict[str, str]:
    """
    Load file-id to relative path map.

    Expected format:
        t000001 vem_ed_01/t001.txt
    """
    if not path.exists():
        raise FileNotFoundError(f"Required file missing: {path}")

    output: dict[str, str] = {}

    with path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()

            if not line:
                continue

            parts = line.split(maxsplit=1)

            if len(parts) != 2:
                raise ValueError(
                    f"Unexpected format in {path} at line {line_number}: "
                    "expected file_id and path."
                )

            file_id, relative_path = parts

            if line_number == 1 and file_id.lower() in {"file_id", "filename"}:
                raise ValueError(
                    f"{path} appears to contain a header. "
                    "Expected a headerless file."
                )

            output[file_id] = relative_path

    if not output:
        raise ValueError(f"No file IDs found in {path}")

    return output


def detect_factor_columns(scores_df: pd.DataFrame) -> list[str]:
    """Detect factor-score columns named fac1, fac2, etc."""
    factor_columns = [
        column for column in scores_df.columns
        if re.fullmatch(r"fac\d+", str(column))
    ]

    if not factor_columns:
        raise RuntimeError("No factor columns 'fac<n>' found in scores file.")

    return sorted(factor_columns, key=natural_sort_key)


def parse_score_details(path: Path, *, num_factors: int) -> dict[str, dict[str, list[str]]]:
    """
    Parse examples/score_details.txt.

    Returns:
        loading_words[tid]["f<n>_pos" or "f<n>_neg"] -> list[str]
    """
    if not path.exists():
        raise FileNotFoundError(
            f"Required file missing: {path}\n"
            "Run `python score_details.py` to generate it "
            "(expected output: examples/score_details.txt)."
        )

    output: dict[str, dict[str, list[str]]] = {}
    text = path.read_text(encoding="utf-8")
    blocks = text.split("=============================================")

    for block in blocks:
        match = re.search(r"text ID:\s*(t\d+)", block)

        if not match:
            continue

        text_id = match.group(1)
        output[text_id] = {}

        for factor_number in range(1, num_factors + 1):
            match_pos = re.search(
                rf"f{factor_number} pos words \(N=\d+\):\s*(.*)",
                block,
            )
            match_neg = re.search(
                rf"f{factor_number} neg words \(N=\d+\):\s*(.*)",
                block,
            )

            pos_words = match_pos.group(1).split(",") if match_pos else []
            neg_words = match_neg.group(1).split(",") if match_neg else []

            output[text_id][f"f{factor_number}_pos"] = [
                word.strip()
                for word in pos_words
                if word.strip()
            ]
            output[text_id][f"f{factor_number}_neg"] = [
                word.strip()
                for word in neg_words
                if word.strip()
            ]

    return output


def locate_tagged_text(
        row: pd.Series,
        id_map: dict[str, str],
        tagged_base: Path,
) -> Path | None:
    """Locate tagged text using file_ids.txt relative path."""
    text_id = row["filename"]
    relative_path = id_map.get(text_id)

    if not relative_path:
        return None

    path = tagged_base / relative_path

    if path.exists():
        return path

    return None


def reconstruct_plaintext_from_tagged(path: Path) -> str:
    """
    Reconstruct readable plaintext from a tagged TSV file.

    Expected format:
        token<TAB>lemma<TAB>pos<TAB>is_alpha<TAB>is_stop

    The token column is used. Header rows are skipped.
    """
    tokens: list[str] = []

    with path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.rstrip("\n")

            if not line:
                continue

            parts = line.split("\t")

            if len(parts) < 5:
                continue

            token, lemma, pos, is_alpha, is_stop = parts[:5]

            if line_number == 1 and token == "token" and lemma == "lemma" and pos == "pos":
                continue

            tokens.append(token)

    text = " ".join(tokens)

    # Basic spacing fixes for punctuation and brackets.
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    text = re.sub(r"\[\s+", "[", text)
    text = re.sub(r"\s+\]", "]", text)

    # Quotation spacing.
    text = re.sub(r"\s+([”’])", r"\1", text)
    text = re.sub(r"([“‘])\s+", r"\1", text)
    text = re.sub(r'\s+"', '"', text)
    text = re.sub(r'"\s+', '"', text)

    # Slash spacing.
    text = re.sub(r"\s+/\s+", "/", text)

    return text.strip()


def write_plaintext_example(
        *,
        outfile: Path,
        text_id: str,
        edition: str,
        tagged_path: Path,
        label: str,
        score_value,
        loading_words: list[str],
) -> None:
    """Write one plaintext example file."""
    header = [
        f"Text ID: {text_id}",
        f"Edition: {edition}",
        f"File:    {tagged_path}",
        "",
        f"Score ({label}): {score_value}",
        f"Loading words ({label}), N={len(loading_words)}: {', '.join(loading_words)}",
        "",
    ]

    body = reconstruct_plaintext_from_tagged(tagged_path)
    outfile.write_text("\n".join(header) + body + "\n", encoding="utf-8")


def read_edition_means(means_file: Path, factor_number: int) -> dict[str, float]:
    """Read VEm edition means for one factor."""
    if not means_file.exists():
        raise FileNotFoundError(f"Required means file missing: {means_file}")

    means_df = pd.read_csv(means_file, sep="\t")
    mean_column = f"Mean fac{factor_number}"

    if "edition" not in means_df.columns:
        raise ValueError(f"Column 'edition' missing in {means_file}")

    if mean_column not in means_df.columns:
        raise ValueError(f"Column '{mean_column}' missing in {means_file}")

    return dict(zip(
        means_df["edition"].astype(str).str.strip(),
        means_df[mean_column],
    ))


# ============================================================
# MAIN
# ============================================================

def main() -> None:
    """Run plaintext example generation."""
    args = parse_args()

    project = args.project
    sas_output_dir = resolve_sas_output_dir(project, args.sas_output_dir)
    tagged_base = Path(args.tagged_base)
    file_ids_path = Path(args.file_ids)
    score_details_path = Path(args.score_details)
    output_root = Path(args.output_dir)

    scores_file = sas_output_dir / f"{project}_scores_only.tsv"

    if not scores_file.exists():
        raise FileNotFoundError(f"Required file missing: {scores_file}")

    if not tagged_base.exists():
        raise FileNotFoundError(f"Tagged corpus root not found: {tagged_base}")

    output_root.mkdir(exist_ok=True, parents=True)

    id_map = load_id_map(file_ids_path)
    scores_df = pd.read_csv(scores_file, sep="\t")

    required_columns = {"filename", "edition"}
    missing_columns = required_columns - set(scores_df.columns)

    if missing_columns:
        raise ValueError(
            f"{scores_file} is missing required columns: "
            f"{', '.join(sorted(missing_columns))}"
        )

    scores_df["filename"] = scores_df["filename"].astype(str).str.strip()
    scores_df["edition"] = scores_df["edition"].astype(str).str.strip()

    factor_columns = detect_factor_columns(scores_df)
    num_factors = len(factor_columns)

    print(f"Project: {project}")
    print(f"Scores file: {scores_file}")
    print(f"Tagged corpus: {tagged_base}")
    print(f"Detected {num_factors} factors.\n")

    loading_words = parse_score_details(
        score_details_path,
        num_factors=num_factors,
    )

    missing_files: set[str] = set()
    missing_loading_words: set[tuple[str, str]] = set()

    for factor_number in range(1, num_factors + 1):
        factor_column = f"fac{factor_number}"

        if factor_column not in scores_df.columns:
            raise ValueError(
                f"Expected factor score column '{factor_column}' missing in {scores_file}"
            )

        means_file = sas_output_dir / f"means_edition_f{factor_number}.tsv"
        edition_means = read_edition_means(means_file, factor_number)

        for pole, ascending in (("pos", False), ("neg", True)):
            label = f"f{factor_number}_{pole}"

            print(
                f"→ {label}: selecting by VEm edition means "
                f"(column={factor_column}, ascending={ascending})"
            )

            ranked_editions = sorted(
                edition_means.keys(),
                key=lambda edition: edition_means[edition],
                reverse=not ascending,
            )

            if not ranked_editions:
                raise ValueError(f"No editions found in {means_file}")

            top_edition = ranked_editions[0]
            other_editions = ranked_editions[1:]

            sorted_df = scores_df.sort_values(by=factor_column, ascending=ascending)

            output_dir = output_root / label
            output_dir.mkdir(parents=True, exist_ok=True)

            example_id = 1

            # Top edition: 20 examples.
            top_edition_df = sorted_df[sorted_df["edition"] == top_edition]

            for _, row in top_edition_df.iterrows():
                if row[factor_column] == 0:
                    continue

                if example_id > args.top_edition_examples:
                    break

                tagged_path = locate_tagged_text(row, id_map, tagged_base)

                if not tagged_path or not tagged_path.exists():
                    missing_files.add(row["filename"])
                    continue

                text_id = row["filename"]
                label_words = loading_words.get(text_id, {}).get(label)

                if label_words is None:
                    missing_loading_words.add((text_id, label))
                    label_words = []

                outfile = output_dir / f"{label}_{example_id:03d}.txt"

                write_plaintext_example(
                    outfile=outfile,
                    text_id=text_id,
                    edition=str(row["edition"]).strip(),
                    tagged_path=tagged_path,
                    label=label,
                    score_value=row[factor_column],
                    loading_words=label_words,
                )

                example_id += 1

            # Other editions: 10 examples each.
            for edition in other_editions:
                edition_df = sorted_df[sorted_df["edition"] == edition]

                count = 0

                for _, row in edition_df.iterrows():
                    if row[factor_column] == 0:
                        continue

                    if count >= args.other_edition_examples:
                        break

                    tagged_path = locate_tagged_text(row, id_map, tagged_base)

                    if not tagged_path or not tagged_path.exists():
                        missing_files.add(row["filename"])
                        continue

                    text_id = row["filename"]
                    label_words = loading_words.get(text_id, {}).get(label)

                    if label_words is None:
                        missing_loading_words.add((text_id, label))
                        label_words = []

                    outfile = output_dir / f"{label}_{example_id:03d}.txt"

                    write_plaintext_example(
                        outfile=outfile,
                        text_id=text_id,
                        edition=str(row["edition"]).strip(),
                        tagged_path=tagged_path,
                        label=label,
                        score_value=row[factor_column],
                        loading_words=label_words,
                    )

                    count += 1
                    example_id += 1

            print(f"  ✓ Wrote {example_id - 1} examples for {label}\n")

    if missing_files:
        missing_path = Path("missing_files.txt")
        missing_path.write_text(
            "\n".join(sorted(missing_files)),
            encoding="utf-8",
        )
        print(f"⚠ Missing files written to {missing_path}")

    if missing_loading_words:
        report_path = Path("missing_loading_words.txt")
        report_path.write_text(
            "\n".join(
                f"{text_id}\t{label}"
                for text_id, label in sorted(missing_loading_words)
            ),
            encoding="utf-8",
        )
        print(f"⚠ Missing loading words written to {report_path}")

    print(f"\n✓ Done! All plaintext examples written to {output_root}/")


if __name__ == "__main__":
    main()