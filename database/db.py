import mysql.connector

def conectar():
    conexao = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "root",
        database = "prateleira_digital"
    )
    return conexao

def tabela_loja():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lojas(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome_loja VARCHAR(100) NOT NULL,
            cidade VARCHAR(100) NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'pendente'
        )
    """)
    conexao.commit()
    conexao.close()

def tabela_avaliacao():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes(
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_loja INT,
            nome_usuario VARCHAR(100) NOT NULL,
            nota_avaliacao DECIMAL(2,1),
            FOREIGN KEY (id_loja) REFERENCES lojas(id)
        )
    """)
    conexao.commit()
    conexao.close()

def criar_loja(nome_loja, cidade):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO lojas(nome_loja, cidade) VALUES (%s, %s)
    """, (nome_loja, cidade))
    conexao.commit()
    conexao.close()

def listar_lojas():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT * FROM lojas
    """)
    lojas = cursor.fetchall()
    for loja in lojas:
        print(loja)
    conexao.commit()
    conexao.close()

def criar_avaliacao(id_loja, nome_usuario, nota_avaliacao):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO avaliacoes(id_loja, nome_usuario, nota_avaliacao) VALUES (%s, %s, %s)
    """, (int(id_loja), nome_usuario, float(nota_avaliacao)))
    conexao.commit()
    conexao.close()

def listar_avaliacoes():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT avaliacoes.id, lojas.nome_loja, avaliacoes.nome_usuario, avaliacoes.nota_avaliacao FROM avaliacoes JOIN lojas ON avaliacoes.id_loja = lojas.id
    """)
    avaliacoes = cursor.fetchall()
    for avaliacao in avaliacoes:
        print(avaliacao)
    conexao.commit()
    conexao.close()