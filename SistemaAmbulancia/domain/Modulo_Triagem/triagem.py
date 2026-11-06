from events.gerenciador_eventos import Gerenciador_eventos

class ErroConfirmacaoTriagem(ValueError):
    """Dados inválidos para confirmar uma triagem."""


class Triagem:

    def __init__(self, id:int, ocorrencia: str, gerenciador_eventos: Gerenciador_eventos, 
                 latitude_do_chamado: float, longitude_do_chamado: float):
        
        self.id = id
        self.ocorrencia = ocorrencia
        self.prioridade = None
        self.qtd_ambulancias = None
        self.qtd_ambulancias_solicitada = None
        self.ambulancias = None
        self.erro = None
        self.latitude_do_chamado = latitude_do_chamado
        self.longitude_do_chamado = longitude_do_chamado

        self.dados_da_ocorrencia = {

            "triagem_id": self.id,
            "ocorrencia": self.ocorrencia,
            "latitude_do_chamado": self.latitude_do_chamado,
            "longitude_do_chamado": self.longitude_do_chamado
        }


        self.gerenciador_eventos = gerenciador_eventos

    def iniciar(self):
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Triagem_concluida", self.resultados_ia)
        self.gerenciador_eventos.emitir_evento("Triagem_iniciada", self.dados_da_ocorrencia)

    def resultados_ia(self, triagem_dict):
        if triagem_dict["triagem_id"] != self.id:
            return

        self.gerenciador_eventos.remover_ouvinte_para_evento("Triagem_concluida", self.resultados_ia)
        self.erro = triagem_dict.get("erro")
        if self.erro is None:
            self.prioridade = triagem_dict["prioridade"]
            self.qtd_ambulancias = triagem_dict["qtd_ambulancias"]
            self.qtd_ambulancias_solicitada = triagem_dict.get("qtd_ambulancias_solicitada")
            self.ambulancias = triagem_dict["ambulancias"]

        self.gerenciador_eventos.emitir_evento("Enviar_triagem_analise", self)