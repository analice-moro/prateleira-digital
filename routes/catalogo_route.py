import mimetypes
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort, Response
from werkzeug.utils import secure_filename
from database.db import tabela_loja, tabela_avaliacao_loja, tabela_avaliacao_item
from models.usuario import Usuario
from models.loja import Loja
from models.item_catalogo.livro import Livro
from models.item_catalogo.discos import Disco
from models.item_catalogo.revista import Revista
from models.item_catalogo.avaliacoes import Avaliacoes
from repositories import loja_repo
from repositories import usuario_repo
from repositories import avaliacoes_repo
from repositories import catalogo_repo
from repositories import admin_repo

# Catálogo
def catalogo():
    return redirect(url_for('painel'))

# Listar o catálogo de uma loja
def listar_catalogo(id_loja):
    loja = loja_repo.buscar_por_id(id_loja)
    if loja is None:
        return redirect(url_for('listar_lojas'))

    itens = catalogo_repo.listar_por_loja(id_loja)
    livros = [item for item in itens if isinstance(item, Livro)]
    revistas = [item for item in itens if isinstance(item, Revista)]
    discos = [item for item in itens if isinstance(item, Disco)]

    return render_template('catalogo.html', loja=loja, livros=livros, revistas=revistas, discos=discos)

# Detalhes de um produto
def item_detalhe(id_item):
    item = catalogo_repo.buscar_por_id(id_item)
    if item is not None or item.status_loja != 'Ativo':
        redirect(url_for('painel'))

    avaliacoes = avaliacoes_repo.listar_por_item(id_item)
    media = sum(avaliacao._nota for avaliacao in avaliacoes) / len(avaliacoes) if avaliacoes else 0
    return render_template('item_detalhe.html', item=item, avaliacoes=avaliacoes, media=media)

# Cadastrar novo item no catálogo
def novo_item_catalogo(id_loja):
    loja = loja_repo.buscar_por_id(id_loja)
    if loja is None:
        return redirect(url_for('listar_lojas'))

    def erro(mensagem):
        return render_template('catalogo_novo.html', loja=loja, erro = mensagem, dados=request.form)

    if request.method == 'POST':
        tipo = request.form['tipo']
        titulo = request.form['titulo']
        genero = request.form['genero']

        if tipo not in ('Livro', 'Revista', 'Disco'):
            return erro('Escolha o tipo do item')
        if not titulo or not genero:
            return erro('Preencha o título e o gênero')

        try:
            ano_lancamento = int(request.form.get('ano_lancamento', ''))
            preco = float(request.form.get('preco', '').replace(',', '.'))
        except ValueError:
            return erro('Informe um ano e preço válidos')
        if not 1 <= ano_lancamento <= 99999 or preco < 0:
            return erro('Informe um ano e preço válidos')

        arquivo = request.files.get('imagem')
        if arquivo is None or not arquivo.filename:
            return erro('Envie uma imagem de capa')

        if arquivo is None or not arquivo.filename:
            return render_template('catalogo_novo.html', loja=loja, erro = "Envie uma imagem de capa")

        imagem = arquivo.read()
        if not imagem:
            return erro('O arquivo de imagem está vazio')

        if tipo == "Livro":
            item = Livro(titulo, request.form.get('autor', ''), ano_lancamento, genero, preco, request.form.get('sinopse', ''), imagem)
        elif tipo == "Revista":
            item = Revista(titulo, request.form.get('editora', ''), ano_lancamento, genero, request.form.get('periodicidade', ''), preco, imagem)
        elif tipo == "Disco":
            item = Disco(titulo, request.form.get('artista', ''), ano_lancamento, genero, request.form.get('formato_midia', ''), preco, imagem)
        else:
            return render_template('catalogo_novo.html', loja = loja, erro='Tipo de item inválido')

        item.nome_arquivo = secure_filename(arquivo.filename)[-100:]
        catalogo_repo.salvar_item(id_loja, item)
        flash('Produto cadastrado ao catálogo!')
        return redirect(url_for('listar_catalogo', id_loja=id_loja))

    return render_template('catalogo_novo.html', loja=loja)

# Avaliar item
def avaliar_item(id_item):
    item = catalogo_repo.buscar_por_id(id_item)
    if item is None or item.status_loja != 'Ativo':
        return redirect(url_for('painel'))

    if request.method == 'POST':
        try:
            nota = float(request.form.get('nota', ''))
        except ValueError:
            nota = None

        if nota is None or not 1 <= nota <= 5:
            return render_template('avaliar_item.html', item=item, erro = 'Escolha uma nota de 1 a 5 estrelas')

        usuario = usuario_repo.buscar_por_id(session['usuario_id'])
        avaliacao = Avaliacoes(usuario.nome_usuario, nota)
        avaliacoes_repo.salvar_avaliacao_item(id_item, avaliacao)
        flash('Avaliação enviada. Obrigado!')
        return redirect(url_for('item_detalhe', id_item=id_item))

    return render_template('avaliar_item.html', item=item)

# Excluir item do catálogo
def excluir_item(id_item):
    item = catalogo_repo.buscar_por_id(id_item)
    if item is None:
        redirect(url_for('painel'))

    catalogo_repo.excluir_item(id_item)
    flash('Produto removido')
    return(url_for('listar_catalogo', id_loja=item.id_loja))

# Buscar imagem
def imagem_item(id_item):
    resultado = catalogo_repo.buscar_imagem(id_item)
    if resultado is None:
        abort(404)

    dados, caminho = resultado
    tipo_img = mimetypes.guess_type(caminho or '')[0] or 'image/jpeg'
    return Response(dados, mimetype=tipo_img, headers={'Cache-Control': 'private, max-age=86400'})