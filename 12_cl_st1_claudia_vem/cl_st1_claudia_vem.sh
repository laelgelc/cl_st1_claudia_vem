python 01_org_corpus.py

python keylemmas.py \
    --input corpus/07_tagged \
    --output corpus/08_keylemmas \
    --cutoff 3

#python select_keywords_deprecated.py --num-keywords 40
# Output: corpus/09_kw_selected

python select_kws_stratified.py \
    --per-edition 200 \
    --max-total 0
# Output: corpus/09_kw_selected

"
=== VEm Edition Keyword Quotas ===
vem_ed_01  → 200 keywords max
vem_ed_02  → 200 keywords max
vem_ed_03  → 200 keywords max
vem_ed_04  → 200 keywords max
vem_ed_05  → 200 keywords max
vem_ed_06  → 200 keywords max
vem_ed_07  → 200 keywords max
vem_ed_08  → 200 keywords max
vem_ed_09  → 200 keywords max
vem_ed_10  → 200 keywords max
vem_ed_11  → 200 keywords max
vem_ed_12  → 200 keywords max
vem_ed_13  → 200 keywords max
vem_ed_14  → 200 keywords max
vem_ed_15  → 200 keywords max
vem_ed_16  → 200 keywords max
vem_ed_17  → 200 keywords max
vem_ed_18  → 200 keywords max
vem_ed_19  → 200 keywords max
vem_ed_20  → 200 keywords max
vem_ed_21  → 200 keywords max
vem_ed_22  → 200 keywords max
vem_ed_23  → 200 keywords max
vem_ed_24  → 200 keywords max
vem_ed_25  → 200 keywords max
vem_ed_26  → 200 keywords max
vem_ed_27  → 200 keywords max
vem_ed_28  → 200 keywords max
vem_ed_29  → 200 keywords max
vem_ed_30  → 200 keywords max
vem_ed_31  → 200 keywords max
vem_ed_32  → 200 keywords max
vem_ed_33  → 200 keywords max
vem_ed_34  → 200 keywords max
vem_ed_35  → 200 keywords max
==================================

vem_ed_01  → selected 65/200 from 65 available POSKW lemmas
vem_ed_02  → selected 51/200 from 51 available POSKW lemmas
vem_ed_03  → selected 38/200 from 38 available POSKW lemmas
vem_ed_04  → selected 45/200 from 45 available POSKW lemmas
vem_ed_05  → selected 46/200 from 46 available POSKW lemmas
vem_ed_06  → selected 50/200 from 50 available POSKW lemmas
vem_ed_07  → selected 48/200 from 48 available POSKW lemmas
vem_ed_08  → selected 37/200 from 37 available POSKW lemmas
vem_ed_09  → selected 39/200 from 39 available POSKW lemmas
vem_ed_10  → selected 25/200 from 25 available POSKW lemmas
vem_ed_11  → selected 26/200 from 26 available POSKW lemmas
vem_ed_12  → selected 36/200 from 36 available POSKW lemmas
vem_ed_13  → selected 39/200 from 39 available POSKW lemmas
vem_ed_14  → selected 18/200 from 18 available POSKW lemmas
vem_ed_15  → selected 27/200 from 27 available POSKW lemmas
vem_ed_16  → selected 48/200 from 48 available POSKW lemmas
vem_ed_17  → selected 16/200 from 16 available POSKW lemmas
vem_ed_18  → selected 54/200 from 54 available POSKW lemmas
vem_ed_19  → selected 125/200 from 125 available POSKW lemmas
vem_ed_20  → selected 34/200 from 34 available POSKW lemmas
vem_ed_21  → selected 33/200 from 33 available POSKW lemmas
vem_ed_22  → selected 24/200 from 24 available POSKW lemmas
vem_ed_23  → selected 17/200 from 17 available POSKW lemmas
vem_ed_24  → selected 65/200 from 65 available POSKW lemmas
vem_ed_25  → selected 69/200 from 69 available POSKW lemmas
vem_ed_26  → selected 57/200 from 57 available POSKW lemmas
vem_ed_27  → selected 123/200 from 123 available POSKW lemmas
vem_ed_28  → selected 132/200 from 132 available POSKW lemmas
vem_ed_29  → selected 93/200 from 93 available POSKW lemmas
vem_ed_30  → selected 71/200 from 71 available POSKW lemmas
vem_ed_31  → selected 79/200 from 79 available POSKW lemmas
vem_ed_32  → selected 77/200 from 77 available POSKW lemmas
vem_ed_33  → selected 14/200 from 14 available POSKW lemmas
vem_ed_34  → selected 117/200 from 117 available POSKW lemmas
vem_ed_35  → selected 152/200 from 152 available POSKW lemmas

Total consolidated keywords before de-duplication: 1990
Unique keywords after de-duplication: 1321
Duplicates removed: 669

Final unique keywords written to: corpus/09_kw_selected/keywords.txt
Final unique keyword count: 1321
"

rm -rf columns columns_clean

python columns.py
# Outputs:
#   columns/
#   columns_clean/
#   file_ids.txt
#   index_keywords.txt

python merge_columns.py
# Output: sas/counts.txt

python sas_formats.py
# Output: sas/word_labels_format.sas, etc

## RUN SAS
## Rogerio Yamada's account

python factor_lists.py \
    --project cl_st1_claudia_vem \
    --sas-output-dir sas/output_cl_st1_claudia_vem
# Output: factors

python corpus_size.py
# Output: corpus_size/corpus_size.tsv

cd latex_boxplots
# Builds boxplots for factor analysis:
python latex_boxplots.py \
    --project cl_st1_claudia_vem \
    --sas-output-dir ../sas/output_cl_st1_claudia_vem
# Output: latex_boxplots/slides
cd ..

python latex_anova_table.py \
    --project cl_st1_claudia_vem \
    --input-dir sas/output_cl_st1_claudia_vem
# Output: latex_tables

python examples.py \
    --project cl_st1_claudia_vem \
    --sas-output-dir sas/output_cl_st1_claudia_vem
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