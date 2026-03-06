"""
This script processes PDF files from the '01_pdf_sep/' directory and extracts their text and images.

Key Features:
- Uses the `fitz` library (PyMuPDF) to handle PDF processing.
- Extracts text from each PDF page and saves it as a `.txt` file in the '02_pdf_txt/' directory.
  The words in these text files will be used to determine if ChatGPT rendered words incorrectly.
- Renders each PDF page as an image and saves it as a `.jpg` file in the '02_pdf_img/' directory.
  These image files will be processed by ChatGPT using OCR strategies.
- The resolution of the images can be adjusted using the `zoom` parameter.

Dependencies:
- `fitz` library (PyMuPDF): Install it using `pip install pymupdf`.
"""

from pathlib import Path
import glob
import fitz

# Define zoom and transformation matrix for image rendering
zoom = 4  # 2 = 200%, 3 = 300%, 4 = 400% (controls resolution)
mat = fitz.Matrix(zoom, zoom)

for src in glob.glob('01_pdf_sep/*'):
    print(src)  # Log the source file path

    doc = fitz.open(src)  # Open the PDF file

    # Extract text and save as .txt
    src_out = '02_pdf_txt/' + Path(src).stem + '.txt'
    with open(src_out, 'w', encoding='utf-8') as txt_file:
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            txt_file.write(text + '\n')

    # Render pages as images and save as .jpg
    src_out = '02_pdf_img/' + Path(src).stem + '.jpg'
    for page_num, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=mat, alpha=False)
        pix.save(src_out)
