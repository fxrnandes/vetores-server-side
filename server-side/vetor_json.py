import random
import time
import json
import mysql.connector
from randomizer import embaralhar_fisher_yates
from graficos import create_all_charts


def generate_vetor_json(tamanho_vetor=1000):
    if tamanho_vetor < 1 or tamanho_vetor > 50000:
        return {"error": "Tamanho do vetor inválido. Deve estar entre 1 e 50.000."}

    try:
        conn = mysql.connector.connect(host="127.0.0.1", port=3306, database="n2-ss", user="root", password="")
        cursor = conn.cursor()
    except mysql.connector.Error as e:
        return {"error": f"Erro ao conectar ao banco de dados: {e}"}

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
            tempo_ordenacao FLOAT NOT NULL,
            FOREIGN KEY (vetor_id) REFERENCES vetor(id)
        );
    """)

    # Adiciona a coluna tempo_ordenacao se ela não existir
    try:
        cursor.execute("ALTER TABLE tempos_embaralhamento ADD COLUMN tempo_ordenacao FLOAT;")
    except mysql.connector.Error as err:
        if err.errno == 1060:  # Duplicate column error
            pass
        else:
            return {"error": f"Erro ao modificar a tabela: {err}"}

    def gerar_vetor(tamanho_vetor):
        vetor = list(range(1, tamanho_vetor + 1))
        random.shuffle(vetor)
        return vetor

    vetor_gerado = gerar_vetor(tamanho_vetor)
    vetor_embaralhado = vetor_gerado.copy()
    tempos_embaralhamento = []
    tempos_ordenacao = []

    for _ in range(3):
        # Tempo de embaralhamento
        start_time = time.time()
        embaralhar_fisher_yates(vetor_embaralhado)
        end_time = time.time()
        tempos_embaralhamento.append(end_time - start_time)

        # Tempo de ordenação
        start_time = time.time()
        vetor_embaralhado.sort()
        end_time = time.time()
        tempos_ordenacao.append(end_time - start_time)

        # Embaralhar novamente para a próxima interação
        random.shuffle(vetor_embaralhado)

    vetor_gerado.sort()

    vetor_gerado_json = json.dumps(vetor_gerado)
    vetor_embaralhado_json = json.dumps(vetor_embaralhado)

    cursor.execute("""
        INSERT INTO vetor (nome_vetor, descricao, vetor_aleatorio, vetor_ordenado)
        VALUES (%s, %s, %s, %s)
    """, (
        "Vetor Aleatório e Ordenado",
        "Descrição do vetor",
        vetor_embaralhado_json,
        vetor_gerado_json
    ))

    vetor_id = cursor.lastrowid

    for tempo_emb, tempo_ord in zip(tempos_embaralhamento, tempos_ordenacao):
        cursor.execute("""
            INSERT INTO tempos_embaralhamento (vetor_id, tempo_embaralhamento, tempo_ordenacao)
            VALUES (%s, %s, %s)
        """, (vetor_id, tempo_emb, tempo_ord))

    conn.commit()
    cursor.close()
    conn.close()

    graficos = create_all_charts(vetor_embaralhado, vetor_gerado)

    vetor_json = {
        "nome_vetor": "Vetor Aleatório e Ordenado",
        "descricao": "Descrição do vetor",
        "vetor_aleatorio": vetor_embaralhado,
        "vetor_ordenado": vetor_gerado,
        "tempos_embaralhamento": tempos_embaralhamento,
        "tempos_ordenacao": tempos_ordenacao,
        "graficos": graficos
    }

    return vetor_json
