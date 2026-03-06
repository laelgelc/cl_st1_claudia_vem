"""
This script converts cleaned JSON files from the '04_json_cleaned/' directory into plain text files.

Key Features:
- Reads JSON files from the '04_json_cleaned/' directory.
- Extracts specific fields such as `title`, `subtitle`, `heading`, and `paragraphs`.
- Converts the extracted content into plain text format.
- Saves the resulting text files in the '05_json_txt/' directory.

Dependencies:
- Standard Python libraries: `pathlib`, `glob`, `json`.
"""

from pathlib import Path
import glob
import json

# Function to safely get a value for a given key from a dictionary
def get_key_val(d_in, k):
    res = ""
    if d_in[k] is not None:
        res = d_in[k]
    return res

# Filter out files that already exist in the output directory
input_files = glob.glob('04_json_cleaned/*')
output_files = {Path(f).stem for f in glob.glob('05_json_txt/*')}
files_to_process = [src for src in input_files if Path(src).stem not in output_files]

for src in files_to_process:
    print(src)  # Log the source file path

    src_out = Path('05_json_txt') / (Path(src).stem + '.txt')

    with open(src, "r") as f:
        txt = f.read()
    
    d = json.loads(txt)

    """
    Assumes JSON structure:
    {
    "title": "string | null",
    "subtitle": "string | null",
    "sections": [
        {
        "heading": "string | null",
        "paragraphs": [
            "string",
            { "list": ["string"] }
        ]
        }
    ]
    }
    """

    txt_ls = []

    txt_ls.append(get_key_val(d, 'title'))
    txt_ls.append(get_key_val(d, 'subtitle'))

    for sec_d in d['sections']:
        txt_ls.append(get_key_val(sec_d, 'heading'))

        paras_ls = get_key_val(sec_d, 'paragraphs')
        if paras_ls is not None and len(paras_ls) > 0:
            for obj in paras_ls:
                if isinstance(obj, str):
                    txt_ls.append(obj)
                if isinstance(obj, dict):
                    s = "\n".join(li for li in obj['list'])
                    txt_ls.append(s)

    txt_s = "\n".join(txt_ls)
    with open(src_out, "w") as f:
        f.write(txt_s)