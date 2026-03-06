"""
This script tokenizes the recombined text files from step nine ('09_recombined_txt/') to prepare them for keyword analysis.

Key Features:
- Reads text files from the '09_recombined_txt/' directory.
- Uses the `spacy` library to tokenize the text into individual words or tokens.
- Saves the tokenized output as newline-separated tokens in the '10_tokenized/' directory.

Workflow Context:
- This script is intended for researchers performing keyword analysis.
- Tokenized text files make it easier to analyze word frequency, identify patterns, and extract meaningful keywords.

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

    src_out = Path('10_tokenized') / (Path(src).stem + '.txt')    

    with open(src, "r") as f:
        txt = f.read()

    # Tokenize the text
    doc = nlp(txt)
    tokens = [
        t.text.strip() for t in doc
        if len(t.text.strip()) > 0
    ]

    # Save tokenized output
    res = "\n".join(tokens)
    with open(src_out, "w") as f:
        f.write(res)

