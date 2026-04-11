from datetime import datetime
from .endereco import Endereco
from .status import Status
from .prioridade import Prioridade
from events.gerenciador_eventos import Gerenciador_eventos

class Chamada:

    def __init__(self, endereco: Endereco, 
                 descricao: str, data_hora: datetime = datetime.now(), id: int = None, 
                 prioridade: Prioridade = None, nome_solicitante: str = None):
        self.id = id
        self.nome_solicitante = nome_solicitante
        self.endereco = endereco
        self.descricao = descricao
        self.horaChamada = data_hora
        self.prioridade = prioridade
        self.status = Status.PENDENTE

    def atualizarID(self, id: int):

        self.id = id

    def atualizarDados(prioridade: Prioridade | None, status: Status | None):
        pass