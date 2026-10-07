import sys
from database.db import conectar

def tornar_admin(email):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE usuarios SET is_admin = TRUE WHERE email = %s
    """, (email,))
    conexao.commit()
    linha_afetada = cursor.rowcount
    conexao.close()
    return linha_afetada

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python tornar_admin.py email@email.com")
        sys.exit(1)

    email_informado = sys.argv[1]
    linha_afetada = tornar_admin(email_informado)

    if linha_afetada:
        print(f'"{email_informado}" agora é administrador(a)')
    else:
        print(f'Nenhum usuário encontrado com o email "{email_informado}"')