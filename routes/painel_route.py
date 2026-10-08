from flask import Flask, render_template, request, redirect, url_for, session, Response, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
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

# Landing page
def index():
    lojas_ativas = loja_repo.listar_por_status('Ativo')
    logado = 'usuario_id' in session
    return render_template('landing.html', lojas=lojas_ativas, logado=logado)

# Cadastro
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha_hash = generate_password_hash(request.form['senha'])

        if usuario_repo.buscar_por_email(email) is not None:
            return render_template('cadastro.html', erro="Este email já está cadastrado")

        usuario = Usuario(nome, email, senha_hash)
        usuario_repo.salvar_usuario(usuario)
        return redirect(url_for('login'))

    return render_template('cadastro.html')

# Login
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = usuario_repo.buscar_por_email(email)
        if usuario and check_password_hash(usuario._senha_hash, senha):
            session['usuario_id'] = usuario.id
            return redirect(url_for('painel'))

        return render_template('login.html', erro='Email ou senha inválidos')
    return render_template('login.html')

# Logout
def logout():
    session.pop('usuario_id', None)
    return redirect(url_for('login'))

# Painel
def painel():
    usuario = usuario_repo.buscar_por_id(session['usuario_id'])

    lista_itens = catalogo_repo.listar_todos()
    livros = [item for item in lista_itens if isinstance(item, Livro)]
    revistas = [item for item in lista_itens if isinstance(item, Revista)]
    discos = [item for item in lista_itens if isinstance(item, Disco)]
    
    return render_template('painel.html', usuario=usuario, livros=livros, revistas=revistas, discos=discos)