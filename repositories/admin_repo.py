from database.db import conectar
from models.usuario import Usuario

def buscar_por_id(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, nome_usuario, email, senha_hash, is_admin FROM usuarios WHERE id = %s",
        (id_usuario,)
    )
    linha = cursor.fetchone()
    conexao.close()

    if linha is None:
        return None

    id_usuario, nome_usuario, email, senha_hash, is_admin = linha
    usuario = Usuario(nome_usuario, email, senha_hash, is_admin=bool(is_admin))
    usuario.id = id_usuario
    return usuario