import pandas as pd  # Importa a biblioteca 'pandas' para manipulação de dados em DataFrames
import random  # Importa a biblioteca 'random' para operações de aleatoriedade

# Função para dividir os dados em conjuntos de treinamento e teste
def split_data(data, train_ratio=0.8):
    random.shuffle(data)  # Embaralha os dados para garantir aleatoriedade
    split_index = int(len(data) * train_ratio)  # Calcula o índice de divisão com base na proporção de treinamento
    train_data = data[:split_index]  # Seleciona os dados de treinamento
    test_data = data[split_index:]  # Seleciona os dados de teste
    return train_data, test_data

# Função para salvar os dados como arquivo CSV
def save_as_csv(data, file_path):
    df = pd.DataFrame(data)  # Converte os dados em um DataFrame do pandas
    df.to_csv(file_path, index=False, encoding='utf-8')  # Salva o DataFrame em um arquivo CSV

# Caminho dos arquivos de entrada e saída
sentiment_file = 'sentiment_analysis.txt'  # Arquivo de entrada com dados de análise de sentimento
train_file = 'train_data.csv'  # Arquivo de saída para dados de treinamento
test_file = 'test_data.csv'  # Arquivo de saída para dados de teste

# Carrega os dados de sentimento a partir do arquivo de texto
with open(sentiment_file, 'r', encoding='utf-8') as file:
    content = file.read()

# Processa os dados de sentimento
emails = []
lines = content.split('\n\n')  # Divide o conteúdo em blocos de texto separados por linhas em branco
for line in lines:
    if line.strip():  # Verifica se a linha não está vazia
        parts = line.split('\n')  # Divide cada bloco em linhas individuais
        if len(parts) >= 6:  # Verifica se há pelo menos 6 partes (campos de dados)
            email_data = {
                'Subject': parts[0].replace('Subject: ', '').strip(),  # Extrai e limpa o assunto
                'Author': parts[1].replace('Author: ', '').strip(),  # Extrai e limpa o autor
                'Body': parts[2].replace('Body: ', '').strip(),  # Extrai e limpa o corpo do e-mail
                'Sentiment Score': float(parts[3].replace('Sentiment Score: ', '').strip()),  # Extrai e converte o score de sentimento
                'Sentiment Description': parts[4].replace('Sentiment Description: ', '').strip(),  # Extrai e limpa a descrição do sentimento
                'Context Description': parts[5].replace('Context Description: ', '').strip()  # Extrai e limpa a descrição do contexto
            }
            emails.append(email_data)  # Adiciona os dados do e-mail à lista de e-mails

# Divide os dados em conjuntos de treinamento e teste
train_data, test_data = split_data(emails)

# Salva os dados de treinamento e teste em arquivos CSV
save_as_csv(train_data, train_file)
save_as_csv(test_data, test_file)

# Imprime uma mensagem de sucesso
print("Dados de treinamento e teste salvos com sucesso em", train_file, "e", test_file)
