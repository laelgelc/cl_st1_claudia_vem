# Metodologia para Extração de Texto de Newsletters em PDF Baseadas em Layout

O objetivo deste projeto foi reconstruir corpora textuais limpos e sequenciais a partir de uma coleção de newsletters em PDF originalmente produzidas com softwares de diagramação. Como esse tipo de software prioriza o posicionamento visual dos elementos em vez da ordem lógica de leitura, a exportação direta do texto dos PDFs resultou em frases fragmentadas, parágrafos desconexos e sequenciamento comprometido. Para contornar essa limitação, foi desenvolvido um fluxo de trabalho em múltiplas etapas, utilizando Python, bibliotecas tradicionais de processamento de PDF e as APIs multimodais da OpenAI.

## 1. Processamento em Nível de Página

Cada newsletter em PDF foi inicialmente dividida em arquivos individuais de uma página. Isso permitiu que cada página fosse processada de forma independente e reduziu a complexidade nas etapas de conversão para imagem e OCR. Newsletters com múltiplas páginas foram separadas em arquivos distintos, enquanto newsletters de página única permaneceram inalteradas.

## 2. Extração Paralela de Texto e Imagem

Para cada PDF em nível de página, foram gerados dois tipos de saída:

Uma extração direta de texto utilizando uma biblioteca de PDF. Esse resultado foi preservado para fins de comparação, embora mantivesse os problemas de fragmentação decorrentes do layout.

Uma renderização da página em imagem de alta resolução. A imagem foi gerada com resolução ampliada para otimizar a precisão do OCR durante o processamento com IA.

As imagens passaram a ser a principal fonte para a reconstrução estruturada do texto.

## 3. OCR com IA e Saída Estruturada

Cada imagem de página foi submetida à API multimodal da OpenAI com um prompt cuidadosamente elaborado para reconstrução de corpus. O prompt instruía o modelo a:

Extrair apenas o conteúdo textual com valor comunicativo.

Excluir cabeçalhos institucionais (mastheads), rodapés padronizados, legendas de imagens e elementos meramente decorativos ou estruturais.

Preservar o idioma original, sem tradução ou normalização.

Retornar o resultado em um esquema estruturado em JSON (incluindo título, subtítulo e seções com cabeçalhos e parágrafos).

Cada página processada gerou um arquivo JSON correspondente, representando o texto daquela página em ordem lógica de leitura.

## 4. Pós-Processamento e Filtragem de Padrões

Após a revisão dos resultados estruturados, foram identificados certos padrões recorrentes que não constituíam conteúdo relevante (por exemplo, avisos administrativos padronizados ou blocos institucionais repetidos). Um script adicional em Python aplicou filtros baseados em padrões para remover esses elementos dos arquivos JSON. Versões limpas foram salvas separadamente, garantindo transparência metodológica.

## 5. Conversão para Texto Simples

Os arquivos JSON limpos foram então convertidos para formato de texto simples. Marcadores estruturais (títulos, cabeçalhos, parágrafos e listas) foram linearizados, preservando a ordem de leitura. O resultado foi um conjunto de arquivos textuais por página, adequados para compilação em corpus e análise linguística.

## 6. Recomposição de Newsletters com Múltiplas Páginas

Por fim, uma rotina adicional em Python recompôs os arquivos de texto individuais em newsletters completas, restaurando a sequência original das páginas. Newsletters de página única foram simplesmente transferidas para o diretório final.

## Próximas Etapas

Encontro-me atualmente comparando os arquivos de texto resultantes com a versão textual original dos PDFs. O objetivo é verificar se houve inserção de palavras ou termos que não estavam presentes nas newsletters originais. Uma análise preliminar indica que o prompt utilizado não levou à introdução de conteúdo inexistente nos documentos originais.

Após a conclusão dessa verificação final, os arquivos serão processados com spaCy para anotação linguística (tagging), dando início à etapa de análise propriamente dita.
