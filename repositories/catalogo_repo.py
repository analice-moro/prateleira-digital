from database.db import conectar
from models.item_catalogo.livro import Livro
from models.item_catalogo.discos import Disco
from models.item_catalogo.revista import Revista

def tabela_catalogo():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_catalogo (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_loja INT,
            titulo_item VARCHAR(100) NOT NULL,
            genero_item VARCHAR(30) NOT NULL,
            ano_lancamento_item DECIMAL(5) NOT NULL,
            preco_item DECIMAL(10, 2) NOT NULL,
            tipo_item VARCHAR(20) NOT NULL,
            caminho_img_item VARCHAR(100) NOT NULL,
            imagem_item MEDIUMBLOB NOT NULL,
            autor_item VARCHAR(100),
            sinopse_item VARCHAR(255),
            artista_item VARCHAR(100),
            formato_midia_item VARCHAR(50),
            editora_item VARCHAR(50),
            periodicidade_item VARCHAR(20),
            FOREIGN KEY (id_loja) REFERENCES lojas(id)
        )
    """)
    conexao.commit()
    conexao.close()

def salvar_item(id_loja, item):
    if isinstance(item, Livro):
        tipo_item = 'Livro'
        autor_item = item._autor
        sinopse_item = item._sinopse
        artista_item = None
        formato_midia_item = None
        editora_item = None
        periodicidade_item = None
    elif isinstance(item, Disco):
        tipo_item = 'Disco'
        autor_item = None
        sinopse_item = None
        artista_item = item._artista
        formato_midia_item = item._formato_midia
        editora_item = None
        periodicidade_item = None
    elif isinstance(item, Revista):
        tipo_item = 'Revista'
        autor_item = None
        sinopse_item = None
        artista_item = None
        formato_midia_item = None
        editora_item = item._editora
        periodicidade_item = item._periodicidade
    else:
        raise ValueError("O item precisa ser um Livro, Disco ou Revista")

    if isinstance(item.imagem, (bytes, bytearray)):
        dados_binarios = bytes(item.imagem)
        caminho_img = getattr(item, 'nome_arquivo', None) or 'imagem'
    else:
        with open(item.imagem, 'rb') as arquivo:
            dados_binarios = arquivo.read()
        caminho_img = item.imagem

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO itens_catalogo
            (id_loja, titulo_item, genero_item, ano_lancamento_item, preco_item, tipo_item, caminho_img_item, imagem_item, autor_item, sinopse_item, artista_item, formato_midia_item, editora_item, periodicidade_item)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (id_loja, item._titulo, item._genero, item._ano_lancamento, item._preco, tipo_item, caminho_img, dados_binarios, autor_item, sinopse_item, artista_item, formato_midia_item, editora_item, periodicidade_item))
    conexao.commit()
    conexao.close()

def listar_por_loja(id_loja):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, titulo_item, genero_item, ano_lancamento_item, preco_item, tipo_item, autor_item, sinopse_item, artista_item, formato_midia_item, editora_item, periodicidade_item 
        FROM itens_catalogo
        WHERE id_loja = %s
    """, (id_loja,))
    linhas = cursor.fetchall()
    conexao.close()

    itens = []
    for id_item, titulo, genero, ano_lancamento, preco, tipo_item, autor, sinopse, artista, formato_midia, editora, periodicidade in linhas:
        preco = float(preco)
        if tipo_item == "Livro":
            item = Livro(titulo, autor, ano_lancamento, genero, preco, sinopse, None)
        elif tipo_item == "Disco":
            item = Disco(titulo, artista, ano_lancamento, genero, formato_midia, preco, None)
        elif tipo_item == "Revista":
            item = Revista(titulo, editora, ano_lancamento, genero, periodicidade, preco, None)

        item.id = id_item
        item.id_loja = id_loja
        itens.append(item)

    return itens

def reconstruir_imagem(caminho_img, imagem):
    dados_binarios = imagem
    with open(caminho_img, 'wb') as arquivo:
        arquivo.write(dados_binarios)

    return dados_binarios

def listar_todos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT itens_catalogo.id, itens_catalogo.id_loja, lojas.nome_loja, itens_catalogo.titulo_item, itens_catalogo.genero_item, itens_catalogo.ano_lancamento_item, itens_catalogo.preco_item, itens_catalogo.tipo_item, itens_catalogo.autor_item, itens_catalogo.sinopse_item, itens_catalogo.artista_item, itens_catalogo.formato_midia_item, itens_catalogo.editora_item, itens_catalogo.periodicidade_item 
        FROM itens_catalogo 
        JOIN lojas ON lojas.id = itens_catalogo.id_loja
        WHERE lojas.status = 'Ativo' 
    """)
    resultados = cursor.fetchall()
    conexao.close()

    itens = []
    for id_item, id_loja, nome_loja, titulo, genero, ano_lancamento, preco, tipo_item, autor, sinopse, artista, formato_midia, editora, periodicidade in resultados:
        preco = float(preco)
        if tipo_item == "Livro":
            item = Livro(titulo, autor, ano_lancamento, genero, preco, sinopse, None)
        elif tipo_item == "Disco":
            item = Disco(titulo, artista, ano_lancamento, genero, formato_midia, preco, None)
        elif tipo_item == "Revista":
            item = Revista(titulo, editora, ano_lancamento, genero, periodicidade, preco, None)

        item.id = id_item
        item.id_loja = id_loja
        item.nome_loja = nome_loja
        itens.append(item)
    return itens

def buscar_imagem(id_item):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT imagem_item, caminho_img_item FROM itens_catalogo WHERE id = %s
    """, (id_item,))
    linha = cursor.fetchone()
    conexao.close()

    if linha is None or not linha[0]:
        return None
    return linha[0], linha[1]

def buscar_por_id(id_item):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, id_loja, titulo_item, genero_item, ano_lancamento_item, preco_item, tipo_item,
               autor_item, sinopse_item, artista_item, formato_midia_item, editora_item, periodicidade_item
        FROM itens_catalogo
        WHERE id = %s
    """, (id_item,))
    resultado = cursor.fetchone()
    conexao.close()

    if resultado is None:
        return None

    id_item, id_loja, titulo, genero, ano_lancamento, preco, tipo_item, autor, sinopse, artista, formato_midia, editora, periodicidade = resultado
    preco = float(preco)

    if tipo_item == "Livro":
        item = Livro(titulo, autor, ano_lancamento, genero, preco, sinopse, None)
    elif tipo_item == "Disco":
        item = Disco(titulo, artista, ano_lancamento, genero, formato_midia, preco, None)
    elif tipo_item == "Revista":
        item = Revista(titulo, editora, ano_lancamento, genero, periodicidade, preco, None)
    else:
        return None  # tipo desconhecido: evita usar uma variável que não existe

    item.id = id_item
    item.id_loja = id_loja
    return item
    
