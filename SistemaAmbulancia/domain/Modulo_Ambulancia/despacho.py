from .ambulancia import Ambulancia
from .status import Status
from domain.Modulo_Chamada.chamada import Chamada
from datetime import datetime
from events.gerenciador_eventos import Gerenciador_eventos

class Despacho:

    def __init__(self, id: int, chamada: Chamada, ambulancia: Ambulancia,
                  gerenciador_eventos: Gerenciador_eventos, observacoes: str = None):

        self.id = id
        self.chamada: Chamada = chamada
        self.ambulancia = ambulancia
        self.observacoes = observacoes
        self.horaInicio = datetime.now()
        self.horaChegadaLocalEstimada = None
        self.horaChegadaLocal = None
        self.status = Status.EMTRANSITO.value

        self.gerenciador_eventos = gerenciador_eventos

        gerenciador_eventos.emitir_evento("Despacho_criado", self)

    def atualizar_hora_chegada_local(self):
        
        self.horaChegadaLocal = datetime.now()

        self.status = Status.RETORNANDO.value

    def finalizar_despacho(self):
        
        self.status = Status.FINALIZADO.value

        self.ambulancia.atualizar_status("Disponivel")
