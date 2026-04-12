from .equipe import Equipe
from .status import Status
from events.gerenciador_eventos import Gerenciador_eventos

class Ambulancia:

    def __init__(self, id: int, placa:str, tipo:str, gerenciador_eventos: Gerenciador_eventos, status: str = "Disponivel"):
        self.id = id
        self.placa = placa
        self.tipo = tipo
        self.latitudeAtual = None
        self.longitudeAtual = None
        self.equipe: Equipe = None
        self.status: str = status

        self.gerenciador_eventos = gerenciador_eventos

        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Despacho_criado", lambda _: self.atualizar_status("Atendendo"))

    def atualizar_status(self, status):
        
        self.status = status

        self.gerenciador_eventos.emitir_evento("Ambulancia_mudou_status", self)

    def atualizarLocalizacao(self, latitudeAtual, longitudeAtual):
        
        self.latitudeAtual = latitudeAtual
        self.longitudeAtual = longitudeAtual

        self.gerenciador_eventos.emitir_evento("Ambulancia_criada", self)