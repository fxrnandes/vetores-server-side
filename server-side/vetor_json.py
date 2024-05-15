from flask import Flask, render_template, jsonify, request
from graficos import bar_chart, bubble_chart, dot_plot, line_chart, scatter_plot
import mysql.connector
import time
import random

from randomizer import embaralhar_fisher_yates

app = Flask(__name__)

@app.route('/vetor_json')
def get_vetor_json():
    # Obter o tamanho do vetor da query string
    tamanho_vetor = request.args.get('tamanho_vetor', type=int)

    # Validar o tamanho do vetor
    if tamanho_vetor is None or tamanho_vetor < 1 or tamanho_vetor > 50000:
        return "Tamanho do vetor inválido. O tamanho do vetor deve ser um número inteiro entre 1 e 50.000."

    # Conectar ao banco de dados MySQL
    conn = mysql.connector.connect(host="localhost", database="nome_banco", user="usuario", password="senha")
    cursor = conn.cursor()

    # Gerar o vetor
    vetor_gerado = gerar_vetor(tamanho_vetor)

    # Embaralhar o vetor
    vetor_embaralhado = vetor_gerado.copy()
    tempos_embaralhamento = []
    for i in range(3):
        start_time = time.time()
        embaralhar_fisher_yates(vetor_embaralhado)
        end_time = time.time()
        tempo_embaralhamento = end_time - start_time
        tempos_embaralhamento.append(tempo_embaralhamento)

    # Ordenar o vetor original
    vetor_gerado.sort()

    # Gerar gráficos
    scatter_plot(range(len(vetor_embaralhado)), vetor_embaralhado, 'scatter_plot.png')
    line_chart(range(len(vetor_gerado)), vetor_gerado, 'line_chart.png')
    bar_chart(range(len(vetor_gerado)), vetor_gerado, 'bar_chart.png')
    bubble_chart(range(len(vetor_embaralhado)), vetor_embaralhado, [random.randint(1, 100) for _ in range(len(vetor_embaralhado))], 'bubble_chart.png')
    dot_plot(range(len(vetor_embaralhado)), vetor_embaralhado, 'dot_plot.png')


    # Converter dados em JSON
    vetor_json = {
        "nome_vetor": "Nome do seu vetor",  # Substitua por um nome real
        "descricao": "Descrição do seu vetor",  # Substitua por uma descrição real
        "vetor_aleatorio": vetor_embaralhado,
        "vetor_ordenado": vetor_gerado,
        "tempos_embaralhamento": tempos_embaralhamento
    }

    # Fechar conexão com o banco de dados
    cursor.close()
    conn.close()

    # Retornar o template HTML com dados em JSON
    return render_template('vetor.html', vetor_json=jsonify(vetor_json))

# Função para gerar o vetor (implemente a lógica de acordo com suas necessidades)
def gerar_vetor(tamanho_vetor):
    """
    Gera um vetor aleatório de números inteiros sem repetição até 50.000 utilizando o algoritmo 'reservoir sampling'.

    Args:
        tamanho_vetor (int): Tamanho do vetor a ser gerado.

    Returns:
        list: Vetor contendo números inteiros aleatórios sem repetição.
    """

    if tamanho_vetor > 50000:
        raise ValueError("Tamanho do vetor não pode ser maior que 50.000.")

    vetor = []
    for i, numero in enumerate(range(1, 50001)):
        if i < tamanho_vetor:
            vetor.append(numero)
        else:
            # Probabilidade de manter o número no vetor
            chance_selecao = tamanho_vetor / (i + 1)

            # Seleciona o número aleatoriamente com base na chance
            if random.random() < chance_selecao:
                vetor[random.randrange(tamanho_vetor)] = numero

    return vetor # Retorne o vetor gerado

if __name__ == '__main__':
    app.run(debug=True)