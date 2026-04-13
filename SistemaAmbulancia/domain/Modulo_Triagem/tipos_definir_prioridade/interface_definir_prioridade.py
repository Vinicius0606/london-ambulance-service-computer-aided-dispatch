from abc import ABC, abstractmethod

class Interface_definir_prioridade(ABC):

    @abstractmethod
    def definir_prioridade(self, ocorrencia: dict) -> int:
        pass