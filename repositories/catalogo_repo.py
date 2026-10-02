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

    with open(item.imagem, 'rb') as arquivo:
        dados_binarios = arquivo.read()

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO itens_catalogo
            (id_loja, titulo_item, genero_item, ano_lancamento_item, preco_item, tipo_item, caminho_img_item, imagem_item, autor_item, sinopse_item, artista_item, formato_midia_item, editora_item, periodicidade_item)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (id_loja, item._titulo, item._genero, item._ano_lancamento, item._preco, tipo_item, item.imagem, dados_binarios, autor_item, sinopse_item, artista_item, formato_midia_item, editora_item, periodicidade_item))
    conexao.commit()
    conexao.close()

def listar_por_loja(id_loja):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT titulo_item, genero_item, ano_lancamento_item, preco_item, tipo_item, caminho_img_item, imagem_item, autor_item, sinopse_item, artista_item, formato_midia_item, editora_item, periodicidade_item 
        FROM itens_catalogo
        WHERE id_loja = %s
    """, (id_loja,))
    linhas = cursor.fetchall()
    conexao.close()

    itens = []
    for titulo, genero, ano_lancamento, preco, tipo_item, caminho_img, imagem, autor, sinopse, artista, formato_midia, editora, periodicidade in linhas:
        preco = float(preco)
        if tipo_item == "Livro":
            img = reconstruir_imagem(caminho_img, imagem)
            itens.append(Livro(titulo, autor, ano_lancamento, genero, preco, sinopse, img))
        elif tipo_item == "Disco":
            img = reconstruir_imagem(caminho_img, imagem)
            itens.append(Disco(titulo, artista, ano_lancamento, genero, formato_midia, preco, img))
        elif tipo_item == "Revista":
            img = reconstruir_imagem(caminho_img, imagem)
            itens.append(Revista(titulo, editora, ano_lancamento, genero, periodicidade, preco, img))
    return itens

def reconstruir_imagem(caminho_img, imagem):
    dados_binarios = imagem
    with open(caminho_img, 'wb') as arquivo:
        arquivo.write(dados_binarios)

    return dados_binarios