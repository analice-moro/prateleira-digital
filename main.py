from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from database.db import tabela_loja, tabela_avaliacao
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

app = Flask(__name__)
app.secret_key = "3itaQue-ch4veDlfic1l"

@app.context_processor
def injetar_usuario_atual():
    usuario_atual = None
    if 'usuario_id' in session:
        usuario_atual = usuario_repo.buscar_por_id(session['usuario_id'])
    return {'usuario_atual': usuario_atual}

def login_required(funcao):
    @wraps(funcao)
    def verificar(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        return funcao(*args, **kwargs)
    return verificar

def admin_required(funcao):
    @wraps(funcao)
    def verificar(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))

        usuario = admin_repo.buscar_por_id(session['usuario_id'])
        if usuario is None or not usuario._is_admin:
            return redirect(url_for('painel'))

        return funcao(*args, **kwargs)
    return verificar

# Landing Page
@app.route('/')
def index():
    lojas_ativas = loja_repo.listar_por_status('ativo')
    logado = 'usuario_id' in session
    return render_template('landing.html', lojas=lojas_ativas, logado=logado)

# Cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
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
@app.route('/login', methods=['GET', 'POST'])
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
@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    return redirect(url_for('login'))

# Painel
@app.route('/painel')
@login_required
def painel():
    usuario = usuario_repo.buscar_por_id(session['usuario_id'])
    return render_template('painel.html', usuario=usuario)

# Catálogo
@app.route('/catalogo')
@login_required
def catalogo():
    lista_itens = catalogo_repo.listar_todos()
    livros = [item for item in lista_itens if isinstance(item, Livro)]
    revistas = [item for item in lista_itens if isinstance(item, Revista)]
    discos = [item for item in lista_itens if isinstance(item, Disco)]

    

@app.route('/admin')
@admin_required
def admin_pendentes():
    pendentes = loja_repo.listar_por_status('Pendente')
    return render_template('admin.html', lojas=pendentes)

@app.route('/admin/lojas')
@admin_required
def admin_lojas():
    todos = loja_repo.listar_todos()
    return render_template('admin_lojas.html', lojas=todos, status_validos = Loja.STATUS_VALIDOS)

@app.route('/admin/loja/<int:id_loja>/status', methods = ['POST'])
@admin_required
def admin_atualizar_status(id_loja):
    novo_status = request.form['status']

    if novo_status not in Loja.STATUS_VALIDOS:
        return redirect(url_for('admin_lojas'))

    loja_repo.atualizar_status(id_loja, novo_status)
    origem = request.form.get('origem', 'admin_lojas')
    return redirect(url_for(origem))

@app.route('/loja/<int:ud_loja>/catalogo/novo', methods=['GET', 'POST'])
@login_required
def novo_item_catalogo(id_loja):
    loja = loja_repo.buscar_por_id(id_loja)
    if loja is None:
        return redirect(url_for('lojas'))

    if request.method == 'POST':
        tipo = request.form['tipo']
        titulo = request.form['titulo']
        ano_lancamento = request.form['ano_lancamento']
        genero = request.form['genero']
        preco = float(request.form['preco'])
        imagem = request.form['imagem']

        if tipo == "Livro":
            item = Livro(titulo, request.form.get('autor', ''), ano_lancamento, genero, preco, request.form.get('sinopse', ''), imagem)
        elif tipo == "Revista":
            item = Revista(titulo, request.form.get('editora', ''), ano_lancamento, genero, request.form.get('periodicidade', ''), preco, imagem)
        elif tipo == "Disco":
            item = Disco(titulo, request.form.get('artista', ''), ano_lancamento, genero, request.form.get('formato_midia', ''), preco, imagem)
        else:
            return render_template('catalogo_novo.html', loja = loja, erro='Tipo de item inválido')

        catalogo_repo.salvar_item(id_loja, item)
        return redirect(url_for('listar_catalogo', id_loja=id_loja))

    return render_template('catalogo_novo.html', loja=loja)

if __name__ == '__main__':
    tabela_loja()
    tabela_avaliacao()
    catalogo_repo.tabela_catalogo()
    usuario_repo.tabela_usuario()
    admin_repo.tabela_admin()

    app.run(debug=True)