import re  # Importa a biblioteca 're' para operações com expressões regulares
import shutil  # Importa a biblioteca 'shutil' para operações de arquivo, como mover e renomear

# Função para limpar conteúdo CSS do texto
def clean_css(content):
    # Remove blocos de mídia (@media queries)
    content = re.sub(r'@media[^{]*\{[^}]*\}', '', content, flags=re.DOTALL)
    # Remove regras CSS que correspondem a seletores específicos
    content = re.sub(r'\s*[\w\-\.#]+\s*\{[^}]*\}\s*', '', content, flags=re.DOTALL)
    # Remove caracteres específicos no final do texto (chaves, colchetes, hashtags, pontos)
    content = re.sub(r'[{}\[\]#\.]*\s*$', '', content)
    # Remove regras CSS restantes após a primeira limpeza
    content = re.sub(r'\s*[\w\-\.#]+\s*\{[^}]*\}\s*', '', content, flags=re.DOTALL)
    return content

# Função para limpar conteúdo HTML e CSS
def clean_html_and_css(content):
    content = clean_css(content)  # Chama a função para limpar o CSS
    # Remove todas as tags HTML do texto
    content = re.sub(r'<.*?>', '', content)
    # Remove entidades HTML, como &amp;, &lt;, etc.
    content = re.sub(r'&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});', '', content)
    # Substitui múltiplos espaços por um único espaço e remove espaços extras no início/fim
    content = re.sub(r'\s+', ' ', content).strip()
    return content

# Função para extrair dados de e-mails a partir do texto limpo
def extract_email_data(content):
    email_pattern = re.compile(
        r'Subject:\s*(.*?)\s*Author:\s*(.*?)\s*Body:\s*(.*?)(?=Subject:|Author:|Body:|$)',
        re.DOTALL
    )
    
    emails = []  # Lista para armazenar os dados dos e-mails extraídos
    matches = email_pattern.findall(content)  # Encontra todas as correspondências no conteúdo
    
    for match in matches:
        subject, author, body = match
        # Armazena os dados do e-mail como um dicionário
        email_data = {
            'subject': subject.strip(),
            'author': author.strip(),
            'body': body.strip()
        }
        emails.append(email_data)  # Adiciona o dicionário à lista de e-mails
    
    return emails

# Função para remover linhas que contenham um texto específico
def remove_lines_with_text(file_path, text_to_remove):
    # Lê o arquivo linha por linha
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Reescreve o arquivo sem as linhas que contêm o texto específico
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            if text_to_remove not in line:
                file.write(line)

# Caminho dos arquivos de entrada e saída
input_file = 'emails.txt'
intermediate_file = 'intermediate_output.txt'
final_output_file = 'final_output.txt'

# Leitura do conteúdo do arquivo de entrada
with open(input_file, 'r', encoding='utf-8') as file:
    content = file.read()

# Limpeza do conteúdo (apenas os primeiros 1.000.000 caracteres)
cleaned_content = clean_html_and_css(content[:1000000])

# Extração de dados dos e-mails
emails = extract_email_data(cleaned_content)

# Salvando o conteúdo limpo e os dados dos e-mails em um arquivo intermediário
with open(intermediate_file, 'w', encoding='utf-8') as file:
    for email in emails:
        file.write(f"Subject: {email['subject']}\n")
        file.write(f"Author: {email['author']}\n")
        file.write(f"Body: {email['body']}\n\n")

print("Arquivo limpo e salvo com sucesso em", intermediate_file)

# Remove linhas do arquivo intermediário que contenham o texto específico
text_to_remove = '.u-row.u-row} .u-row.u-col >}table, tr,.ie-container table, .mso-container* { line-height: inherit; } a[x-apple-data-detectors=\'true\'] { color: inherit !important; text-decoration: none !important; } table,#u_body'
remove_lines_with_text(intermediate_file, text_to_remove)

# Renomeia o arquivo intermediário para o arquivo final
shutil.move(intermediate_file, final_output_file)

print("Arquivo final limpo e salvo com sucesso em", final_output_file)
