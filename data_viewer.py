import matplotlib.pyplot as plt  # Importa a biblioteca matplotlib para visualização de dados
from most_used_words import analyze  # Importa a função 'analyze' do módulo 'most_used_words'

# Função para plotar a frequência das palavras
def plot_word_frequencies(word_freq):
    # Descompacta as palavras e suas contagens a partir da lista de tuplas
    words, counts = zip(*word_freq)
    
    # Cria um gráfico de barras para as palavras e suas frequências
    plt.bar(words, counts)
    plt.xlabel('Words')  # Define o rótulo do eixo x como 'Words'
    plt.ylabel('Frequency')  # Define o rótulo do eixo y como 'Frequency'
    plt.title('Word Frequency Distribution')  # Define o título do gráfico
    plt.xticks(rotation=90)  # Rotaciona os rótulos do eixo x em 90 graus para melhor legibilidade
    plt.show()  # Exibe o gráfico

# Exemplo de uso da função
plot_word_frequencies(analyze())  # Chama a função para analisar e plotar as frequências das palavras
