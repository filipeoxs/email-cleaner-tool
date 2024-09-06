import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import joblib

# 1. Carregar os dados CSV
df = pd.read_csv('train_data.csv')

# 2. Pré-processar os dados
# Identifique as colunas categóricas (textuais)
categorical_cols = df.select_dtypes(include=['object']).columns

# Codifique as variáveis categóricas (uma opção: Label Encoding)
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Supondo que a última coluna seja o target e o restante as features
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# Dividir os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Treinar o modelo
modelo = RandomForestClassifier()
modelo.fit(X_train, y_train)

# 4. Avaliar o modelo
y_pred = modelo.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Acurácia do modelo: {accuracy:.2f}')

# 5. Exportar o modelo
joblib.dump(modelo, 'modelo_treinado.pkl')

# Salvar os codificadores
joblib.dump(label_encoders, 'label_encoders.pkl')
