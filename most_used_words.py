from collections import Counter  # Para contar a frequência das palavras
import re  # Para expressões regulares

# Função para obter as palavras mais comuns em um texto
def get_most_common_words(text, num_words=10):
    # Encontra todas as palavras no texto, convertendo tudo para minúsculas
    words = re.findall(r'\b\w+\b', text.lower())
    # Conta a frequência de cada palavra
    word_counts = Counter(words)
    # Retorna as palavras mais comuns
    return word_counts.most_common(num_words)

# Leitura do conteúdo do arquivo
with open('final_output.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Separar os corpos dos e-mails
# Divide o conteúdo em e-mails com base em linhas em branco (assumindo que há uma linha em branco entre e-mails)
emails = content.split('\n\n')
all_bodies = []

# Extrair o corpo de cada e-mail
for email in emails:
    if 'Body:' in email:
        # Encontrar o início do corpo do e-mail e extrair o texto
        body_start = email.index('Body:') + len('Body:')
        body = email[body_start:].strip()
        all_bodies.append(body)

# Função de análise
def analyze():
    # Junta todos os corpos dos e-mails em um único texto
    all_bodies_text = ' '.join(all_bodies)
    # Obtém as palavras mais comuns
    common_words = get_most_common_words(all_bodies_text)
    # Imprime as palavras mais comuns
    print("Palavras mais comuns:", common_words)
    return common_words
