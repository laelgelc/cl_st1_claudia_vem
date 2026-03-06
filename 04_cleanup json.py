"""
This script cleans up JSON files in the '03_pdf_json/' directory by removing unwanted keys and sections based on specified patterns.

Key Features:
- Reads JSON files from the '03_pdf_json/' directory.
- Removes keys and sections that match patterns defined in the `targets` variable.
- Outputs cleaned JSON files to the '04_json_cleaned/' directory.
- Ensures the structure of the JSON files remains intact while excluding unwanted data.

Dependencies:
- Standard Python libraries: `re`, `json`, `glob`, `itertools`, `pathlib`.
"""

import re
import json
import glob
from itertools import chain
from pathlib import Path

# Define patterns for keys and sections to exclude
targets = """
heading__TAB__.*Expediente.*
heading__TAB__.*Fale conosco.*
title__TAB__.*Fale conosco.*"
"""

targets_ls = targets.strip().splitlines()
targets_ls = [a.split("__TAB__") for a in targets_ls]

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

for src in glob.glob('03_pdf_json/*'):
    print(src)  # Log the source file path

    with open(src, "r") as f:
        txt = f.read()
    
    src_out = Path('04_json_cleaned') / (Path(src).stem + '.json')

    d = json.loads(txt)

    dels_ls = [[], []]
    non_sections_ls = [k for k in d.keys() if k != 'sections']
    for i in range(0, len(non_sections_ls)):
        k = non_sections_ls[i]
        s = str(d[k])
        exclude = False
        for target_kv in targets_ls:
            if target_kv[0] == k:
                val = d[k]
                pat = target_kv[1]
                if val is not None and re.search(target_kv[1], d[k]):
                    dels_ls[0].append(k)
                    exclude = True
                    break

    if 'sections' in [k for k in d.keys()]:
        for i in range(0, len(d['sections'])):
            sec = d['sections'][i]
            s = str(sec)
            exclude = False
            for target_kv in targets_ls:
                k2 = target_kv[0]
                if k2 in sec.keys():
                    val = sec[k2]
                    pat = target_kv[1]
                    if val is not None and re.search(pat, val):
                        dels_ls[1].append(i)
                        exclude = True
                        break

    flat = list(chain.from_iterable(dels_ls))
    if len(flat) > 0:

        print(src)

        if len(dels_ls[0]) > 0:
            for k in dels_ls[0]:
                del d[k]

        # Remove sections
        if len(dels_ls[1]) > 0:
            to_remove = set(dels_ls[1])
            sections_ls = d['sections']
            sections_ls = [x for i, x in enumerate(sections_ls) if i not in to_remove]
            d['sections'] = sections_ls

    with open(src_out, "w") as f:
        d_s = json.dumps(d, indent=2, ensure_ascii=False)
        f.write(d_s)
