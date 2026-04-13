from datetime import datetime
from .endereco import Endereco
from .status import Status
from .prioridade import Prioridade
from events.gerenciador_eventos import Gerenciador_eventos

class Chamada:

    def __init__(self, endereco: Endereco, descricao: str, 
                 gerenciador_eventos: Gerenciador_eventos, data_hora: datetime = datetime.now(), id: int = None, 
                 prioridade: Prioridade = None, nome_solicitante: str = None, status: str = Status.PENDENTE.value,
                 veio_do_banco_de_dados: bool = False):
        
        self.id = id
        self.nome_solicitante = nome_solicitante
        self.endereco = endereco
        self.descricao = descricao
        self.hora_chamada = data_hora
        self.prioridade: str = prioridade
        self.status: str = status
        self.veio_do_banco_de_dados = veio_do_banco_de_dados

        self.gerenciador_eventos = gerenciador_eventos

        if veio_do_banco_de_dados: self.gerenciador_eventos.emitir_evento("Chamada_criada", self)

        if not veio_do_banco_de_dados: self.organizar_dados_para_banco_dados()

    def organizar_dados_para_banco_dados(self):

        dict_endereco = {
            "tabela": "Endereco",
            "CEP": self.endereco.CEP,
            "logradouro": self.endereco.logradouro,
            "numero": self.endereco.numero if self.endereco.numero != None else "Não Informado",
            "bairro": self.endereco.bairro if self.endereco.bairro != None else "Não Informado",
            "cidade": self.endereco.cidade,
            "estado": self.endereco.estado,
            "complemento": self.endereco.complemento if self.endereco.complemento != None else "Não Informado",
            "latitude": self.endereco.latitude,
            "longitude": self.endereco.longitude,
            "objeto": self.endereco
        }

        self.gerenciador_eventos.emitir_evento("Armazenar_endereco_Banco_dados", dict_endereco)

        dict_chamada = {
            "tabela": "Chamada",
            "ID_endereco": self.endereco.id,
            "nome_solicitante": self.nome_solicitante if self.nome_solicitante != None else "Não Informado",
            "hora_chamada": self.hora_chamada,
            "descricao": self.descricao,
            "prioridade": -1,
            "status": self.status,
            "objeto": self
        }

        self.gerenciador_eventos.emitir_evento("Armazenar_chamada_Banco_dados", dict_chamada)
        
        self.gerenciador_eventos.emitir_evento("Chamada_criada", self)

    def atualizar_ID(self, id: int):

        self.id = id

    def atualizar_dados(self, prioridade: Prioridade | None, status: Status | None):

        dict_chamada_atualizar_dados = {
            "tabela": "Chamada",
            "ID": self.id
        }

        if prioridade:
            
            self.prioridade = prioridade

            prioridade_int = 0

            if self.prioridade == "Transporte": prioridade_int = 1
            elif self.prioridade == "Moderada": prioridade_int = 2
            elif self.prioridade == "Alta": prioridade_int = 3
            else: prioridade_int = 4

            dict_chamada_atualizar_dados["prioridade"] = prioridade_int

        if status: 
            
            self.status = status

            dict_chamada_atualizar_dados["status"] = status

        self.gerenciador_eventos.emitir_evento("Atualizar_chamada_Banco_dados", dict_chamada_atualizar_dados)

