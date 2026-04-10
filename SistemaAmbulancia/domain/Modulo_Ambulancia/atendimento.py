from ..Modulo_Chamada.chamada import Chamada
from datetime import datetime

class Atendimento:

    def __init__(self, id: int, chamada: Chamada, qtdAmbulancias: int, ambulancias: list, hora_inicio: datetime = datetime.now()):

        self.id = id
        self.hora_inicio = hora_inicio
        self.hora_finalizacao = None
        self.chamada = chamada
        self.qtd_ambulancias = qtdAmbulancias
        self.ambulancias_alocadas = ambulancias
        self.despachos = []

    def criarDespachos():
        pass

    def finalizarAtendimento():
        pass