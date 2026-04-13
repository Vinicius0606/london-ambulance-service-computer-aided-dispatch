from .interface_escolha_ambulancia import Interface_escolha_ambulancia
from domain.Modulo_Ambulancia.ambulancia import Ambulancia
import math

class Escolher_ambulancia_hipotenusa(Interface_escolha_ambulancia):

    def escolher_ambulancias(self, ambulancias: list[Ambulancia], qtd_vitimas: int, 
                             latitude_chamado: float, longitude_chamado: float):
        

        lista_ambulancias_para_alocar = []

        hipotenusas = []

        for ambulancia in ambulancias:

            if ambulancia.status != "Disponivel": continue

            hipotenusa = math.sqrt(
            ((ambulancia.latitudeAtual - latitude_chamado) ** 2)
            +
            ((ambulancia.longitudeAtual - longitude_chamado) ** 2)
            )

            hipotenusas.append({"ambulancia": ambulancia, "hipotenusa": hipotenusa})

        hipotenusas.sort(key=lambda hipotenusa: hipotenusa["hipotenusa"])

        lista_ambulancias_para_alocar = [ambulancia_hipotenusa["ambulancia"] for ambulancia_hipotenusa in hipotenusas[:qtd_vitimas]]

        return {
            "ambulancias": lista_ambulancias_para_alocar,
            "qtd_ambulancias": qtd_vitimas
        }