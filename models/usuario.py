class Usuario:
    def __init__(self, nome_usuario, email, senha_hash):
        self.id = None
        self.nome_usuario = nome_usuario
        self.email = email
        self._senha_hash = senha_hash