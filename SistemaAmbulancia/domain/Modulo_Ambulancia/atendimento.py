from Modulo_Chamada.chamada import Chamada
from datetime import datetime

class Atendimento:

    def __init__(self, id: int, chamada: Chamada, qtdAmbulancias: int, ambulancias: list):

        self.id = id
        self.horaInicio = datetime.now()
        self.horaFinalizacao = None
        self.chamada = chamada
        self.qtdAmbulancias = qtdAmbulancias
        self.ambulanciasAlocadas = ambulancias
        self.despachos = []

    def criarDespachos():
        pass

    def finalizarAtendimento():
        pass