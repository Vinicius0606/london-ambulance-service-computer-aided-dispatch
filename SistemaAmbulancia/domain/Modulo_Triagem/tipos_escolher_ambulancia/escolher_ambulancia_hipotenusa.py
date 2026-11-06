from .interface_escolha_ambulancia import Interface_escolha_ambulancia
from domain.Modulo_Ambulancia.ambulancia import Ambulancia
from domain.Modulo_Chamada.endereco import normalizar_coordenadas
import math

class Escolher_ambulancia_hipotenusa(Interface_escolha_ambulancia):

    def escolher_ambulancias(self, ambulancias: list[Ambulancia], qtd_vitimas: int, 
                             latitude_chamado: float, longitude_chamado: float):
        

        coordenadas_chamada = normalizar_coordenadas(latitude_chamado, longitude_chamado)
        if coordenadas_chamada is None:
            return {"ambulancias": [], "qtd_ambulancias": 0}
        latitude_chamado, longitude_chamado = coordenadas_chamada

        hipotenusas = []
        ids_consultados = set()

        for ambulancia in ambulancias:

            if ambulancia.status != "Disponivel" or ambulancia.id in ids_consultados:
                continue
            coordenadas = normalizar_coordenadas(ambulancia.latitudeAtual, ambulancia.longitudeAtual)
            if coordenadas is None:
                continue

            ids_consultados.add(ambulancia.id)
            latitude, longitude = coordenadas
            hipotenusa = math.hypot(latitude - latitude_chamado, longitude - longitude_chamado)

            hipotenusas.append({"ambulancia": ambulancia, "hipotenusa": hipotenusa})

        hipotenusas.sort(key=lambda hipotenusa: hipotenusa["hipotenusa"])

        lista_ambulancias_para_alocar = [
            candidata["ambulancia"] for candidata in hipotenusas[:max(0, qtd_vitimas)]
        ]

        return {
            "ambulancias": lista_ambulancias_para_alocar,
            "qtd_ambulancias": len(lista_ambulancias_para_alocar)
        }