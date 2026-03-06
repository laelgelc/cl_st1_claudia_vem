from pathlib import Path

"""
These are the necessary folders. If a folder does not exist, it is created.
"""

folders_ls = """
pdf
01_pdf_sep
02_pdf_img
02_pdf_txt
03_pdf_json
04_json_cleaned
05_json_txt
06_txt_comp
07_corrections
08_json_txt_corrected
09_recombined_txt
10_tokenized
11_tagged
""".strip().splitlines()

for f in folders_ls:

    dir_path = Path(f)

    if not dir_path.exists():
        dir_path.mkdir(parents=True)
