import usuario
import tipoUsuario

class Atendente(usuario):

    def __init__(self, id: int, nome: str, email: str, senhaHash: str, tipoUsuario: tipoUsuario):
        super().__init__(id, nome, email, senhaHash, tipoUsuario)

    def registrarChamada():
        pass

    def confirmarTriagem():
        pass