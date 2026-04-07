from .usuario import Usuario
from .tipoUsuario import TipoUsuario

class Atendente(Usuario):

    def __init__(self, id: int, nome: str, email: str, senhaHash: str, tipoUsuario: TipoUsuario):
        super().__init__(id, nome, email, senhaHash, tipoUsuario)

    def registrarChamada():
        pass

    def confirmarTriagem():
        pass