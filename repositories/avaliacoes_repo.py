from database.db import conectar
from models.item_catalogo.avaliacoes import Avaliacoes

def salvar_avaliacao_loja(id_loja, avaliacao):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO avaliacoes_lojas (id_loja, nome_usuario, nota_avaliacao)
        VALUES (%s, %s, %s)
    """, (id_loja, avaliacao._cliente, avaliacao._nota))
    conexao.commit()
    conexao.close()

def salvar_avaliacao_item(id_item, avaliacao):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO avaliacoes_itens (id_item, nome_usuario, nota_avaliacao) VALUES (%s, %s, %s)
    """, (id_item, avaliacao._cliente, avaliacao._nota))
    conexao.commit()
    conexao.close()

def listar_por_loja(id_loja):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT nome_usuario, nota_avaliacao FROM avaliacoes_lojas WHERE id_loja = %s",
        (id_loja,)
    )
    linhas = cursor.fetchall()
    conexao.close()

    avaliacoes = []
    for nome_usuario, nota in linhas:
        avaliacoes.append(Avaliacoes(nome_usuario, float(nota)))
    return avaliacoes

def listar_por_item(id_item):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT nome_usuario, nota_avaliacao FROM avaliacoes_itens WHERE id_item = %s
    """, (id_item,))
    linhas = cursor.fetchall()
    conexao.close()

    avaliacoes = []
    for nome_usuario, nota in linhas:
        avaliacoes.append(Avaliacoes(nome_usuario, float(nota)))
    return avaliacoes