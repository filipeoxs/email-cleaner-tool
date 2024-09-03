from textblob import TextBlob  # Biblioteca para análise de sentimentos
import pandas as pd  # Biblioteca para manipulação e salvamento de dados em formato CSV

# Função para analisar o sentimento de um texto
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity  # Retorna a polaridade do sentimento

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

# Função para descrever o contexto com base no corpo do e-mail
def context_description(body):
    body_lower = body.lower()  # Converte o corpo para minúsculas
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

# Função para extrair dados de e-mails de um texto
def extract_email_data(content):
    import re  # Importa aqui para evitar importação desnecessária
    email_pattern = re.compile(
        r'Subject:\s*(.*?)\s*Author:\s*(.*?)\s*Body:\s*(.*?)(?=Subject:|Author:|Body:|$)',
        re.DOTALL  # Permite que o ponto corresponda a quebras de linha
    )
    
    emails = []
    matches = email_pattern.findall(content)  # Encontra todos os e-mails no conteúdo
    
    for match in matches:
        subject, author, body = match
        email_data = {
            'subject': subject.strip(),
            'author': author.strip(),
            'body': body.strip()
        }
        emails.append(email_data)
    
    return emails

# Função para salvar dados em um arquivo CSV
def save_as_csv(data, file_path):
    df = pd.DataFrame(data)  # Converte os dados em um DataFrame do pandas
    df.to_csv(file_path, index=False, encoding='utf-8')  # Salva o DataFrame como CSV

# Caminho dos arquivos de entrada e saída
final_output_file = 'final_output.txt'
sentiment_file = 'sentiment_analysis.txt'
train_file = 'train_data.csv'
test_file = 'test_data.csv'

# Leitura do conteúdo do arquivo
with open(final_output_file, 'r', encoding='utf-8') as file:
    content = file.read()

# Extração de dados de e-mails para análise de sentimento
emails = extract_email_data(content)

# Salvando a análise de sentimento em um novo arquivo
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

# Salvando os dados de análise de sentimento em um arquivo
with open(sentiment_file, 'w', encoding='utf-8') as file:
    for data in sentiment_data:
        file.write(f"Subject: {data['Subject']}\n")
        file.write(f"Author: {data['Author']}\n")
        file.write(f"Body: {data['Body']}\n")
        file.write(f"Sentiment Score: {data['Sentiment Score']}\n")
        file.write(f"Sentiment Description: {data['Sentiment Description']}\n")
        file.write(f"Context Description: {data['Context Description']}\n\n")

print("Análise de sentimento com contexto salva com sucesso em", sentiment_file)
