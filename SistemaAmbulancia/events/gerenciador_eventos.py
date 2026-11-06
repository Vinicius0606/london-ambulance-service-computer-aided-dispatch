from typing import Callable

class Gerenciador_eventos:

    def __init__(self):

        self.ouvintes = dict()

    def adicionar_ouvinte_para_evento(self, nome_evento: str, funcao: Callable):

        if nome_evento not in self.ouvintes:

            self.ouvintes[nome_evento] = []

        self.ouvintes[nome_evento].append(funcao)

    def remover_ouvinte_para_evento(self, nome_evento: str, funcao: Callable):
        ouvintes = self.ouvintes.get(nome_evento)
        if ouvintes and funcao in ouvintes:
            ouvintes.remove(funcao)
            if not ouvintes:
                del self.ouvintes[nome_evento]

    def emitir_evento(self, nome_evento: str, dados=None):
        for funcao in tuple(self.ouvintes.get(nome_evento, ())):
            if dados:
                funcao(dados)
            else:
                funcao()