from events.gerenciador_eventos import Gerenciador_eventos
from domain.Modulo_Ambulancia.despacho import Despacho
from PySide6.QtCore import QTimer
import requests

class Simulacao:

    def __init__(self, gerenciador_eventos: Gerenciador_eventos):

        self.gerenciador_eventos = gerenciador_eventos

        self.temporizadores_funcao = []

        self.mapa_carregado = 0

        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Despacho_criado", self.__calcular_movimento_ambulancia)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Mapa_carregado", self.__mapa_carregado)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Ambulancia_retornar_hospital", self.__calcular_movimento_ambulancia)

    def __mapa_carregado(self):

        
        self.mapa_carregado += 1

        if self.mapa_carregado != 3: return

        for temporizador_funcao in self.temporizadores_funcao:

            temporizador_funcao["timer"].start(100)

    def __calcular_movimento_ambulancia(self, despacho: Despacho):

        if despacho.status == "EmTransito":
            
            url = (
                f"https://router.project-osrm.org/route/v1/driving/"
                f"{despacho.ambulancia.longitudeAtual},{despacho.ambulancia.latitudeAtual};{despacho.chamada.endereco.longitude},{despacho.chamada.endereco.latitude}"
                f"?overview=full&geometries=geojson"
            )

        else: 

            url = (
                f"https://router.project-osrm.org/route/v1/driving/"
                f"{despacho.ambulancia.longitudeAtual},{despacho.ambulancia.latitudeAtual};{-47.911496},{-15.834400}"
                f"?overview=full&geometries=geojson"
            )

        resposta = requests.get(url)

        resposta.raise_for_status()

        dados = resposta.json()

        if dados.get("code") == "Ok":

            pontos_da_roda = dados["routes"][0]["geometry"]["coordinates"]

            timer = QTimer()
            
            index_temporizador_funcao = -1

            for index, temporizador_funcao in enumerate(self.temporizadores_funcao):

                if temporizador_funcao == None:
                     index_temporizador_funcao = index

            if index_temporizador_funcao != -1:

                self.temporizadores_funcao[index_temporizador_funcao] = {"timer": timer, "index": 0}

            else:

                self.temporizadores_funcao.append({"timer": timer, "index": 0})

                index_temporizador_funcao = (len(self.temporizadores_funcao) - 1)


            timer.timeout.connect(lambda: self.__movimentar_ambulancia(despacho, pontos_da_roda, 
                                                                       index_temporizador_funcao))
            
            if self.mapa_carregado == 3: timer.start(100)

    def __movimentar_ambulancia(self, despacho: Despacho, pontos_da_rota: list, index_temporizadores_funcao: int):

        pontos_da_rota_index = self.temporizadores_funcao[index_temporizadores_funcao]["index"]

        despacho.ambulancia.atualizarLocalizacao(
            pontos_da_rota[pontos_da_rota_index][1], pontos_da_rota[pontos_da_rota_index][0])
        
        pontos_da_rota_index += 1

        self.temporizadores_funcao[index_temporizadores_funcao]["index"] = pontos_da_rota_index

        if pontos_da_rota_index >= len(pontos_da_rota):

            self.temporizadores_funcao[index_temporizadores_funcao]["timer"].stop()

            self.temporizadores_funcao[index_temporizadores_funcao] = None

            if despacho.status == "EmTransito":

                despacho.atualizar_hora_chegada_local()

                self.gerenciador_eventos.emitir_evento("Ambulancia_retornar_hospital", despacho)

            elif despacho.status == "Retornando":

                self.gerenciador_eventos.emitir_evento("Ambulancia_chegou_no_hospital", despacho)