# VEM Corpus

# PDF → Text Corpus Processing Pipeline

This repository contains a multi-step pipeline for converting PDF documents into clean, tokenized, and linguistically tagged text suitable for corpus analysis.

Each script represents one stage in the workflow. The leading numbers in the filenames indicate the **order of processing**.

---


# Step-by-Step Pipeline Description

## 01_sep_pdfs_by_page.py

**Purpose**

Splits source PDF documents into individual pages.

**Process**

All PDFs in the `pdf/` directory are processed. Multi-page PDFs are divided into single-page files so that each page can be handled independently in later OCR stages.

**Output**

```
01_pdf_sep/
```

Single-page PDF files.

---

## 02_pdf_to_txt_and_img.py

**Purpose**

Extracts both raw text and page images from each single-page PDF.

**Process**

Each PDF page from `01_pdf_sep/` is processed using PyMuPDF.

Two outputs are produced:

- A **raw text extraction** used later for error comparison.
- A **high-resolution image** used for AI-based OCR.

**Outputs**

```
02_pdf_txt/
02_pdf_img/
```

---

## 03_jpg_to_json.py

**Purpose**

Performs structured OCR using an AI model.

**Process**

Each `.jpg` image from `02_pdf_img/` is encoded in Base64 and sent to an AI model with a custom extraction prompt.  
The model returns **structured JSON representing the page’s textual content**.

**Output**

```
03_pdf_json/
```

---

## 04_cleanup_json.py

**Purpose**

Removes unwanted sections from the AI-generated JSON.

**Process**

JSON files from `03_pdf_json/` are cleaned by removing sections matching predefined patterns, such as boilerplate structures or recurring non-content elements.

**Output**

```
04_json_cleaned/
```

---

## 05_json_to_txt.py

**Purpose**

Converts cleaned JSON into plain text.

**Process**

Relevant textual fields such as:

- titles  
- headings  
- paragraphs  

are extracted and combined into readable text files.

**Output**

```
05_json_txt/
```

---

## 06_txt_comp.py

**Purpose**

Detects potential OCR errors.

**Process**

The AI-generated text (`05_json_txt/`) is compared against the raw PDF extraction (`02_pdf_txt/`).

The script:

- identifies tokens present in the AI text but absent in the PDF text  
- applies **normalized Levenshtein distance**  
- produces **KWIC (keyword-in-context) displays**

These files are intended for **manual inspection**.

**Output**

```
06_txt_comp/
```

---

## 07_get_corrections.py

**Purpose**

Extracts manual corrections.

**Process**

After reviewing the comparison files, the user marks corrections with:

```
___SUB___
```

This script extracts those corrections and compiles them into structured correction lists.

**Output**

```
07_corrections/
```

---

## 08_make_corrections.py

**Purpose**

Applies corrections to the AI-generated text.

**Process**

The correction lists produced in Step 7 are applied to the text files from `05_json_txt/`, generating corrected versions.

**Output**

```
08_json_txt_corrected/
```

---

## 09_recombine_txts.py

**Purpose**

Reconstructs full documents.

**Process**

Page-level text files belonging to the same document are merged back together.  
Single-page documents are copied unchanged.

**Output**

```
09_recombined_txt/
```

---

## 10_tokenize.py

**Purpose**

Tokenizes the cleaned corpus.

**Process**

SpaCy is used to segment each document into tokens.

Tokens are written as **newline-separated entries** for corpus analysis.

**Output**

```
10_tokenized/
```

---

## 11_tag.py

**Purpose**

Adds linguistic annotation.

**Process**

SpaCy analyzes each token and produces annotations including:

- token  
- lemma  
- part-of-speech  
- alphabetic status  
- stopword status  

**Output**

```
11_tagged/
```

Output files are written in **TSV format**, suitable for corpus linguistics workflows.

---

# Final Corpus Outputs

### Tokenized corpus

```
10_tokenized/
```

### Linguistically tagged corpus

```
11_tagged/
```

These outputs can be used for:

- keyword analysis  
- frequency analysis  
- collocation analysis  
- corpus-based linguistic research