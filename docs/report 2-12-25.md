# Methodology for Extracting Text from Layout-Based PDF Newsletters

The objective of this project was to reconstruct clean, sequential textual corpora from a collection of PDF newsletters originally produced with layout software. Because such software prioritizes visual positioning over logical reading order, direct text export from the PDFs resulted in fragmented sentences, disjointed paragraphs, and disrupted sequencing. To overcome this limitation, a multi-stage workflow was developed in Python using both traditional PDF processing tools and OpenAI’s multimodal APIs.

## 1. Page-Level Processing

Each newsletter PDF was first divided into single-page files. This ensured that each page could be processed independently and reduced complexity during image conversion and OCR. Multi-page newsletters were separated into individual page files, while single-page newsletters remained unchanged.

## 2. Parallel Text and Image Extraction

For each page-level PDF, two outputs were generated:

A direct text extraction using a PDF library. This output was preserved for comparison purposes, even though it retained layout-related fragmentation.

A high-resolution image rendering of the page. The image was generated at enhanced resolution to optimize OCR accuracy during AI processing.

The image files became the primary input for structured text reconstruction.

## 3. AI-Based OCR with Structured Output

Each page image was submitted to OpenAI’s multimodal API with a carefully engineered prompt designed specifically for corpus reconstruction. The prompt instructed the model to:

Extract only communicatively meaningful textual content.

Exclude mastheads, boilerplate footers, graphic captions, and decorative or layout-only elements.

Preserve original language without translation or normalization.

Return the output in a structured JSON schema (including title, subtitle, and section headings with paragraphs).

Each processed page produced a corresponding JSON file representing the logically ordered text of that page.

## 4. Post-Processing and Pattern Filtering

After reviewing the structured outputs, certain recurring non-content patterns were identified (e.g., standardized administrative notices or repeated institutional blocks). A subsequent Python script applied targeted pattern-based filtering to remove these elements from the JSON files. Cleaned versions were saved separately to preserve a transparent processing trail.

## 5. Conversion to Plain Text

The cleaned JSON structures were then converted into plain-text format. Structural markers (titles, headings, paragraphs, lists) were flattened into a linear sequence while preserving reading order. This produced page-level text files suitable for corpus compilation and linguistic analysis.

## 6. Recombination of Multi-Page Newsletters

Finally, another Python routine recombined individual page-level text files into complete newsletter documents, restoring multi-page sequencing. Single-page newsletters were simply transferred into the final output directory.

## TO DO

1. I am in the process of comparing the resulting text files and the original text version of the PDFs. The purpose of this process is to determine whether ChatGPT inserted words that were not present in the original newsletters. A preliminary analysis indicates that the prompt that I used to extract text did not lead to the introduction of words and terms not originally present.

2. Once that last process is complete, I will use spacy to tag the files.
