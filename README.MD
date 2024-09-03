# Análise de E-mails

Este projeto realiza uma análise completa de e-mails extraídos de um arquivo de texto, incluindo limpeza de conteúdo, extração de dados, análise de sentimento e geração de conjuntos de dados para treinamento e teste. Abaixo estão descritas as etapas e funções principais do projeto.

## Funcionalidades

1. **Limpeza de Conteúdo**
   - Remove CSS e HTML desnecessário de e-mails.
   - Remove linhas específicas indesejadas do conteúdo.

2. **Extração de Dados de E-mails**
   - Extrai o assunto, autor e corpo dos e-mails de um texto.

3. **Análise de Sentimento**
   - Calcula a polaridade do sentimento dos corpos dos e-mails.
   - Classifica o sentimento em categorias descritivas (positivo, negativo, neutro, etc.).
   - Determina o contexto dos e-mails (questão, atualização, reunião, etc.).

4. **Geração de Dados de Treinamento e Teste**
   - Separa os dados analisados em conjuntos de treinamento e teste.
   - Salva os dados em arquivos CSV para uso posterior.

5. **Contagem de Palavras Mais Comuns**
   - Conta as palavras mais comuns no corpo dos e-mails.

## Arquivos e Saídas

- **Entrada:**
  - `emails_treinamento.txt`: Arquivo de texto contendo os e-mails para análise.

- **Processo:**
  - `intermediate_output.txt`: Arquivo intermediário após a limpeza inicial.
  - `final_output.txt`: Arquivo final com e-mails limpos e prontos para análise.

- **Saídas:**
  - `sentiment_analysis.txt`: Análise de sentimento dos e-mails com descrições e contexto.
  - `train_data.csv`: Dados de treinamento separados.
  - `test_data.csv`: Dados de teste separados.

## Requisitos

- Python 3.x
- Bibliotecas:
  - `textblob`
  - `pandas`

## Como Executar

1. **Instale as bibliotecas necessárias:**
   ```bash
   pip install textblob pandas
