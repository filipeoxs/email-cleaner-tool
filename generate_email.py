import pandas as pd
import joblib

def predict_email_from_text(file_path):
    # Carregar o modelo treinado
    modelo = joblib.load('modelo_treinado.pkl')
    
    # Carregar os codificadores
    label_encoders = joblib.load('label_encoders.pkl')
    
    # Ler o conteúdo do arquivo de texto com codificação UTF-8
    with open(file_path, 'r', encoding='utf-8') as file:
        email_content = file.read()

    # Supondo que o e-mail está dividido em subject e body
    email_parts = email_content.split('\n\n', 1)  # Dividir subject e body
    
    if len(email_parts) == 2:
        subject, body = email_parts
    else:
        subject = email_parts[0]
        body = ""

    # Criar um DataFrame com as colunas usadas durante o treinamento
    df = pd.DataFrame({
        'Subject': [subject],
        'Body': [body],
        # Inclua outras colunas se necessário, como 'Author', 'Sentiment Score', etc.
    })
    
    # Aplicar o Label Encoding nas colunas categóricas, se necessário
    for col, le in label_encoders.items():
        if col in df.columns:
            df[col] = le.transform(df[col].astype(str))  # Certifique-se de transformar para string antes de usar o LabelEncoder
    
    # Fazer a previsão
    prediction = modelo.predict(df)
    
    return prediction[0]

# Exemplo de uso
file_path = 'sentiment_analysis.txt'
resultado = predict_email_from_text(file_path)
print(f'Resultado da predição: {resultado}')
