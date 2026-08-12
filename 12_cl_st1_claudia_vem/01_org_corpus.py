"""
Organise tagged corpus files by edition.

This script reads all TSV files from 11_tagged, assigns each file a new
sequential name in the format tNNN.txt, writes the filename mapping to
12_cl_st1_claudia/file_index.txt, and copies the files into
12_cl_st1_claudia/corpus/07_tagged/vem_ed_NN/ according to the edition number
encoded in the original filename.
"""
from pathlib import Path
import re
import shutil


BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "11_tagged"
TARGET_ROOT = BASE_DIR / "12_cl_st1_claudia"
INDEX_PATH = TARGET_ROOT / "file_index.txt"
CORPUS_DIR = TARGET_ROOT / "corpus" / "07_tagged"

FILENAME_PATTERN = re.compile(r"(?i)^vem[-_](\d{2})[.-](\d+)$")


def parse_filename(file_path: Path) -> tuple[str, int]:
    """
    Return:
    - edition number as two digits
    - document/page number as integer

    Supported examples:
    - VEm_01.1.tsv
    - VEm-17-3.tsv
    - VEm_30.05.tsv
    """
    stem = file_path.stem
    match = FILENAME_PATTERN.match(stem)
    if not match:
        raise ValueError(f"Unrecognized filename format: {file_path.name}")

    edition = match.group(1)
    part_number = int(match.group(2))
    return edition, part_number


def get_source_files() -> list[Path]:
    """
    Collect and sort all TSV files from 11_tagged using numeric filename order.
    """
    if not SOURCE_DIR.exists():
        raise FileNotFoundError(f"Source directory not found: {SOURCE_DIR}")

    files = [path for path in SOURCE_DIR.iterdir() if path.is_file() and path.suffix.lower() == ".tsv"]

    if not files:
        raise FileNotFoundError(f"No .tsv files found in: {SOURCE_DIR}")

    return sorted(files, key=lambda path: (*parse_filename(path), path.stem.lower()))


def organise_corpus() -> None:
    source_files = get_source_files()

    TARGET_ROOT.mkdir(parents=True, exist_ok=True)
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)

    index_lines: list[str] = []

    for i, source_path in enumerate(source_files, start=1):
        edition, _ = parse_filename(source_path)
        new_filename = f"t{i:03d}.txt"

        destination_dir = CORPUS_DIR / f"vem_ed_{edition}"
        destination_dir.mkdir(parents=True, exist_ok=True)

        destination_path = destination_dir / new_filename
        shutil.copy2(source_path, destination_path)

        index_lines.append(f"{new_filename} {source_path.stem}")

    INDEX_PATH.write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    print(f"Created index: {INDEX_PATH}")
    print(f"Copied {len(source_files)} files into: {CORPUS_DIR}")


if __name__ == "__main__":
    organise_corpus()