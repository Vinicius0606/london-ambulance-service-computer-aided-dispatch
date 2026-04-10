from datetime import datetime
from .endereco import Endereco
from .status import Status
from .prioridade import Prioridade
from events.gerenciador_eventos import Gerenciador_eventos

class Chamada:

    def __init__(self, nome_solicitante: str, endereco: Endereco, 
                 descricao: str, data_hora: datetime = datetime.now()):
        self.id = None
        self.nome_solicitante = nome_solicitante
        self.endereco = endereco
        self.descricao = descricao
        self.horaChamada = data_hora
        self.prioridade = None
        self.status = Status.PENDENTE

    def atualizarID(self, id: int):

        self.id = id

    def atualizarDados(prioridade: Prioridade | None, status: Status | None):
        pass