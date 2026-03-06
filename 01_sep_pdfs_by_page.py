"""
This script processes all PDF files in the 'pdf/' directory and splits them into individual pages.

Key Features:
- Uses the `pypdf` library to read and write PDF files.
- Iterates through all PDF files in the 'pdf/' directory.
- For multi-page PDFs, each page is saved as a separate file in the '01_pdf_sep/' directory with filenames indicating the page number (e.g., 'filename_page_1.pdf').
- For single-page PDFs, the file is saved directly in the '01_pdf_sep/' directory without appending a page number.
- Output files are stored in the '01_pdf_sep/' directory.

This script is useful for preparing PDFs for further processing by splitting them into manageable, single-page files.

Dependencies:
- `pypdf` library: Install it using `pip install pypdf`.
"""

from pypdf import PdfReader, PdfWriter
import glob

for src in glob.glob('pdf/*'):
    print(src)  # Log the source file path
    reader = PdfReader(src)
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        if len(reader.pages) > 1:  # Handle multi-page PDFs
            src = src.replace("pdf/", "").replace(".pdf", "")
            out_path = f"01_pdf_sep/{src}_page_{i+1}.pdf"
        else:  # Handle single-page PDFs
            src = src.replace("pdf/", "")
            out_path = f"01_pdf_sep/{src}"
        with open(out_path, "wb") as f:
            writer.write(f)

