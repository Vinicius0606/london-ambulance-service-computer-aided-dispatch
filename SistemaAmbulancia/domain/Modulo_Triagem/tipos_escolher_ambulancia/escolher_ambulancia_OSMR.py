from .interface_escolha_ambulancia import Interface_escolha_ambulancia
from domain.Modulo_Ambulancia.ambulancia import Ambulancia
from domain.Modulo_Chamada.endereco import normalizar_coordenadas
import requests

class Escolher_ambulancia_OSMR(Interface_escolha_ambulancia):

    def escolher_ambulancias(self, ambulancias: list[Ambulancia], qtd_vitimas: int,
                             latitude_chamado: float, longitude_chamado: float):
        coordenadas_chamada = normalizar_coordenadas(latitude_chamado, longitude_chamado)
        if qtd_vitimas <= 0 or coordenadas_chamada is None:
            return {"ambulancias": [], "qtd_ambulancias": 0}

        limite = min(qtd_vitimas, 4)
        candidatas = []
        ids_consultados = set()

        for ambulancia in ambulancias:
            if ambulancia.status != "Disponivel" or ambulancia.id in ids_consultados:
                continue

            coordenadas = normalizar_coordenadas(ambulancia.latitudeAtual, ambulancia.longitudeAtual)
            if coordenadas is None:
                continue

            ids_consultados.add(ambulancia.id)
            rota = self.buscar_ambulancias_proximas(coordenadas, *coordenadas_chamada)

            if rota is not None and rota["distancia_km"] < 30:
                candidatas.append((rota["distancia_km"], ambulancia))

        candidatas.sort(key=lambda candidata: candidata[0])
        escolhidas = [ambulancia for _, ambulancia in candidatas[:limite]]

        return {
            "ambulancias": escolhidas,
            "qtd_ambulancias": len(escolhidas),
        }

    def buscar_ambulancias_proximas(self, posicao_ambulancia, latitude_chamado, longitude_chamado):
        url = (
            f"https://router.project-osrm.org/route/v1/driving/"
            f"{posicao_ambulancia[1]},{posicao_ambulancia[0]};{longitude_chamado},{latitude_chamado}"
            f"?overview=full&geometries=geojson"
        )

        try:
            resposta = requests.get(url, timeout=5)
            resposta.raise_for_status()
            dados = resposta.json()
        except (requests.exceptions.RequestException, ValueError):
            return None

        rotas = dados.get("routes") if isinstance(dados, dict) else None
        if not isinstance(rotas, list) or not rotas or not isinstance(rotas[0], dict):
            return None

        distancia = rotas[0].get("distance")
        if type(distancia) not in (int, float) or not 0 <= distancia < float("inf"):
            return None

        return {
            "distancia_metros": distancia,
            "distancia_km": distancia / 1000,
        }