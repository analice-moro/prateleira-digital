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

# Listar lojas com status "Pendente"
def admin_pendentes():
    pendentes = loja_repo.listar_por_status('Pendente')
    return render_template('admin.html', lojas=pendentes)

# Listar lojas com todos os status
def admin_lojas():
    todos = loja_repo.listar_todos()
    return render_template('admin_lojas.html', lojas=todos, status_validos = Loja.STATUS_VALIDOS)

# Atualizar status da loja
def admin_atualizar_status(id_loja):
    novo_status = request.form['status']

    if novo_status not in Loja.STATUS_VALIDOS:
        return redirect(url_for('admin_lojas'))

    loja_repo.atualizar_status(id_loja, novo_status)
    origem = request.form.get('origem', 'admin_lojas')
    return redirect(url_for(origem))

