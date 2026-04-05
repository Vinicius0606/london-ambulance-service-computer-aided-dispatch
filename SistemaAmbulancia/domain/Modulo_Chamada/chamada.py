from datetime import datetime
from endereco import Endereco
from status import Status
from prioridade import Prioridade

class Chamada:

    def __init__(self, id: int, nomeSolicitante: str, endereco: Endereco, descricao: str):
        self.id = id
        self.nomeSolicitante = nomeSolicitante
        self.endereco = endereco
        self.descricao = descricao
        self.horaChamada = datetime.now()
        self.prioridade = None
        self.status = Status.PENDENTE

    def atualizarDados(prioridade: Prioridade | None, status: Status | None):
        pass