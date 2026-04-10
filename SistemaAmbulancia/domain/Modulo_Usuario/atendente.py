from .usuario import Usuario
from .tipoUsuario import TipoUsuario
from events.gerenciador_eventos import Gerenciador_eventos
from domain.Modulo_Chamada.chamada import Chamada
from domain.Modulo_Chamada.endereco import Endereco
from datetime import datetime

class Atendente(Usuario):

    def __init__(self, id: int, nome: str, email: str, senhaHash: str, 
                 tipoUsuario: TipoUsuario, gerenciador_eventos: Gerenciador_eventos):
        
        super().__init__(id, nome, email, senhaHash, tipoUsuario)

        self.gerenciador_eventos = gerenciador_eventos

        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Chamada_enviada", self.registrarChamada)

    def registrarChamada(self, info_chamada: list):

        endereco = Endereco(info_chamada[0], info_chamada[1], info_chamada[2], info_chamada[3], 
                            info_chamada[4], info_chamada[5], info_chamada[6], info_chamada[7], info_chamada[8])

        chamada = Chamada(info_chamada[9], endereco, info_chamada[10])

        self.gerenciador_eventos.emitir_evento("Chamada_registrada", chamada)

    def confirmarTriagem():
        pass