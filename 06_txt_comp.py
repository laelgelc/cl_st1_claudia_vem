"""
This script compares AI-generated text files from the '05_json_txt/' directory with the original text dumps from the '02_pdf_txt/' directory to identify suspicious tokens.

Key Features:
- Uses the `spacy` library for natural language processing.
- Identifies tokens in the AI-generated text that are not present in the original text dump.
- Filters out tokens listed in the `06_excludes.txt` file.
- Calculates normalized Levenshtein distances between suspicious tokens and original tokens.
- Retrieves Key Word In Context (KWIC) for suspicious tokens in both AI-generated and original texts.
- Outputs the comparison results to the '06_txt_comp/' directory.

Explanation for Colleagues:
- The goal of this script is to identify potential errors in the AI-generated text by comparing it to the raw text extracted from the original PDF files.
- Levenshtein distance is used to measure the similarity between two strings. It calculates the minimum number of single-character edits (insertions, deletions, or substitutions) required to change one word into another.
- The script identifies tokens (words) in the AI-generated text that do not appear in the raw text. These tokens are flagged as "suspicious" because they might be incorrect representations of the original text.
- For each suspicious token, the script calculates its similarity to all tokens in the raw text using normalized Levenshtein distance (a value between 0 and 1, where 1 means identical).
- Tokens in the raw text with a similarity score above a certain threshold (0.5) are considered "close matches" to the suspicious token.
- The script retrieves the context (KWIC) for both the suspicious token and its close matches, making it easier to analyze the discrepancies manually.
- This process helps narrow down the potential errors, making the manual review more manageable.

Dependencies:
- `spacy` library: Install it using `pip install spacy`.
- `levenstein` and `kwics` modules for distance calculation and KWIC extraction.
- A small SpaCy model for Portuguese (`pt_core_news_sm`): Install it using `python -m spacy download pt_core_news_sm`.
"""

from pathlib import Path
import glob
import spacy
from levenstein import normalized_levenshtein
from kwics import get_kwic

# Load SpaCy model for Portuguese
nlp = spacy.load("pt_core_news_sm")

# Load suspicious tokens to exclude
with open("06_excludes.txt", "r") as f:
    suspicious_lemmas_excludes_ls = f.read().strip().splitlines()

# Helper function to get indices and values above a threshold
def indices_and_values_above_threshold(values, threshold):
    results = [(i, v) for i, v in enumerate(values) if v > threshold]
    return sorted(results, key=lambda x: x[1], reverse=True)

for src in glob.glob('05_json_txt/*'):
    print(src)  # Log the source file path

    src_out = Path('06_txt_comp') / (Path(src).stem + '.txt')
    src_orig = Path('02_pdf_txt') / (Path(src).stem + '.txt')

    with open(src, "r") as f:
        txt = f.read()

    with open(src_orig, "r") as f:
        txt_orig = f.read()

    # Process text with SpaCy
    doc = nlp(txt)
    doc_orig = nlp(txt_orig)

    tokens = [t.text.strip() for t in doc if len(t.text.strip()) > 0]
    tokens_orig = [t.text.strip() for t in doc_orig if len(t.text.strip()) > 0]

    tokens_uniq = list(set(tokens))
    tokens_orig_uniq = list(set(tokens_orig))

    # Identify suspicious tokens
    suspicious_tokens_ls = [
        t for t in tokens_uniq
        if t not in tokens_orig_uniq and t not in suspicious_lemmas_excludes_ls
    ]

    for t in suspicious_tokens_ls:
        # Calculate Levenshtein distances for suspicious tokens
        similarities_ls = [
            normalized_levenshtein(t, t_orig_uniq) for t_orig_uniq in tokens_orig_uniq
        ]

        # Get KWIC for the token in AI-generated text
        t_kwics_s = get_kwic(t, doc)

        # Get KWIC for similar tokens in original text
        t_similar_kwics_ls = []
        most_similar_indices = indices_and_values_above_threshold(similarities_ls, 0.49)
        for i, lev in most_similar_indices:
            lev_s = str(round(lev, 2))
            kwics_s = get_kwic(tokens_orig_uniq[i], doc_orig) + f"\n{lev_s}"
            t_similar_kwics_ls.append(kwics_s)
        t_similar_kwics_s = "\n".join(t_similar_kwics_ls).strip() or "***NONE***"

        # Write results to output file
        if t_similar_kwics_s != "***NONE***" and len(txt_orig.strip()) > 0:
            res_ls = [
                "-----------------------------",
                f"TEXT: {src}",
                f"TOKEN:\n{t}\n",
                f"=====\nAI CONTEXT:\n{t_kwics_s}\n",
                f"=====\nORIG CONTEXT(S):\n{t_similar_kwics_s}"
            ]

            res = "\n".join(res_ls) + "\n\n"

            with open(src_out, "a") as f:
                f.write(res)