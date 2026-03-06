"""
This script tags the recombined text files from step nine ('09_recombined_txt/') with lexical and morphological information.

Key Features:
- Reads text files from the '09_recombined_txt/' directory.
- Uses the `spacy` library to analyze each token and extract:
  - Token text
  - Lemma (base form of the word)
  - Part-of-speech (POS) tag
  - Whether the token is alphabetic
  - Whether the token is a stop word
- Saves the tagged output as tab-separated values (TSV) files in the '11_tagged/' directory.
- Includes a header row in the TSV files for clarity.

Workflow Context:
- This script is intended for researchers performing lexical and morphological analysis.
- Tagged text files provide detailed information about each token, enabling advanced linguistic analysis.

Dependencies:
- `spacy` library: Install it using `pip install spacy`.
- A small SpaCy model for Portuguese (`pt_core_news_sm`): Install it using `python -m spacy download pt_core_news_sm`.
"""

from pathlib import Path
import glob
import spacy

# Load SpaCy model for Portuguese
nlp = spacy.load("pt_core_news_sm")

for src in glob.glob('09_recombined_txt/*'):
    print(src)  # Log the source file path

    src_out = Path('11_tagged') / (Path(src).stem + '.tsv')    

    with open(src, "r") as f:
        txt = f.read()

    # Analyze tokens and extract lexical and morphological information
    doc = nlp(txt)
    tokens = [
        "\t".join([token.text, token.lemma_, token.pos_, str(token.is_alpha), str(token.is_stop)]) for token in doc
        if len(token.text.strip()) > 0
    ]

    # Add header row to the TSV file
    header = "token\tlemma\tpos\tis_alpha\tis_stop"
    tokens = [header] + tokens

    # Save tagged output
    res = "\n".join(tokens)
    with open(src_out, "w") as f:
        f.write(res)
