python 01_org_corpus.py

python keylemmas.py \
    --input corpus/07_tagged \
    --output corpus/08_keylemmas \
    --cutoff 3

#python select_keywords_deprecated.py --num-keywords 40
# Output: corpus/09_kw_selected



"
=== Keyword Quotas ===
generic_gpt     → 250 keywords (max)
human           → 500 keywords (max)
summary_guided_gpt → 250 keywords (max)
=======================

generic_gpt     → selected 76/250 keywords
human           → selected 46/500 keywords
summary_guided_gpt → selected 45/250 keywords

Total consolidated keywords (incl. duplicates): 167
Unique keywords (used downstream): 140
Duplicates removed later: 27

Final unique keywords written: 140
"

rm -rf columns columns_clean
python columns.py
# Output: columns, columns_clean, file_ids.txt, index_keywords.txt

python merge_columns.py
# Output: sas/counts.txt

python sas_formats.py
# Output: sas/word_labels_format.sas, etc

## RUN SAS
## Rogerio Yamada's account

python factor_lists.py
# Output: factors

python corpus_size.py
# Output: corpus_size/corpus_size.tsv

cd latex_boxplots
# Builds boxplots for factor analysis:
python latex_boxplots.py
# Output: latex_boxplots/slides
cd ..

python latex_anova_table.py
# Output: latex_tables

python examples.py
# Output: examples (LaTeX format)

# Sanity check on the scores:
python score_details.py
# Output: examples/score_details.txt

python examples_txt.py
# Output: examples_txt (plaintext format)

# Interpretation
# Build prompts:
python interpretation_prompts.py
# Output: interpretation/input

# Submit prompts:
python generate_interpretation_gpt.py \
    --input interpretation/input \
    --output interpretation/output \
    --model gpt-5.1 \
    --workers 4
# Output: interpretation/output