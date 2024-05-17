from flask import Flask, render_template, jsonify, request
from graficos import bar_chart, bubble_chart, dot_plot, line_chart, scatter_plot
import mysql.connector
import time
import random
import json
from randomizer import embaralhar_fisher_yates


app = Flask(__name__)


@app.route('/vetor_json')
def get_vetor_json():
    # Obter o tamanho do vetor da query string
    try:
        tamanho_vetor = int(request.args.get('tamanho_vetor'))
    except ValueError:
        return "Tamanho do vetor inválido. Deve ser um número inteiro."

    # Validar o tamanho do vetor
    if tamanho_vetor < 1 or tamanho_vetor > 50000:
        return "Tamanho do vetor inválido. Deve estar entre 1 e 50.000."

    # Conectar ao banco de dados MySQL
    try:
        conn = mysql.connector.connect(host="127.0.0.1:3306", database="aula", user="root", password="")
        cursor = conn.cursor()
    except mysql.connector.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return "Erro ao conectar ao banco de dados."

    # Criar as tabelas se ainda não existirem (execute apenas na primeira vez)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vetor (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome_vetor VARCHAR(255) NOT NULL,
            descricao VARCHAR(255) NOT NULL,
            vetor_aleatorio LONGTEXT NOT NULL,
            vetor_ordenado LONGTEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tempos_embaralhamento (
            id INT AUTO_INCREMENT PRIMARY KEY,
            vetor_id INT NOT NULL,
            tempo_embaralhamento FLOAT NOT NULL,
            FOREIGN KEY (vetor_id) REFERENCES vetor(id)
        );
    """)

    # Função para gerar um vetor aleatorio de números inteiros sem repetição
    def gerar_vetor(tamanho_vetor):
        """
        Gera um vetor aleatório de números inteiros sem repetição até 50.000 utilizando o algoritmo 'reservoir
        sampling'.

        Args:
            tamanho_vetor (int): Tamanho do vetor a ser gerado.

        Returns:
            List: Vetor aleatório de números inteiros.
        """
        reservoir = []
        for i in range(tamanho_vetor):
            if len(reservoir) < tamanho_vetor:
                reservoir.append(i)
            else:
                # Seleciona um índice aleatório entre 0 e len(reservoir) - 1
                j = random.randrange(len(reservoir))
                reservoir[j] = i

        # Embaralha o vetor 'reservoir' para garantir aleatoriedade
        random.shuffle(reservoir)

        return reservoir

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

    # Salvar dados no banco de dados
    def salvar_dados_no_banco(conn, cursor, tamanho_vetor, vetor_gerado, vetor_embaralhado, tempos_embaralhamento):
        """
        Salva os dados do vetor no banco de dados MySQL.

        Args:
            conn (MySQLConnection): Conexão com o banco de dados MySQL.
            cursor (MySQLCursor): Cursor para executar comandos SQL.
            tamanho_vetor (int): Tamanho do vetor.
            vetor_gerado (List): Vetor aleatório gerado.
            vetor_embaralhado (List): Vetor aleatório embaralhado.
            tempos_embaralhamento (List): Tempos de embaralhamento do vetor.
        """
        vetor_gerado_json = json.dumps(vetor_gerado)
        vetor_embaralhado_json = json.dumps(vetor_embaralhado)

        # Inserir dados na tabela "vetor"
        cursor.execute("""
            INSERT INTO vetor (nome_vetor, descricao, vetor_aleatorio, vetor_ordenado)
            VALUES (%s, %s, %s, %s)
        """, (
            "Vetor Aleatório e Ordenado",  # Substitua por nome real do vetor
            "Descrição do seu vetor",  # Substitua por uma descrição real
            vetor_embaralhado_json,
            vetor_gerado_json
        ))

        # Inserir dados na tabela "tempos_embaralhamento"
        for tempo_embaralhamento in tempos_embaralhamento:
            cursor.execute("""
                INSERT INTO tempos_embaralhamento (vetor_id, tempo_embaralhamento)
                VALUES (LAST_INSERT_ID(), %s)
            """, (tempo_embaralhamento,))

        # Confirmar as alterações no banco de dados
        conn.commit()

    # Gerar gráficos
    scatter_plot(range(len(vetor_embaralhado)), vetor_embaralhado, 'scatter_plot.png')
    line_chart(range(len(vetor_gerado)), vetor_gerado, 'line_chart.png')
    bar_chart(range(len(vetor_gerado)), vetor_gerado, 'bar_chart.png')
    bubble_chart(range(len(vetor_embaralhado)), vetor_embaralhado,
                 [random.randint(1, 100) for _ in range(len(vetor_embaralhado))], 'bubble_chart.png')
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
