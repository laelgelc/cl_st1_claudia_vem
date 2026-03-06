"""
This script applies the corrections identified in step seven ('07_get corrections.py') to the AI-generated text files, creating corrected versions.

Key Features:
- Reads the corrections from the JSON file generated in step seven ('07_corrections/corrections.json').
- Copies the original AI-generated text files from '05_json_txt/' to '08_json_txt_corrected/'.
- Applies the substitutions to the copied files, replacing erroneous tokens with the correct ones.
- Saves the corrected files in the '08_json_txt_corrected/' directory.

Workflow Context:
- This script is used after the corrections have been compiled into a JSON file in step seven.
- It ensures that the AI-generated text files are updated with the corrections, creating a new set of corrected files for further processing or analysis.

Dependencies:
- Standard Python libraries: `json`, `re`, `os`.
"""

import json
import re
import os

# Define the base path for the project
my_path = "/Users/collenti/Documents/python/"

# Load corrections from the JSON file
with open("07_corrections/corrections.json", "r") as f:
    txt = f.read()

corrections_a = json.loads(txt)

# Copy the original AI-generated text files to the corrected directory
cmd = f"""
cp -R '{my_path}vem-corpus/05_json_txt/' '{my_path}vem-corpus/08_json_txt_corrected/'
""".strip()
os.system(cmd)

# Apply corrections to the copied files
for d in corrections_a:
    file = d['file']
    file = file.replace('05_json_txt', '08_json_txt_corrected')

    with open(file, "r") as f:
        txt = f.read()
    
    # Replace the target token with the substitution
    txt = re.sub(f"\\b{d['target']}\\b", d['substitution'], txt)
     
    with open(file, "w") as f:
        f.write(txt)
