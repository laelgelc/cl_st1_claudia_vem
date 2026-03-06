"""
This script recombines corrected text files from step eight ('08_json_txt_corrected/') into complete texts, handling both multipage and single-page files.

Key Features:
- Identifies multipage text files and recombines them into single files.
- Copies single-page text files directly to the output directory.
- Saves the recombined and copied files in the '09_recombined_txt/' directory.

Workflow Context:
- This script is used after corrections have been applied to the AI-generated text files in step eight.
- It ensures that multipage texts are recombined into their original form, while single-page texts are preserved as-is.

Dependencies:
- Standard Python libraries: `glob`, `re`, `os`.
"""

import glob
import re
import os

# Collect all corrected text files
texts_ls = []
for src in glob.glob('08_json_txt_corrected/*.txt'):
    texts_ls.append(src)

# Identify multipage text files
multipage_texts_ls = [i for i in texts_ls if '_page_' in i]
multipage_texts_ls = [re.sub(r'_page_.*', '', i) for i in multipage_texts_ls]
multipage_texts_ls = list(set(multipage_texts_ls))

# ---------------------
# Recombine multipage PDFs into single texts
# ---------------------
for src in multipage_texts_ls:
    page_files_ls = [
        i for i in texts_ls
        if f'{src}_page' in i
    ]
    page_files_ls.sort()

    pages_ls = []
    for p in page_files_ls:
        with open(p, "r") as f:
            pages_ls.append(f.read())
    txt = "\n".join(pages_ls)

    src_out = '09_recombined_txt/' + src.split('/')[1] + '.txt'

    with open(src_out, "w") as f:
        f.write(txt)

# ---------------------
# Copy single-page texts to the output directory
# ---------------------
singlepage_texts_ls = [i for i in texts_ls if '_page_' not in i]

for src in singlepage_texts_ls:
    cmd = f"cp '{src}' 09_recombined_txt/"
    os.system(cmd)

