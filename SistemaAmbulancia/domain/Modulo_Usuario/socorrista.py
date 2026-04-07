from .usuario import Usuario
from .tipoUsuario import TipoUsuario

class Socorrista(Usuario):

    def __init__(self, id: int, nome: str, email: str, senhaHash: str, tipoUsuario: TipoUsuario):
        super().__init__(id, nome, email, senhaHash, tipoUsuario)

    def aceitarChamada():
        pass

    def atualizarStatusAtendimento():
        pass