from database.db import conectar
from models.usuario import Usuario

def tabela_usuario():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome_usuario VARCHAR(100) NOT NULL,
            email VARCHAR(150) NOT NULL UNIQUE,
            senha_hash VARCHAR(255) NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT FALSE
        )
    """)
    conexao.commit()
    conexao.close()

def salvar_usuario(usuario):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO usuarios (nome_usuario, email, senha_hash, is_admin)
        VALUES (%s, %s, %s, %s)
    """, (usuario.nome, usuario.email, usuario._senha_hash, False))
    conexao.commit()
    id_gerado = cursor.lastrowid
    conexao.close()

    usuario.id = id_gerado
    return id_gerado

def buscar_por_email(email):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, nome_usuario, email, senha_hash, is_admin FROM usuarios WHERE email = %s",
        (email,)
    )
    linha = cursor.fetchone()
    conexao.close()

    if linha is None:
        return None

    id_usuario, nome, email, senha_hash, is_admin = linha
    usuario = Usuario(nome, email, senha_hash, isadmin=bool(is_admin))
    usuario.id = id_usuario
    return usuario

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