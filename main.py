from functools import wraps
import os
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, session
from database.db import tabela_loja, tabela_avaliacao_loja, tabela_avaliacao_item
from repositories import usuario_repo
from repositories import catalogo_repo
from repositories import admin_repo
from routes import admin_route, catalogo_route, lojas_route, painel_route

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

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
    return painel_route.index()

# Cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    return painel_route.cadastro()

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    return painel_route.login()

# Logout
@app.route('/logout')
def logout():
    return painel_route.logout()

# Painel
@app.route('/painel')
@login_required
def painel():
    return painel_route.painel()

# Catálogo
@app.route('/catalogo')
@login_required
def catalogo():
    return catalogo_route.catalogo()

@app.route('/item/<int:id_item>/imagem')
@login_required
def imagem_item(id_item):
    return catalogo_route.imagem_item(id_item)

# Cadastrar loja
@app.route('/loja/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar_loja():
    return lojas_route.cadastrar_loja()

# Listar Lojas
@app.route('/lojas')
@login_required
def listar_lojas():
    return lojas_route.listar_lojas()

# Detalhes da loja
@app.route('/loja/<int:id_loja>')
@login_required
def loja_detalhe(id_loja):
    return lojas_route.loja_detalhe(id_loja)

# Avaliar loja
@app.route('/loja/<int:id_loja>/avaliar', methods = ['GET', 'POST'])
@login_required
def avaliar_loja(id_loja):
    return lojas_route.avaliar_loja(id_loja)

# Listar avaliações de uma loja
@app.route('/loja/<int:id_loja>/avaliacoes')
@login_required
def listar_avaliacoes(id_loja):
    return lojas_route.listar_avaliacoes(id_loja)

# Listar catálogo de uma loja específica
@app.route('/loja/<int:id_loja>/catalogo')
@login_required
def listar_catalogo(id_loja):
    return catalogo_route.listar_catalogo(id_loja)

# Detalhes de um produto de determinada loja
@app.route('/item/<int:id_item>')
@login_required
def item_detalhe(id_item):
    return catalogo_route.item_detalhe(id_item)

@app.route('/item/<int:id_item>/avaliar', methods= ['GET', 'POST'])
@login_required
def avaliar_item(id_item):
    return catalogo_route.avaliar_item(id_item)

@app.route('/admin')
@admin_required
def admin_pendentes():
    return admin_route.admin_pendentes()

@app.route('/admin/lojas')
@admin_required
def admin_lojas():
    return admin_route.admin_lojas()

@app.route('/admin/loja/<int:id_loja>/status', methods = ['POST'])
@admin_required
def admin_atualizar_status(id_loja):
    return admin_route.admin_atualizar_status(id_loja)

# Cadastrar novo item do catatlogo
@app.route('/loja/<int:id_loja>/catalogo/novo', methods=['GET', 'POST'])
@login_required
def novo_item_catalogo(id_loja):
    return catalogo_route.novo_item_catalogo(id_loja)

# Remover item do catálogo
@app.route('/item/<int:id_item>/remover', methods=['POST'])
@admin_required
def excluir_item(id_item):
    return catalogo_route.excluir_item(id_item)

# Remover loja
@app.route('/admin/loja/<int:id_loja>/remover', methods=['POST'])
@admin_required
def excluir_loja(id_loja):
    return lojas_route.excluir_loja(id_loja)

if __name__ == '__main__':
    tabela_loja()
    usuario_repo.tabela_usuario()  
    tabela_avaliacao_loja()
    catalogo_repo.tabela_catalogo()
    tabela_avaliacao_item()

    app.run(debug=True)