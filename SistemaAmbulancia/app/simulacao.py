from events.gerenciador_eventos import Gerenciador_eventos
from domain.Modulo_Ambulancia.despacho import Despacho
from domain.Modulo_Ambulancia.status import Status
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

    def retomar_despacho(self, despacho: Despacho):
        if despacho.status in (Status.EMTRANSITO.value, Status.RETORNANDO.value):
            despacho.ambulancia.atualizar_status("Atendendo")
            self.__calcular_movimento_ambulancia(despacho)

    def __mapa_carregado(self):
        self.mapa_carregado += 1
        if self.mapa_carregado != 3:
            return

        for movimento in self.temporizadores_funcao:
            if movimento is not None:
                movimento["timer"].start(100)

    def __calcular_movimento_ambulancia(self, despacho: Despacho):
        if despacho.status == Status.EMTRANSITO.value:
            destino = (despacho.chamada.endereco.longitude, despacho.chamada.endereco.latitude)
        elif despacho.status == Status.RETORNANDO.value:
            destino = (-47.911496, -15.834400)
        else:
            return

        if any(
            movimento is not None and movimento["despacho"] is despacho
            for movimento in self.temporizadores_funcao
        ):
            return

        ambulancia = despacho.ambulancia
        url = (
            "https://router.project-osrm.org/route/v1/driving/"
            f"{ambulancia.longitudeAtual},{ambulancia.latitudeAtual};{destino[0]},{destino[1]}"
            "?overview=full&geometries=geojson"
        )
        try:
            resposta = requests.get(url, timeout=5)
            resposta.raise_for_status()
            dados = resposta.json()
        except (requests.exceptions.RequestException, ValueError):
            return

        if not isinstance(dados, dict) or dados.get("code") != "Ok":
            return
        try:
            pontos_da_rota = dados["routes"][0]["geometry"]["coordinates"]
        except (KeyError, IndexError, TypeError):
            return
        if not isinstance(pontos_da_rota, list) or not pontos_da_rota:
            return
        if any(
            not isinstance(ponto, list) or len(ponto) < 2
            or not all(isinstance(coordenada, (int, float)) for coordenada in ponto[:2])
            for ponto in pontos_da_rota
        ):
            return

        timer = QTimer()
        movimento = {"timer": timer, "index": 0, "despacho": despacho}
        indice = next(
            (i for i, item in enumerate(self.temporizadores_funcao) if item is None),
            len(self.temporizadores_funcao),
        )
        if indice == len(self.temporizadores_funcao):
            self.temporizadores_funcao.append(movimento)
        else:
            self.temporizadores_funcao[indice] = movimento

        timer.timeout.connect(
            lambda: self.__movimentar_ambulancia(pontos_da_rota, indice, movimento)
        )
        if self.mapa_carregado == 3:
            timer.start(100)

    def __movimentar_ambulancia(self, pontos_da_rota: list, indice: int, movimento: dict):
        if self.temporizadores_funcao[indice] is not movimento:
            return

        despacho = movimento["despacho"]
        longitude, latitude = pontos_da_rota[movimento["index"]][:2]
        despacho.ambulancia.atualizar_localizacao(latitude, longitude)
        movimento["index"] += 1
        if movimento["index"] < len(pontos_da_rota):
            return

        movimento["timer"].stop()
        self.temporizadores_funcao[indice] = None
        movimento["timer"].deleteLater()

        if despacho.status == Status.EMTRANSITO.value:
            despacho.atualizar_hora_chegada_local()
            self.gerenciador_eventos.emitir_evento("Ambulancia_retornar_hospital", despacho)
        elif despacho.status == Status.RETORNANDO.value:
            self.gerenciador_eventos.emitir_evento("Ambulancia_chegou_no_hospital", despacho)