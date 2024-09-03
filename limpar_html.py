import re  # Biblioteca para expressões regulares
import shutil  # Biblioteca para operações de arquivo de alto nível
import random  # Biblioteca para operações aleatórias
from textblob import TextBlob  # Biblioteca para processamento de texto e análise de sentimento
import pandas as pd  # Biblioteca para manipulação de dados em DataFrames

# Função para limpar conteúdo CSS de um texto
def clean_css(content):
    # Remove blocos de CSS que correspondem a determinadas regras de mídia e seletores
    content = re.sub(r'@media[^{]*\{[^}]*\}', '', content, flags=re.DOTALL)
    content = re.sub(r'\s*[\w\-\.#]+\s*\{[^}]*\}\s*', '', content, flags=re.DOTALL)
    content = re.sub(r'[{}\[\]#\.]*\s*$', '', content)
    content = re.sub(r'\s*[\w\-\.#]+\s*\{[^}]*\}\s*', '', content, flags=re.DOTALL)
    return content

# Função para limpar conteúdo HTML e CSS de um texto
def clean_html_and_css(content):
    content = clean_css(content)
    # Remove tags HTML e entidades HTML, substituindo por espaços
    content = re.sub(r'<.*?>', '', content)
    content = re.sub(r'&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});', '', content)
    content = re.sub(r'\s+', ' ', content).strip()
    return content

# Função para extrair dados de e-mails a partir de um texto
def extract_email_data(content):
    # Padrão para capturar dados de e-mails (assunto, autor e corpo)
    email_pattern = re.compile(
        r'Subject:\s*(.*?)\s*Author:\s*(.*?)\s*Body:\s*(.*?)(?=Subject:|Author:|Body:|$)',
        re.DOTALL
    )
    
    emails = []
    matches = email_pattern.findall(content)
    
    for match in matches:
        subject, author, body = match
        email_data = {
            'subject': subject.strip(),
            'author': author.strip(),
            'body': body.strip()
        }
        emails.append(email_data)
    
    return emails

# Função para remover linhas contendo um texto específico de um arquivo
def remove_lines_with_text(file_path, text_to_remove):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            if text_to_remove not in line:
                file.write(line)

# Função para analisar o sentimento de um texto
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# Função para descrever o sentimento com base na pontuação
def sentiment_description(score):
    if score >= 0.5:
        return "Altamente positivo"
    elif score >= 0.2:
        return "Moderadamente positivo"
    elif score > 0:
        return "Levemente positivo"
    elif score == 0:
        return "Neutro"
    elif score > -0.2:
        return "Levemente negativo"
    elif score > -0.5:
        return "Moderadamente negativo"
    else:
        return "Altamente negativo"

# Função para descrever o contexto do corpo do e-mail
def context_description(body):
    body_lower = body.lower()
    if 'question' in body_lower or 'help' in body_lower:
        return "Questão ou pedido de ajuda"
    elif 'update' in body_lower or 'report' in body_lower:
        return "Relatório ou atualização"
    elif 'meeting' in body_lower or 'schedule' in body_lower:
        return "Discussão de reunião ou agenda"
    elif 'project' in body_lower or 'task' in body_lower:
        return "Discussão de projeto ou tarefa"
    elif 'feedback' in body_lower or 'review' in body_lower:
        return "Feedback ou revisão"
    else:
        return "Conteúdo geral"

# Função para salvar dados em um arquivo CSV
def save_as_csv(data, file_path):
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False, encoding='utf-8')

# Função para dividir dados em conjuntos de treinamento e teste
def split_data(data, train_ratio=0.8):
    random.shuffle(data)
    split_index = int(len(data) * train_ratio)
    train_data = data[:split_index]
    test_data = data[split_index:]
    return train_data, test_data

# Caminhos dos arquivos de entrada e saída
input_file = 'emails_treinamento.txt'
intermediate_file = 'intermediate_output.txt'
final_output_file = 'final_output.txt'
sentiment_file = 'sentiment_analysis.txt'
train_file = 'train_data.csv'
test_file = 'test_data.csv'

# Leitura do conteúdo do arquivo de entrada
with open(input_file, 'r', encoding='utf-8') as file:
    content = file.read()

# Limpeza do conteúdo (HTML e CSS)
cleaned_content = clean_html_and_css(content[:1000000])

# Extração de dados de e-mails do conteúdo limpo
emails = extract_email_data(cleaned_content)

# Salvando o conteúdo limpo em um novo arquivo intermediário
with open(intermediate_file, 'w', encoding='utf-8') as file:
    for email in emails:
        file.write(f"Subject: {email['subject']}\n")
        file.write(f"Author: {email['author']}\n")
        file.write(f"Body: {email['body']}\n\n")

print("Arquivo limpo e salvo com sucesso em", intermediate_file)

# Remoção de linhas que contêm um texto específico do arquivo intermediário
text_to_remove = '.u-row.u-row} .u-row.u-col >}table, tr,.ie-container table, .mso-container* { line-height: inherit; } a[x-apple-data-detectors=\'true\'] { color: inherit !important; text-decoration: none !important; } table,#u_body'
remove_lines_with_text(intermediate_file, text_to_remove)

# Renomeia o arquivo intermediário para o arquivo de saída final
shutil.move(intermediate_file, final_output_file)

print("Arquivo final limpo e salvo com sucesso em", final_output_file)

# Leitura do conteúdo do arquivo final para análise de sentimento
with open(final_output_file, 'r', encoding='utf-8') as file:
    content = file.read()

# Extração de dados de e-mails para a análise de sentimento
emails = extract_email_data(content)

# Salvando a análise de sentimento e descrição do contexto em um novo arquivo
sentiment_data = []
for email in emails:
    sentiment = analyze_sentiment(email['body'])
    sentiment_desc = sentiment_description(sentiment)
    context_desc = context_description(email['body'])
    sentiment_data.append({
        'Subject': email['subject'],
        'Author': email['author'],
        'Body': email['body'],
        'Sentiment Score': sentiment,
        'Sentiment Description': sentiment_desc,
        'Context Description': context_desc
    })

with open(sentiment_file, 'w', encoding='utf-8') as file:
    for data in sentiment_data:
        file.write(f"Subject: {data['Subject']}\n")
        file.write(f"Author: {data['Author']}\n")
        file.write(f"Body: {data['Body']}\n")
        file.write(f"Sentiment Score: {data['Sentiment Score']}\n")
        file.write(f"Sentiment Description: {data['Sentiment Description']}\n")
        file.write(f"Context Description: {data['Context Description']}\n\n")

print("Análise de sentimento com contexto salva com sucesso em", sentiment_file)

# Separação dos dados em conjuntos de treinamento e teste
train_data, test_data = split_data(sentiment_data)

# Salvando os dados de treinamento e teste em arquivos CSV
save_as_csv(train_data, train_file)
save_as_csv(test_data, test_file)

print("Dados de treinamento e teste salvos com sucesso em", train_file, "e", test_file)
