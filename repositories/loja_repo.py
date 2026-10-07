from database.db import conectar
from models.loja import Loja
from repositories import avaliacoes_repo, catalogo_repo

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

def buscar_por_nome_e_cidade(nome_loja, cidade):
    """Procura uma loja com o mesmo nome na mesma cidade, ignorando maiúsculas e espaços nas pontas."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome_loja, cidade, status FROM lojas
        WHERE LOWER(TRIM(nome_loja)) = LOWER(TRIM(%s))
          AND LOWER(TRIM(cidade)) = LOWER(TRIM(%s))
        LIMIT 1
    """, (nome_loja, cidade))
    resultado = cursor.fetchone()
    conexao.close()
 
    if resultado is None:
        return None
 
    id_loja, nome_loja, cidade, status = resultado
    loja = Loja(nome_loja, cidade)
    loja.definir_status(status)
    loja.id = id_loja
    return loja

def buscar_por_id(id_loja):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome_loja, cidade, status FROM lojas WHERE id = %s
    """, (id_loja,))
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

    for loja in lojas:
        for avaliacao in avaliacoes_repo.listar_por_loja(nome_loja):
            loja._avaliacoes.append(avaliacao)
        
        for item in catalogo_repo.listar_por_loja(nome_loja):
            loja.adicionar_catalogo(item)
    
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

def _carregar_avaliacoes(loja):
    for avaliacao in avaliacoes_repo.listar_por_loja(loja.id):
        loja._avaliacoes.append(avaliacao)

def listar_completo(nome_loja):

    loja = buscar_por_nome(nome_loja)
    if loja is None:
        return None

    for avaliacao in avaliacoes_repo.listar_por_loja(nome_loja):
        loja._avaliacoes.append(avaliacao)

    for item in catalogo_repo.listar_por_loja(nome_loja):
        loja.adicionar_catalogo(item)

    return loja

def listar_por_status(status):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome_loja, cidade, status FROM lojas WHERE status = %s
    """, (status,))
    resultados = cursor.fetchall()
    conexao.close()

    lojas = []
    for id_loja, nome_loja, cidade, status_banco in resultados:
        loja = Loja(nome_loja, cidade)
        loja.definir_status(status_banco)
        loja.id = id_loja
        lojas.append(loja)

    for loja in lojas:
        _carregar_avaliacoes(loja)
    return lojas