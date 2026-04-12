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
        self.despachos = []
        
        self.gerenciador_eventos = gerenciador_eventos

        self.id_despacho = -1

    def criarDespachos(self):
        
        for ambulancia in self.ambulancias_alocadas:

            despacho = Despacho(self.id_despacho, self.chamada, ambulancia, self.gerenciador_eventos)

            self.despachos.append(despacho)


    def finalizarAtendimento():
        pass