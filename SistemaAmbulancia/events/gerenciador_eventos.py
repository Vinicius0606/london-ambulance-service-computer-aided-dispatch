from typing import Callable

class Gerenciador_eventos:

    def __init__(self):

        self.ouvintes = dict()

    def adicionar_ouvinte_para_evento(self, nome_evento: str, funcao: Callable):

        if nome_evento not in self.ouvintes:

            self.ouvintes[nome_evento] = []

        self.ouvintes[nome_evento].append(funcao)

    def emitir_evento(self, nome_evento: str, dados= None):

        if nome_evento in self.ouvintes:

            for funcao in self.ouvintes[nome_evento]:
                
                if(dados): funcao(dados)
                else: funcao()