from domain.Modulo_Ambulancia.ambulancia import Ambulancia
from domain.Modulo_Ambulancia.status import Status
from domain.Modulo_Chamada.chamada import Chamada
from datetime import datetime
from events.gerenciador_eventos import Gerenciador_eventos

class Despacho:

    def __init__(self, id: int, chamada: Chamada, ambulancia: Ambulancia,
                  gerenciador_eventos: Gerenciador_eventos, observacoes: str = None,
                  veio_do_banco_de_dados: bool = False, id_atendimento: int = -1):

        self.id = id
        self.chamada: Chamada = chamada
        self.ambulancia = ambulancia
        self.observacoes = observacoes
        self.hora_inicio = datetime.now()
        self.hora_chegada_local_estimada = None
        self.hora_chegada_local = None
        self.status = Status.EMTRANSITO.value
        self.veio_do_banco_de_dados = veio_do_banco_de_dados

        self.id_atendimento = id_atendimento

        self.gerenciador_eventos = gerenciador_eventos

        self.gerenciador_eventos.emitir_evento("Despacho_criado", self)

        if not self.veio_do_banco_de_dados: self.organizar_dados_para_banco_dados()

    def atualizar_ID(self, id: int):

        self.id = id

    def organizar_dados_para_banco_dados(self):
    
        dict_despacho = {
            "tabela": "Atendimento_Ambulancia",
            "ID_atendimento": self.id_atendimento,
            "ID_ambulancia": self.ambulancia.id,
            "data_hora_envio": self.hora_inicio,
            "data_hora_chegada": self.hora_chegada_local_estimada,
            "status": self.status,
            "observacoes": self.chamada.descricao,
            "objeto": self
        }

        self.gerenciador_eventos.emitir_evento("Armazenar_despacho_Banco_dados", dict_despacho)

    def atualizar_hora_chegada_local(self):
        
        self.hora_chegada_local = datetime.now()

        self.status = Status.RETORNANDO.value

        dict_despacho_atualizar_dados = {
            "tabela": "Atendimento_Ambulancia",
            "ID": self.id,
            "status": self.status,
            "data_hora_chegada": self.hora_chegada_local
        }

        self.gerenciador_eventos.emitir_evento("Atualizar_despacho_Banco_dados", dict_despacho_atualizar_dados)

    def finalizar_despacho(self):
        
        self.status = Status.FINALIZADO.value

        self.ambulancia.atualizar_status("Disponivel")

        dict_despacho_atualizar_dados = {
            "tabela": "Atendimento_Ambulancia",
            "ID": self.id,
            "status": self.status,
        }

        self.gerenciador_eventos.emitir_evento("Atualizar_despacho_Banco_dados", dict_despacho_atualizar_dados)
