from flask import render_template, request, redirect, url_for
from models.loja import Loja
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

