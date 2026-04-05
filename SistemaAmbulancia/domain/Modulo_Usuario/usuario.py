import tipoUsuario

class Usuario:

    def __init__(self, id: int, nome: str, email: str, senhaHash: str, tipoUsuario: tipoUsuario):
        self.id = id
        self.nome = nome
        self.email = email
        self.senhaHash = senhaHash
        self.tipoUsuario = tipoUsuario

    def autenticar():
        pass

    def alterarSenha():
        pass
    
    