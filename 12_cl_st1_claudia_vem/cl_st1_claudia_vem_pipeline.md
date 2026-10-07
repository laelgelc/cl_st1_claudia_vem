# Lexical Multi-dimensional Analysis (LMDA) Pipeline

This document organises the processing pipeline for the **Lexical Multi-dimensional Analysis (LMDA)** of the VEm corpus.

It is **not intended to be run as a Bash script**. Commands are included only as documentation of the processing sequence.

---

## 1. Organise the Corpus

**Purpose:** Prepare the corpus structure for LMDA processing.
```bash
python 01_org_corpus.py
```
---

## 2. Generate Key Lemmas

**Purpose:** Identify key lemmas from the tagged corpus.
```bash
python keylemmas.py \
    --input corpus/07_tagged \
    --output corpus/08_keylemmas \
    --cutoff 3
```
**Output:**
```text
corpus/08_keylemmas/
```
---

## 3. Select Keywords

### Deprecated method

The previous keyword-selection method is retained for reference only.
```bash
python select_keywords_deprecated.py --num-keywords 40
```
**Output:**
```text
corpus/09_kw_selected/
```
### Current method: stratified keyword selection (deprecated)

**Purpose:** Select keywords by edition, with a maximum quota per VEm edition.
```bash
python select_kws_stratified.py \
    --per-edition 200 \
    --max-total 0
```
**Output:**
```text
corpus/09_kw_selected_deprecated_2/
```
### Keyword-selection summary

Each VEm edition is allowed up to **200 keywords**.

The final selection produced:

- **1,990** consolidated keywords before de-duplication
- **1,321** unique keywords after de-duplication
- **669** duplicates removed

Final output:
```text
corpus/09_kw_selected/keywords.txt
```
Final unique keyword count:
```text
1321
```

### Current method: stratified keyword selection

**Purpose:** Select keywords by edition, with a maximum quota per VEm edition.
```bash
python select_kws_stratified.py \
    --per-edition 2 \
    --max-total 0
```
**Output:**
```text
corpus/09_kw_selected/
```
### Keyword-selection summary

Each VEm edition is allowed up to **200 keywords**.

The final selection produced:

- **1,990** consolidated keywords before de-duplication
- **1,321** unique keywords after de-duplication
- **669** duplicates removed

Final output:
```text
corpus/09_kw_selected/keywords.txt
```
Final unique keyword count:
```text
1321
```

---

## 4. Reset Column Outputs

**Purpose:** Remove previously generated keyword-column folders before rebuilding them.
```bash
rm -rf columns columns_clean
```
---

## 5. Generate Keyword-Presence Columns

**Purpose:** Create binary keyword-presence columns for each text in the tagged corpus.
```bash
python columns.py
```
**Outputs:**
```text
columns/
columns_clean/
file_ids.txt
index_keywords.txt
```
---

## 6. Merge Keyword Columns for SAS

**Purpose:** Merge individual keyword-presence columns into a single count matrix for SAS.
```bash
python merge_columns.py
```
**Output:**
```text
sas/counts.txt
```
---

## 7. Generate SAS Formats

**Purpose:** Generate SAS format files for keyword labels and related metadata.
```bash
python sas_formats.py
```
**Outputs:**
```text
sas/word_labels_format.sas
sas/word_labels_full_format.sas
```
Additional SAS format files may also be generated.

---

## 8. Run SAS Factor Analysis

**Purpose:** Run the LMDA factor-analysis stage in SAS.

This step is performed outside the Python pipeline.

**Account:**
```text
Rogerio Yamada's account
```
**Input:**
```text
sas/cl_st1_claudia_vem.sas
sas/counts.txt
sas/word_labels_format.sas
sas/word_labels_full_format.sas
```
**Expected SAS output directory:**
```text
sas/output_cl_st1_claudia_vem/
```
---

## 9. Generate Factor Lists

**Purpose:** Extract and organise factor lists from SAS output.
```bash
python factor_lists.py \
    --project cl_st1_claudia_vem \
    --sas-output-dir sas/output_cl_st1_claudia_vem
```
**Output:**
```text
factors/
```
---

## 10. Calculate Corpus Size

**Purpose:** Calculate corpus-size information for the analysed dataset.
```bash
python corpus_size.py
```
**Output:**
```text
corpus_size/corpus_size.tsv
```
---

## 11. Generate LaTeX Boxplots

**Purpose:** Build boxplots for the factor-analysis results.
```bash
cd latex_boxplots
python latex_boxplots.py \
    --project cl_st1_claudia_vem \
    --sas-output-dir ../sas/output_cl_st1_claudia_vem
cd ..
```
**Output:**
```text
latex_boxplots/slides/
```
---

## 12. Generate LaTeX ANOVA Tables

**Purpose:** Generate LaTeX tables from the SAS ANOVA output.
```bash
python latex_anova_table.py \
    --project cl_st1_claudia_vem \
    --input-dir sas/output_cl_st1_claudia_vem
```
**Output:**
```text
latex_tables/
```
---

## 13. Generate Examples in LaTeX Format

**Purpose:** Extract representative examples for factor interpretation in LaTeX format.
```bash
python examples.py \
    --project cl_st1_claudia_vem \
    --sas-output-dir sas/output_cl_st1_claudia_vem
```
**Output:**
```text
examples/
```
---

## 14. Check Score Details

**Purpose:** Perform a sanity check on factor scores.
```bash
python score_details.py \
    --project cl_st1_claudia_vem \
    --sas-output-dir sas/output_cl_st1_claudia_vem
```
**Output:**
```text
examples/score_details.txt
```
---

## 15. Generate Examples in Plain Text Format

**Purpose:** Extract representative examples for factor interpretation in plain text format.
```bash
python examples_txt.py \
    --project cl_st1_claudia_vem \
    --sas-output-dir sas/output_cl_st1_claudia_vem
```
**Output:**
```text
examples_txt/
```
---

## 16. Prepare Interpretation Prompts

**Purpose:** Build prompts for factor interpretation.
```bash
python interpretation_prompts.py \
    --project cl_st1_claudia_vem \
    --sas-output-dir sas/output_cl_st1_claudia_vem
```
**Output:**
```text
interpretation/input/
```
---

## 17. Generate Factor Interpretations

**Purpose:** Submit interpretation prompts to the language model and save generated interpretations.
```bash
python generate_interpretation_gpt.py \
    --input interpretation/input \
    --output interpretation/output \
    --model gpt-5.5 \
    --workers 4
```
**Output:**
```text
interpretation/output/
```
---

# Pipeline Overview

The LMDA workflow proceeds through the following major stages:

1. **Corpus organisation**
2. **Key-lemma extraction**
3. **Stratified keyword selection**
4. **Keyword-presence column generation**
5. **Column merging for SAS**
6. **SAS factor analysis**
7. **Factor-list extraction**
8. **Corpus-size calculation**
9. **Visualisation and table generation**
10. **Example extraction**
11. **Score checking**
12. **Interpretation prompt generation**
13. **Automated interpretation generation**

---

# Main Outputs

| Stage                     | Output                               |
|---------------------------|--------------------------------------|
| Key lemmas                | `corpus/08_keylemmas/`               |
| Selected keywords         | `corpus/09_kw_selected/keywords.txt` |
| Keyword columns           | `columns/`                           |
| Clean keyword columns     | `columns_clean/`                     |
| File ID index             | `file_ids.txt`                       |
| Keyword index             | `index_keywords.txt`                 |
| SAS input matrix          | `sas/counts.txt`                     |
| Factor lists              | `factors/`                           |
| Corpus size table         | `corpus_size/corpus_size.tsv`        |
| Boxplot slides            | `latex_boxplots/slides/`             |
| LaTeX tables              | `latex_tables/`                      |
| LaTeX examples            | `examples/`                          |
| Plain-text examples       | `examples_txt/`                      |
| Score details             | `examples/score_details.txt`         |
| Interpretation prompts    | `interpretation/input/`              |
| Generated interpretations | `interpretation/output/`             |


