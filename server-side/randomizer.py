import random
import mysql.connector

# Importa o módulo 'vetor_json'
from vetor_json import app, get_vetor_json

# Conexão com o banco de dados
db = mysql.connector.connect(host="localhost", user="usuario", password="senha", database="nome_banco")
cursor = db.cursor()

def embaralhar_fisher_yates(vetor):
    """
    embaralha um vetor de números não duplicados usando o algoritmo de Fisher-Yates.

    Args:
        vetor: Uma lista de números não duplicados.

    Returns:
        A lista original embaralhada. (Modifica o vetor original em vez de criar um novo)
    """
    n = len(vetor)
    for i in range(n - 1, 0, -1):
        # Gera um índice aleatório entre i (inclusive) e 0 (exclusive)
        j = random.randrange(i + 1)
        # Troca os elementos nas posições i e j
        vetor[i], vetor[j] = vetor[j], vetor[i]

    return vetor

# Gera um vetor de 50.000 números não duplicados de 1 a 50.000
vetor_original = list(range(1, 50001))

# Embaralhe o vetor 3 vezes e imprima o resultado
for i in range(3):
    embaralhar_fisher_yates(vetor_original)  # Chamada do Fisher-Yates
    print(f"Vetor embaralhado #{i + 1}: {vetor_original[:10]}... (primeiros 10 elementos)")
    # Imprime apenas os primeiros 10 elementos

# Inicie o aplicativo Flask
if __name__ == '__main__':
    app.run(debug=True)