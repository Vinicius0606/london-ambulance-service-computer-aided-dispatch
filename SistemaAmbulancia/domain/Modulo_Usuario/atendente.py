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

        endereco = Endereco(info_chamada["cep"], info_chamada["logradouro"], info_chamada["bairro"], info_chamada["cidade"], 
                            info_chamada["estado"], info_chamada["latitude"], info_chamada["longitude"], info_chamada["complemento"], info_chamada["numero"])

        chamada = Chamada(endereco, info_chamada["descricao"], nome_solicitante=info_chamada["nome"])

        self.gerenciador_eventos.emitir_evento("Chamada_registrada", chamada)

    def confirmarTriagem():
        pass