from collections import Counter
import re
from textgenrnn import textgenrnn
import random

# Função para extrair e-mails de um arquivo de texto
def read_emails(file_path):
    # Abre o arquivo no caminho especificado e lê seu conteúdo
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Define um padrão de regex para capturar o assunto e corpo dos e-mails
    email_pattern = re.compile(
        r'Subject:\s*(.*?)\s*Body:\s*(.*?)(?=Subject:|Body:|$)',
        re.DOTALL  # Permite que o ponto na regex também corresponda a quebras de linha
    )
    
    # Lista para armazenar os e-mails extraídos
    emails = []
    
    # Encontra todas as correspondências no conteúdo do arquivo
    matches = email_pattern.findall(content)
    
    # Processa cada correspondência encontrada
    for match in matches:
        subject, body = match
        # Cria um dicionário com o assunto e corpo do e-mail, removendo espaços extras
        email_data = {
            'subject': subject.strip(),
            'body': body.strip()
        }
        # Adiciona o e-mail à lista
        emails.append(email_data)
    
    return emails  # Retorna a lista de e-mails extraídos

# Lê os e-mails do arquivo 'final_output.txt'
emails = read_emails('final_output.txt')

# Função para extrair características de estilo dos e-mails
def extract_style_features(emails):
    # Extrai todos os assuntos dos e-mails
    subjects = [email['subject'] for email in emails]
    # Extrai todos os corpos dos e-mails
    bodies = [email['body'] for email in emails]
    
    # Concatena todos os corpos dos e-mails em uma única string
    all_bodies = ' '.join(bodies)
    # Encontra todas as palavras nos corpos dos e-mails, ignorando maiúsculas/minúsculas
    words = re.findall(r'\b\w+\b', all_bodies.lower())
    # Conta a frequência de cada palavra
    word_freq = Counter(words)
    
    # Retorna um dicionário com as características extraídas
    return {
        'subjects': subjects,
        'bodies': bodies,
        'word_freq': word_freq
    }

# Extrai as características de estilo dos e-mails lidos
style_features = extract_style_features(emails)

# Função para gerar novos e-mails com base em um prefixo
def generate_email(prefix):
    # Inicializa o modelo de geração de texto
    textgen = textgenrnn.TextgenRNN()
    
    # Gera um novo texto baseado no prefixo fornecido
    generated_text = textgen.generate(return_as_list=True, prefix=prefix)[0]
    
    return generated_text  # Retorna o texto gerado

# Seleciona um exemplo de assunto aleatoriamente dos e-mails extraídos
subject_example = random.choice(style_features['subjects'])
# Seleciona um exemplo de corpo aleatoriamente dos e-mails extraídos
body_example = random.choice(style_features['bodies'])
# Gera um novo assunto com base no exemplo de assunto
new_subject = generate_email(subject_example)
# Gera um novo corpo de e-mail com base no exemplo de corpo
new_body = generate_email(body_example)

# Função para salvar os novos e-mails gerados em um arquivo de texto
def save_new_emails(subjects, bodies, file_path):
    # Abre o arquivo no modo de escrita
    with open(file_path, 'w', encoding='utf-8') as file:
        # Escreve cada novo e-mail no arquivo
        for subject, body in zip(subjects, bodies):
            file.write(f"Subject: {subject}\n")
            file.write(f"Body: {body}\n\n")

# Gera 10 novos assuntos baseados no exemplo selecionado
new_subjects = [generate_email(subject_example) for _ in range(10)]
# Gera 10 novos corpos de e-mails baseados no exemplo selecionado
new_bodies = [generate_email(body_example) for _ in range(10)]

# Salva os novos e-mails gerados no arquivo 'generated_emails.txt'
save_new_emails(new_subjects, new_bodies, 'generated_emails.txt')
print("Novos e-mails gerados e salvos em 'generated_emails.txt'")
