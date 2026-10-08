from flask import render_template, request, redirect, url_for, session,flash
from models.loja import Loja
from models.item_catalogo.avaliacoes import Avaliacoes
from repositories import loja_repo
from repositories import usuario_repo
from repositories import avaliacoes_repo

def normalizar(texto):
    return ' '.join((texto or '').split())

# Cadastrar loja
def cadastrar_loja():
    if request.method == 'POST':
        nome_loja = normalizar(request.form['nome_loja'])
        cidade = normalizar(request.form['cidade'])
 
        if not nome_loja or not cidade:
            return render_template('cadastrar_loja.html', erro="Preencha o nome e a cidade da loja",
                                   nome_loja=nome_loja, cidade=cidade)
 
        if loja_repo.buscar_por_nome_e_cidade(nome_loja, cidade) is not None:
            return render_template('cadastrar_loja.html',
                                   erro=f'Já existe uma loja chamada "{nome_loja}" em {cidade}.',
                                   nome_loja=nome_loja, cidade=cidade)
 
        loja_repo.salvar_loja(Loja(nome_loja, cidade))
        flash('Loja cadastrada! Ela aparecerá no site assim que for aprovada.')
        return redirect(url_for('painel'))
 
    return render_template('cadastrar_loja.html')

# Listar lojas
def listar_lojas():
    lista_lojas = loja_repo.listar_por_status('Ativo')
    return render_template('lojas.html', lojas=lista_lojas)

# Mostrar os detalhes da loja
def loja_detalhe(id_loja):
    loja = loja_repo.buscar_com_avaliacoes(id_loja)
    if loja is None or loja.status != 'Ativo':
        return redirect(url_for('listar_lojas'))
    return render_template('loja_detalhe.html', loja=loja)

# Avaliar uma loja
def avaliar_loja(id_loja):
    loja = loja_repo.buscar_por_id(id_loja)
    if loja is None:
        return redirect(url_for('listar_lojas'))

    if request.method == 'POST':
        try:
            nota = float(request.form.get('nota', ''))
        except ValueError:
            nota = None

        if nota is None or not 1 <= nota <= 5:
            return render_template('avaliar.html', loja=loja, erro = "Escolha uma nota de 1 a 5 estrelas")
        
        usuario = usuario_repo.buscar_por_id(session['usuario_id'])
        avaliacao = Avaliacoes(usuario.nome_usuario, nota)
        avaliacoes_repo.salvar_avaliacao_loja(id_loja, avaliacao)
        flash('Avaliação enviada. Obrigado!')
        return redirect(url_for('listar_avaliacoes', id_loja=id_loja))

    return render_template('avaliar.html', loja=loja)

# Lista as avaliações de uma loja
def listar_avaliacoes(id_loja):
    loja = loja_repo.listar_completo(id_loja)
    if loja is None:
        return redirect(url_for('listar_lojas'))

    return render_template('avaliacoes.html', loja=loja)

# Excluir loja
def excluir_loja(id_loja):
    if loja_repo.buscar_por_id(id_loja) is not None:
        loja_repo.excluir_loja(id_loja)
        flash('Loja removida')
    return redirect(url_for('admin_lojas'))