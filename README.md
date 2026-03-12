# VEM Corpus

# PDF → Text Corpus Processing Pipeline

This repository contains a multi-step pipeline for converting PDF documents into clean, tokenized, and linguistically tagged text suitable for corpus analysis.

Each script represents one stage in the workflow. The leading numbers in the filenames indicate the **order of processing**.


These two folders contain the final products of this workflow:

The folder containing the tokens of each file:
```
10_tokenized/
```

The folder containing the part of speech tagging and lemma of each token:

```
11_tagged/

```

---
## Methodology

The textual data analyzed in this study originated from a collection of documents distributed as PDF files. Although the PDFs contained selectable text, the underlying content had originally been produced using page-layout software. As a result, the embedded text layer did not reliably reflect the logical reading order of the document. Lines, columns, and textual elements were frequently fragmented or interleaved in ways that made direct extraction unsuitable for corpus-linguistic analysis. For this reason, a multi-stage reconstruction and verification pipeline was developed.

The first stage of the procedure involved decomposing each source PDF into individual page units. Treating each page as a separate document allowed subsequent processing to operate on smaller, visually coherent segments. From each page two parallel representations were produced. First, a conventional text extraction was generated directly from the PDF. This extraction was retained primarily as a reference representation of the lexical material present in the original file. Second, a high-resolution image of each page was produced in order to support image-based optical character recognition.

In the second stage, the page images were submitted to an OCR process using ChatGPT’s vision-based recognition capabilities. A structured extraction prompt was employed to guide the system in reconstructing the textual content visible on the page. The model’s output was returned in structured JSON format containing discrete textual elements such as titles, headings, and paragraph-level prose. Because the goal of the corpus was to capture only communicative text, the extraction prompt explicitly instructed the system to exclude non-prose elements such as mastheads, boilerplate footers, captions, and other recurring layout artifacts.

Given the well-known possibility that large language models may introduce lexical items not present in the original source, an additional verification stage was implemented. The reconstructed OCR text was compared against the reference text extracted directly from the PDF. Token-level comparisons were performed between the two versions of each page. Tokens present in the OCR reconstruction but absent in the PDF text were flagged as potential hallucinations or recognition errors. For example, in one instance the OCR reconstruction produced the token `Fates`, whereas the original PDF text contained the proper name `Fatecs`, referring to the Brazilian academic institutions known as *Faculdades de Tecnologia*. In another case, the OCR system produced `aumentado` (‘increased’) where the original token was `aumentando` (‘increasing’). Such discrepancies typically arise from ambiguity in character recognition (e.g., confusion between visually similar character sequences such as `-s` and `-cs` or `-do` and `-ndo`). To assist with identifying these discrepancies, normalized Levenshtein distance was used to measure similarity between tokens in the OCR output and those in the reference extraction. In addition, keyword-in-context (KWIC) displays were generated so that each flagged token could be examined within its surrounding textual environment. These contextual displays allowed the researcher to determine whether a token represented a plausible OCR recognition error, a minor orthographic deviation, or a lexical insertion introduced during the reconstruction process. Manual corrections were then recorded and applied to the reconstructed text.

After manual review and correction, the cleaned page-level texts were recombined into complete documents corresponding to the original PDFs. The resulting corpus was then processed using the spaCy natural language processing library. Each document was tokenized and annotated with standard linguistic information, including lemma, part-of-speech category, and additional token attributes. The final output consists of both tokenized and linguistically tagged versions of the corpus, formatted in tabular form to facilitate downstream corpus-linguistic analyses such as frequency analysis, keyword analysis, and collocation studies.

## Metodologia

Os dados textuais analisados neste estudo originam-se de um conjunto de documentos distribuídos em formato PDF. Embora os arquivos contivessem uma camada de texto selecionável, o conteúdo original havia sido produzido em software de editoração eletrônica. Como consequência, a camada textual incorporada não refletia de forma confiável a ordem lógica de leitura do documento. Linhas, colunas e outros elementos textuais apareciam frequentemente fragmentados ou intercalados, o que tornava a extração direta inadequada para análise de corpus. Por esse motivo, foi desenvolvido um pipeline de reconstrução e verificação em múltiplas etapas.

A primeira etapa do procedimento consistiu na decomposição de cada PDF de origem em unidades correspondentes a páginas individuais. O tratamento de cada página como um documento independente permitiu que o processamento subsequente operasse sobre segmentos visualmente coerentes e de menor dimensão. A partir de cada página foram produzidas duas representações paralelas. Em primeiro lugar, realizou-se uma extração textual convencional diretamente do PDF. Essa extração foi preservada principalmente como uma representação de referência do material lexical presente no arquivo original. Em segundo lugar, gerou-se uma imagem de alta resolução de cada página, destinada a apoiar processos de reconhecimento óptico de caracteres baseados em imagem.

Na segunda etapa, as imagens das páginas foram submetidas a um processo de OCR utilizando as capacidades de reconhecimento visual do ChatGPT. Um prompt estruturado de extração foi empregado para orientar o sistema na reconstrução do conteúdo textual visível em cada página. A saída do modelo foi retornada em formato JSON estruturado, contendo elementos textuais discretos, como títulos, subtítulos e parágrafos. Como o objetivo do corpus era capturar apenas texto com valor comunicativo, o prompt de extração instruía explicitamente o sistema a excluir elementos não textuais ou paratextuais, tais como mastheads, rodapés padronizados (boilerplate), legendas e outros artefatos recorrentes de layout.

Considerando a possibilidade amplamente reconhecida de que modelos de linguagem de grande porte possam introduzir itens lexicais que não estão presentes na fonte original, foi implementada uma etapa adicional de verificação. O texto reconstruído por OCR foi comparado com o texto de referência extraído diretamente do PDF. Comparações em nível de token foram realizadas entre as duas versões de cada página. Tokens presentes na reconstrução OCR, mas ausentes no texto extraído do PDF, foram sinalizados como potenciais alucinações ou erros de reconhecimento. Por exemplo, em um caso a reconstrução OCR produziu o token `Fates`, enquanto o texto original continha o nome próprio `Fatecs`, referente às instituições brasileiras conhecidas como *Faculdades de Tecnologia*. Em outro exemplo, o sistema OCR produziu `aumentado` (“increased”) quando o token original era `aumentando` (“increasing”). Tais discrepâncias frequentemente resultam de ambiguidades no reconhecimento de caracteres, como a confusão entre sequências visualmente semelhantes como `-s` e `-cs` ou `-do` e `-ndo`. Para auxiliar na identificação dessas discrepâncias, empregou-se a distância de Levenshtein normalizada para medir a similaridade entre tokens na saída do OCR e aqueles presentes na extração de referência. Além disso, foram geradas visualizações de palavra-em-contexto (KWIC – *keyword in context*), permitindo que cada token sinalizado fosse examinado dentro de seu ambiente textual imediato. Esses contextos facilitaram a avaliação manual de cada caso, permitindo distinguir entre erros plausíveis de OCR, pequenas variações ortográficas ou inserções lexicais introduzidas durante o processo de reconstrução. As correções necessárias foram então registradas e aplicadas ao texto reconstruído.

Após a revisão e correção manual, os textos limpos em nível de página foram recombinados para reconstruir os documentos completos correspondentes aos PDFs originais. O corpus resultante foi então processado utilizando a biblioteca de processamento de linguagem natural spaCy. Cada documento foi tokenizado e anotado com informações linguísticas padrão, incluindo lema, categoria gramatical (parte do discurso) e outros atributos de token. O resultado final consiste em versões tokenizadas e linguisticamente anotadas do corpus, formatadas em estrutura tabular (TSV), adequadas para análises de linguística de corpus, tais como análise de frequência, análise de palavras-chave e estudos de colocação.
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