from nltk import ngrams  # Importa a função ngrams para gerar n-gramas
from nltk.probability import FreqDist  # Importa FreqDist para calcular a frequência dos n-gramas
import nltk  # Importa a biblioteca nltk (Natural Language Toolkit)

# Baixa o pacote 'punkt', necessário para a tokenização de palavras
nltk.download('punkt', force=True)

# Função para obter os n-gramas mais comuns em um texto
def get_most_common_ngrams(text, n=2, num_ngrams=10):
    # Tokeniza o texto em palavras, convertendo-o para minúsculas
    tokens = nltk.word_tokenize(text.lower())
    # Gera os n-gramas a partir dos tokens
    n_grams = ngrams(tokens, n)
    # Calcula a frequência dos n-gramas
    ngram_freq = FreqDist(n_grams)
    # Retorna os n-gramas mais comuns
    return ngram_freq.most_common(num_ngrams)

# Leitura do conteúdo do arquivo 'final_output.txt'
with open('final_output.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Separação dos corpos dos e-mails
emails = content.split('\n\n')  # Divide os e-mails com base em linhas em branco
all_bodies = []  # Lista para armazenar os corpos dos e-mails

# Extrai o corpo de cada e-mail
for email in emails:
    if 'Body:' in email:
        # Encontra o início do corpo do e-mail
        body_start = email.index('Body:') + len('Body:')
        # Extrai e limpa o corpo do e-mail
        body = email[body_start:].strip()
        # Adiciona o corpo à lista
        all_bodies.append(body)

# Junta todos os corpos dos e-mails em uma única string
all_bodies_text = ' '.join(all_bodies)

# Exemplo de uso da função get_most_common_ngrams para gerar bigramas (n=2)
bigrams = get_most_common_ngrams(all_bodies_text, n=2)
print("Bigramas mais comuns:", bigrams)  # Exibe os bigramas mais comuns
