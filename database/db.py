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

def tabela_avaliacao_loja():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes_lojas(
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_loja INT,
            nome_usuario VARCHAR(100) NOT NULL,
            nota_avaliacao DECIMAL(2,1),
            FOREIGN KEY (id_loja) REFERENCES lojas(id)
        )
    """)
    conexao.commit()
    conexao.close()

def tabela_avaliacao_item():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes_itens(
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_item INT,
            nome_usuario VARCHAR(100) NOT NULL,
            nota_avaliacao DECIMAL (2,1),
            FOREIGN KEY (id_item) REFERENCES itens_catalogo(id)
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

def criar_avaliacao_loja(id_loja, nome_usuario, nota_avaliacao):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO avaliacoes_lojas(id_loja, nome_usuario, nota_avaliacao) VALUES (%s, %s, %s)
    """, (int(id_loja), nome_usuario, float(nota_avaliacao)))
    conexao.commit()
    conexao.close()

def listar_avaliacoes_loja():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT avaliacoes_lojas.id, lojas.nome_loja, avaliacoes_lojas.nome_usuario, avaliacoes_lojas.nota_avaliacao FROM avaliacoes_lojas JOIN lojas ON avaliacoes_lojas.id_loja = lojas.id
    """)
    avaliacoes = cursor.fetchall()
    for avaliacao in avaliacoes:
        print(avaliacao)
    conexao.commit()
    conexao.close()

def criar_avaliacao_item(id_item, nome_usuario, nota_avaliacao):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO avaliacoes_itens(id_item, nome_usuario, nota_avaliacao) VALUES (%s, %s, %s)
    """, (int(id_item), nome_usuario, float(nota_avaliacao)))
    conexao.commit()
    conexao.close()

def listar_avaliacoes_item():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT avaliacoes_itens.id, itens_catalogo.titulo_item, avaliacoes_itens.nome_usuario, avaliacoes_itens.nota_avaliacao FROM avaliacoes_itens JOIN itens_catalogo ON avaliacoes_itens.id_item = itens_catalogo.id 
    """)
    avaliacoes = cursor.fetchall()
    for avaliacao in avaliacoes:
        print(avaliacao)
    conexao.commit()
    conexao.close()