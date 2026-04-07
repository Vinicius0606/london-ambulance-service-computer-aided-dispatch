from .usuario import Usuario
from .tipoUsuario import TipoUsuario

class Administrador(Usuario):

    def __init__(self, id: int, nome: str, email: str, senhaHash: str, tipoUsuario: TipoUsuario):
        super().__init__(id, nome, email, senhaHash, tipoUsuario)

    def cadastrarUsuario():
        pass

    def removerUsuario():
        pass