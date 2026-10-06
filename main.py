from functools import wraps
import mimetypes

from flask import Flask, render_template, request, redirect, url_for, session, Response, flash
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
    lojas_ativas = loja_repo.listar_por_status('Ativo')
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

    lista_itens = catalogo_repo.listar_todos()
    livros = [item for item in lista_itens if isinstance(item, Livro)]
    revistas = [item for item in lista_itens if isinstance(item, Revista)]
    discos = [item for item in lista_itens if isinstance(item, Disco)]
    
    return render_template('painel.html', usuario=usuario, livros=livros, revistas=revistas, discos=discos)

# Catálogo
@app.route('/catalogo')
@login_required
def catalogo():
    return redirect(url_for('painel'))

@app.route('/item/<int:id_item>/imagem')
@login_required
def imagem_item(id_item):
    resultado = catalogo_repo.buscar_imagem(id_item)

    dados, caminho = resultado
    tipo_img = mimetypes.guess_type(caminho or '')[0] or 'image/jpeg'
    return Response(dados, mimetype=tipo_img, headers={'Cache-Control': 'private, max-age=86400'})

# Cadastrar loja
@app.route('/loja/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar_loja():
    if request.method == 'POST':
        nome_loja = request.form['nome_loja'].strip()
        cidade = request.form['cidade'].strip()

        if not nome_loja or not cidade:
            return render_template('cadastrar_loja.html', erro = "Preencha o nome e a cidade da loja")

        loja_repo.salvar_loja(Loja(nome_loja, cidade))
        flash('Loja cadastrada! Ela aparecerá no site assim que for aprovada.')
        return redirect(url_for('painel'))

    return render_template('cadastrar_loja.html')

# Listar Lojas
@app.route('/lojas')
@login_required
def listar_lojas():
    lista_lojas = loja_repo.listar_por_status('Ativo')
    return render_template('lojas.html', lojas=lista_lojas)

# Detalhes da loja
@app.route('/loja/<int:id_loja>')
@login_required
def loja_detalhe(id_loja):
    loja = loja_repo.buscar_por_id(id_loja)
    if loja is None or loja.status != 'Ativo':
        return redirect(url_for('listar_lojas'))
    return render_template('loja_detalhe.html', loja=loja)

# Avaliar loja
@app.route('/loja/<int:id_loja>/avaliar', methods = ['GET', 'POST'])
@login_required
def avaliar_loja(id_loja):
    loja = loja_repo.buscar_por_id(id_loja)
    if loja is None:
        return redirect(url_for('lojas'))

    if request.method == 'POST':
        cliente = request.form['cliente']
        nota = float(request.form['nota'])

        avaliacao = Avaliacoes(cliente, nota)
        avaliacoes_repo.salvar_avaliacao(id_loja, avaliacao)
        return redirect(url_for('listar_avaliacoes', id_loja=id_loja))

    return render_template('avaliar.html', loja=loja)

# Listar avaliações de um restaurante
@app.route('/loja/<int:id_loja>/avaliacoes')
@login_required
def listar_avaliacoes(id_loja):
    loja = loja_repo.listar_completo(id_loja)
    if loja is None:
        return redirect(url_for('listar_lojas'))

    return render_template('avaliacoes.html', loja=loja)

# Listar catálogo de uma loja específica
@app.route('/loja/<int:id_loja>/catalogo')
@login_required
def listar_catalogo(id_loja):
    loja = loja_repo.buscar_por_id(id_loja)
    if loja is None:
        return redirect(url_for('listar_lojas'))

    itens = catalogo_repo.listar_por_loja(id_loja)
    livros = [item for item in itens if isinstance(item, Livro)]
    revistas = [item for item in itens if isinstance(item, Revista)]
    discos = [item for item in itens if isinstance(item, Disco)]

    return render_template('catalogo.html', loja=loja, livros=livros, revistas=revistas, dsicos=discos)


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

# Cadastrar novo item do catatlogo
@app.route('/loja/<int:id_loja>/catalogo/novo', methods=['GET', 'POST'])
@login_required
def novo_item_catalogo(id_loja):
    loja = loja_repo.buscar_por_id(id_loja)
    if loja is None:
        return redirect(url_for('listar_lojas'))

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