from .interface_escolha_ambulancia import Interface_escolha_ambulancia
from domain.Modulo_Ambulancia.ambulancia import Ambulancia
import requests

class Escolher_ambulancia_OSMR(Interface_escolha_ambulancia):

    def escolher_ambulancias(self, ambulancias: list[Ambulancia], qtd_vitimas: int, 
                             latitude_chamado: float, longitude_chamado: float):
        
        menor_distancia_pro_chamado: float = 30

        escolha_de_ambulancia = []
        ambulancias_para_remover = []

        if qtd_vitimas < 4 :
            qtd_ambulancias = qtd_vitimas

        elif qtd_vitimas >= 4:
            qtd_ambulancias = 4

        aux_qtd_ambulancias = qtd_ambulancias

        while aux_qtd_ambulancias > 0:

            for ambulancia in self.ambulancias:

                distancia = self.buscar_ambulancias_proximas([ambulancia.latitudeAtual, ambulancia.longitudeAtual])

                if distancia["distancia_km"] < menor_distancia_pro_chamado and ambulancia not in escolha_de_ambulancia: 
                    menor_distancia_pro_chamado = distancia["distancia_km"]
                    ambulancias_para_remover.append(ambulancia)

            escolha_de_ambulancia.append(ambulancias_para_remover[-1])
            
            aux_qtd_ambulancias -= 1
  
        return{
            "ambulancias": escolha_de_ambulancia,
            "qtd_ambulancias": qtd_ambulancias
        }
    
    def buscar_ambulancias_proximas(self, posicao_ambulancia, latitude_chamado, longitude_chamado):
        
        
        url = (
            f"https://router.project-osrm.org/route/v1/driving/"
            f"{posicao_ambulancia[1]},{posicao_ambulancia[0]};{latitude_chamado},{longitude_chamado}"
            f"?overview=full&geometries=geojson"
        )

        resposta = requests.get(url)
        resposta.raise_for_status()

        dados = resposta.json()

        if not dados.get("routes"):
            return None

        rota = dados["routes"][0]

        return {
            "distancia_metros": rota["distance"],
            "distancia_km": rota["distance"] / 1000,
        }