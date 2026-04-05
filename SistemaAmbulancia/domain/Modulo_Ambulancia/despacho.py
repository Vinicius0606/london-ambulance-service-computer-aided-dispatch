from ambulancia import Ambulancia
from status import Status
from Modulo_Chamada.chamada import Chamada
from datetime import datetime

class Despacho:

    def __init__(self, id: int, chamada: Chamada, ambulancia: Ambulancia, observacoes: str):

        self.id = id
        self.chamada = Chamada
        self.ambulancia = ambulancia
        self.observacoes = observacoes
        self.horaInicio = datetime.now()
        self.horaChegadaLocalEstimada = None
        self.horaChegadaLocal = None
        self.status = Status.EMTRANSITO

    def atualizarHoraChegadaLocalEstimada():
        pass

    def atualizarHoraChegadaLocal():
        pass

    def atualizarStatus():
        pass
