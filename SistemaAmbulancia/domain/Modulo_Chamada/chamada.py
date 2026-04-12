from datetime import datetime
from .endereco import Endereco
from .status import Status
from .prioridade import Prioridade
from events.gerenciador_eventos import Gerenciador_eventos

class Chamada:

    def __init__(self, endereco: Endereco, descricao: str, 
                 gerenciador_eventos: Gerenciador_eventos, data_hora: datetime = datetime.now(), id: int = None, 
                 prioridade: Prioridade = None, nome_solicitante: str = None, status: str = Status.PENDENTE.value):
        
        self.id = id
        self.nome_solicitante = nome_solicitante
        self.endereco = endereco
        self.descricao = descricao
        self.hora_chamada = data_hora
        self.prioridade: str = prioridade
        self.status: str = status

        self.gerenciador_eventos = gerenciador_eventos

        self.gerenciador_eventos.emitir_evento("Chamada_criada", self)


    def atualizar_ID(self, id: int):

        self.id = id

    def atualizar_dados(self, prioridade: Prioridade | None, status: Status | None):

        if prioridade: self.prioridade = prioridade
        if status: self.status = status