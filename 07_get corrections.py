"""
This script processes the output from step six ('06_txt_comp/') to extract corrections identified by the researcher and compiles them into a JSON file.

Key Features:
- Reads text files from the '06_txt_comp/' directory.
- Identifies tokens marked with '___SUB___' as requiring substitution.
- Extracts the original token, the substitution, and the file where the correction is needed.
- Saves the corrections as a JSON file in the '07_corrections/' directory.

Workflow Context:
- This script is used after the researcher has manually reviewed the output from step six and marked substitutions in the text files.
- Example of a marked substitution:
  -----------------------------
  TEXT: 05_json_txt/VEm_03.4.txt
  TOKEN:
  contribuiu

  =====
  AI CONTEXT:
  do encontro virtual [contribuiu] para reforçar esses

  =====
  ORIG CONTEXT(S):
  _EOL_ encontro virtual [contribui] para _EOL_ reforçar ___SUB___
  0.9
  _EOL_ Mona Pearl [contou] que a _EOL_
  0.5

- In this example, the token 'contribuiu' was not present in the original text and was flagged as a potential error. The researcher identified 'contribui' as the correct substitution.
- The script extracts the substitution ('contribui' in this example) and compiles it into a structured JSON file for further processing.

Dependencies:
- `pandas` library: Install it using `pip install pandas`.
- Standard Python libraries: `glob`, `re`.
"""

import glob
import pandas as pd
import re

# Create empty DataFrame with specified columns
df = pd.DataFrame(columns=["file", "target", "substitution"])

for src in glob.glob('06_txt_comp/*'):
    print(src)  # Log the source file path
    with open(src, 'r') as f:
        txt = f.read().strip()
    
    ls = txt.split('-----------------------------')
    ls = [i.strip() for i in ls if len(i.strip()) > 0]
    
    for t in ls:
        if '___SUB___' in t:
            file = re.findall(r'TEXT: ([^\n]+)', t)[0]
            target = re.findall(r'TOKEN:\n([^\n]+)', t)[0]
            
            # Find the substitution
            orig_ls = t.split('ORIG CONTEXT(S):')[1].splitlines()
            orig = [o for o in orig_ls if '___SUB___' in o][0]
            substitution = re.findall(r'\[([^\]]+)\]', orig)[0]
            
            row = {
                'file': file,
                'target': target,
                'substitution': substitution
            }
            df.loc[len(df)] = row

# Save corrections to JSON file
df.to_json(
    '07_corrections/corrections.json',
    force_ascii=False,
    indent=4,
    orient="records"
)
