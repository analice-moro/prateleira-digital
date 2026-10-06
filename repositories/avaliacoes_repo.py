from database.db import conectar
from models.item_catalogo.avaliacoes import Avaliacoes

def salvar_avaliacao(id_loja, avaliacao):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO avaliacoes (id_loja, nome_usuario, nota_avaliacao)
        VALUES (%s, %s, %s)
    """, (id_loja, avaliacao._cliente, avaliacao._nota))
    conexao.commit()
    conexao.close()

def listar_por_loja(id_loja):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT nome_usuario, nota_avaliacao FROM avaliacoes WHERE id_loja = %s",
        (id_loja,)
    )
    linhas = cursor.fetchall()
    conexao.close()

    avaliacoes = []
    for nome_usuario, nota in linhas:
        avaliacoes.append(Avaliacoes(nome_usuario, float(nota)))
    return avaliacoes