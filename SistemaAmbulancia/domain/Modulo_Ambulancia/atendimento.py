from ..Modulo_Chamada.chamada import Chamada
from ..Modulo_Chamada.status import Status as StatusChamada
from ..Modulo_Ambulancia.ambulancia import Ambulancia
from ..Modulo_Ambulancia.despacho import Despacho
from .status import Status as StatusDespacho
from datetime import datetime
from events.gerenciador_eventos import Gerenciador_eventos

class Atendimento:

    def __init__(self, id: int, chamada: Chamada, qtdAmbulancias: int, 
                 ambulancias: list[Ambulancia], gerenciador_eventos: Gerenciador_eventos,
                 hora_inicio: datetime | None = None, veio_do_banco_de_dados: bool = False):

        self.id = id
        self.hora_inicio = hora_inicio if hora_inicio is not None else datetime.now()
        self.hora_finalizacao = None
        self.chamada = chamada
        self.qtd_ambulancias = qtdAmbulancias
        self.ambulancias_alocadas = ambulancias
        self.despachos: list[Despacho] = []
        self.veio_do_banco_de_dados = veio_do_banco_de_dados
        
        self.gerenciador_eventos = gerenciador_eventos

        self.id_despacho = 0

        self.gerenciador_eventos.emitir_evento("Atendimento_criado", self)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Ambulancia_chegou_no_hospital", self.retirar_despacho)

        if not self.veio_do_banco_de_dados: self.organizar_dados_para_banco_dados()

    def atualizar_ID(self, id: int):

        self.id = id

    def organizar_dados_para_banco_dados(self):

        dict_atendimento = {
            "tabela": "Atendimento",
            "ID_chamada": self.chamada.id,
            "qtd_ambulancias": self.qtd_ambulancias,
            "data_hora_inicio": self.hora_inicio,
            "data_hora_finalizacao": self.hora_finalizacao,
            "objeto": self
        }

        self.gerenciador_eventos.emitir_evento("Armazenar_atendimento_Banco_dados", dict_atendimento)

    def criar_despachos(self):
        
        for ambulancia in self.ambulancias_alocadas:

            despacho = Despacho(self.id_despacho, self.chamada, ambulancia, self.gerenciador_eventos, 
                                veio_do_banco_de_dados=self.veio_do_banco_de_dados, id_atendimento=self.id)

            self.despachos.append(despacho)


    def retirar_despacho(self, despacho: Despacho):
        if self.hora_finalizacao is not None or despacho not in self.despachos:
            return

        despacho.finalizar_despacho()
        if len(self.despachos) == 1:
            self.finalizar_atendimento()
        else:
            self.despachos.remove(despacho)

    def finalizar_atendimento(self):
        if self.hora_finalizacao is not None or not self.despachos:
            return
        if any(despacho.status != StatusDespacho.FINALIZADO.value for despacho in self.despachos):
            return

        hora_finalizacao = datetime.now()
        dados_atendimento = {
            "tabela": "Atendimento",
            "ID": self.id,
            "data_hora_finalizacao": hora_finalizacao,
        }
        self.gerenciador_eventos.emitir_evento("Atualizar_atendimento_Banco_dados", dados_atendimento)
        self.chamada.atualizar_dados(prioridade=None, status=StatusChamada.FINALIZADO.value)

        self.hora_finalizacao = hora_finalizacao
        self.despachos.clear()
        self.gerenciador_eventos.remover_ouvinte_para_evento(
            "Ambulancia_chegou_no_hospital", self.retirar_despacho,
        )
        self.gerenciador_eventos.emitir_evento("Atendimento_finalizado", self)