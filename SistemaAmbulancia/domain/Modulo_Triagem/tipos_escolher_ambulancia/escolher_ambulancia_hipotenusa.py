from .interface_escolha_ambulancia import Interface_escolha_ambulancia
from domain.Modulo_Ambulancia.ambulancia import Ambulancia
import math

class Escolher_ambulancia_hipotenusa(Interface_escolha_ambulancia):

    def escolher_ambulancias(self, ambulancias: list[Ambulancia], qtd_vitimas: int, 
                             latitude_chamado: float, longitude_chamado: float):
        

        hipotenusas = []
        ids_consultados = set()

        for ambulancia in ambulancias:

            if ambulancia.status != "Disponivel" or ambulancia.id in ids_consultados:
                continue
            ids_consultados.add(ambulancia.id)

            hipotenusa = math.sqrt(
            ((ambulancia.latitudeAtual - latitude_chamado) ** 2)
            +
            ((ambulancia.longitudeAtual - longitude_chamado) ** 2)
            )

            hipotenusas.append({"ambulancia": ambulancia, "hipotenusa": hipotenusa})

        hipotenusas.sort(key=lambda hipotenusa: hipotenusa["hipotenusa"])

        lista_ambulancias_para_alocar = [
            candidata["ambulancia"] for candidata in hipotenusas[:max(0, qtd_vitimas)]
        ]

        return {
            "ambulancias": lista_ambulancias_para_alocar,
            "qtd_ambulancias": len(lista_ambulancias_para_alocar)
        }