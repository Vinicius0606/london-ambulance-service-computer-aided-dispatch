from abc import ABC, abstractmethod
from domain.Modulo_Ambulancia.ambulancia import Ambulancia

class Interface_escolha_ambulancia(ABC):

    @abstractmethod
    def escolher_ambulancias(self, ambulancias: list[Ambulancia], qtd_vitimas: int, 
                             latitude_chamado: float, longitude_chamado: float) -> dict[str, list[Ambulancia] | int]:
        pass