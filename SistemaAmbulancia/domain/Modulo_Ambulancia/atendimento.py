from ..Modulo_Chamada.chamada import Chamada
from ..Modulo_Ambulancia.ambulancia import Ambulancia
from ..Modulo_Ambulancia.despacho import Despacho
from datetime import datetime
from events.gerenciador_eventos import Gerenciador_eventos

class Atendimento:

    def __init__(self, id: int, chamada: Chamada, qtdAmbulancias: int, 
                 ambulancias: list[Ambulancia], gerenciador_eventos: Gerenciador_eventos,
                 hora_inicio: datetime = datetime.now()):

        self.id = id
        self.hora_inicio = hora_inicio
        self.hora_finalizacao = None
        self.chamada = chamada
        self.qtd_ambulancias = qtdAmbulancias
        self.ambulancias_alocadas = ambulancias
        self.despachos: list[Despacho] = []
        
        self.gerenciador_eventos = gerenciador_eventos

        self.id_despacho = 0

        self.gerenciador_eventos.emitir_evento("Atendimento_criado", self)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Ambulancia_chegou_no_hospital", self.retirar_despacho)

    def criarDespachos(self):
        
        for ambulancia in self.ambulancias_alocadas:

            despacho = Despacho(self.id_despacho, self.chamada, ambulancia, self.gerenciador_eventos)

            self.despachos.append(despacho)


    def retirar_despacho(self, despacho: Despacho):

        if despacho.chamada.id != self.chamada.id: return

        for index, despacho_lista_item in enumerate(self.despachos):

            if despacho_lista_item.ambulancia.id == despacho.ambulancia.id:

                self.despachos.pop(index)

                despacho.ambulancia.atualizar_status("Disponivel")

                break
        
        if len(self.despachos) == 0:

            self.finalizarAtendimento()


    def finalizarAtendimento(self):
        
        self.chamada.atualizar_dados(prioridade=None, status="Encerrado")

        self.hora_finalizacao = datetime.now()

        self.gerenciador_eventos.emitir_evento("Atendimento_finalizado", self)