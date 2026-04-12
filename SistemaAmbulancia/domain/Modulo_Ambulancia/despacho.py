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
        self.status = Status.EMTRANSITO

        self.gerenciador_eventos = gerenciador_eventos

        gerenciador_eventos.emitir_evento("Despacho_criado", self)

    def atualizarHoraChegadaLocalEstimada():
        pass

    def atualizarHoraChegadaLocal():
        pass

    def atualizarStatus():
        pass
