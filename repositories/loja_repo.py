from database.db import conectar
from models.loja import Loja

def salvar_loja(loja):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO lojas (nome_loja, cidade, status) VALUES (%s, %s, %s)
    """, (loja.nome_loja, loja.cidade, 'Pendente'))
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

def atualizar_status(id_loja, novo_status):
    if novo_status not in Loja.STATUS_VALIDOS:
        raise ValueError(f"Status inválido: {novo_status}")

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE lojas SET status = %s WHERE id = %s",
        (novo_status, id_loja)
    )
    conexao.commit()
    conexao.close()

def listar_completo(nome_loja):
    from repositories import avaliacao_repo, catalogo_repo

    loja = buscar_por_nome(nome_loja)
    if loja is None:
        return None

    for avaliacao in avaliacao_repo.listar_por_loja(nome_loja):
        loja._avaliacoes.append(avaliacao)

    for item in catalogo_repo.listar_por_loja(nome_loja):
        loja.adicionar_catalogo(item)

    return loja