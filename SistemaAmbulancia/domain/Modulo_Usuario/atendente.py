from .usuario import Usuario
from .tipoUsuario import TipoUsuario
from events.gerenciador_eventos import Gerenciador_eventos
from domain.Modulo_Chamada.chamada import Chamada
from domain.Modulo_Chamada.endereco import Endereco, normalizar_coordenadas
from datetime import datetime

class Atendente(Usuario):

    def __init__(self, id: int, nome: str, email: str, senhaHash: str, 
                 tipoUsuario: TipoUsuario, gerenciador_eventos: Gerenciador_eventos):
        
        super().__init__(id, nome, email, senhaHash, tipoUsuario)

        self.gerenciador_eventos = gerenciador_eventos

        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Chamada_enviada", self.registrarChamada)

        self.chamada_id_registrada = -1

    def registrarChamada(self, info_chamada: dict):

        coordenadas = normalizar_coordenadas(info_chamada.get("latitude"), info_chamada.get("longitude"))
        if coordenadas is None:
            raise ValueError("Informe coordenadas válidas para registrar a chamada.")

        latitude, longitude = coordenadas
        endereco = Endereco(
            info_chamada["cep"], info_chamada["logradouro"], info_chamada["bairro"],
            info_chamada["cidade"], info_chamada["estado"], latitude, longitude,
            info_chamada["complemento"], info_chamada["numero"],
        )

        chamada = Chamada(endereco, info_chamada["descricao"], self.gerenciador_eventos , id=self.chamada_id_registrada, 
                    nome_solicitante=info_chamada["nome"])

        self.chamada_id_registrada -= 1

        self.gerenciador_eventos.emitir_evento("Chamada_registrada", chamada)