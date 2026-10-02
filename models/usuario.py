class Usuario:
    def __init__(self, nome_usuario, email, senha_hash, is_admin=False):
        self.id = None
        self.nome_usuario = nome_usuario
        self.email = email
        self._senha_hash = senha_hash
        self._is_admin = is_admin