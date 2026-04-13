from .equipe import Equipe
from events.gerenciador_eventos import Gerenciador_eventos

class Ambulancia:

    def __init__(self, id: int, placa:str, latitudeAtual: float, longitudeAtual: float,
                 gerenciador_eventos: Gerenciador_eventos, status: str = "Disponivel"):
        self.id = id
        self.placa = placa
        self.latitudeAtual = latitudeAtual
        self.longitudeAtual = longitudeAtual
        self.equipe: Equipe = None
        self.status: str = status

        self.gerenciador_eventos = gerenciador_eventos

        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Despacho_criado", self.despacho_criado)

        self.gerenciador_eventos.emitir_evento("Ambulancia_criada", self)

    def despacho_criado(self, despacho):

        if despacho.ambulancia.id == self.id:

            self.atualizar_status("Atendendo");

    def atualizar_status(self, status):
        
        self.status = status

        self.gerenciador_eventos.emitir_evento("Ambulancia_mudou_status", self)

    def atualizar_localizacao(self, latitudeAtual, longitudeAtual):
        
        self.latitudeAtual = latitudeAtual
        self.longitudeAtual = longitudeAtual

        self.gerenciador_eventos.emitir_evento("Ambulancia_movimentada", self)