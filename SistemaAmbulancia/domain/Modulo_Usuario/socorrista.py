import usuario
import tipoUsuario

class Socorrista(usuario):

    def __init__(self, id: int, nome: str, email: str, senhaHash: str, tipoUsuario: tipoUsuario):
        super().__init__(id, nome, email, senhaHash, tipoUsuario)

    def aceitarChamada():
        pass

    def atualizarStatusAtendimento():
        pass