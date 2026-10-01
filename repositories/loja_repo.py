from database.db import conectar
from models.loja import Loja

def salvar(loja):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO lojas (nome_loja, cidade, status) VALUES (%s, %s, %s)
    """, (loja.nome, loja.cidade, 'Pendente'))
    conexao.commit()
    id_gerado = cursor.lastrowid
    conexao.close()

    loja.definir_status("Pendente")
    loja.id = id_gerado
    return id_gerado

def buscar_por_nome(nome_loja):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome_loja, cidade, status FROM lojas WHERE nome_loja = %s
    """, (nome_loja,))
    resultado = cursor.fetchone()
    conexao.close()

    if resultado is None:
        return None

    id_loja, nome_loja, cidade, status = resultado
    loja = Loja(nome_loja, cidade)
    loja.definir_status(status)
    loja.id = id_loja
    return loja

def listar_todos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome_loja, cidade, status FROM lojas
    """)
    resultados = cursor.fetchall()
    conexao.close()

    lojas = []
    for id_loja, nome_loja, cidade, status in resultados:
        loja = Loja(nome_loja, cidade)
        loja.definir_status(status)
        loja.id = id_loja
        lojas.append(loja)
    return lojas