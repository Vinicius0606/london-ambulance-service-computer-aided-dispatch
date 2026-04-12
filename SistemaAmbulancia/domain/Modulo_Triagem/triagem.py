from events.gerenciador_eventos import Gerenciador_eventos

class Triagem:

    def __init__(self, ocorrencia: str, gerenciador_eventos: Gerenciador_eventos, latitude_do_chamado: float, longitude_do_chamado: float):
        
        self.ocorrencia = ocorrencia
        self.prioridade = None
        self.qtdAmbulancias = None
        self.ambulancias = None
        self.latitude_do_chamado = latitude_do_chamado
        self.longitude_do_chamado = longitude_do_chamado

        self.dados_da_ocorrencia = {

            "ocorrencia": self.ocorrencia,
            "latitude_do_chamado": self.latitude_do_chamado,
            "longitude_do_chamado": self.longitude_do_chamado
        }


        self.gerenciador_eventos = gerenciador_eventos

        self.gerenciador_eventos.emitir_evento("Triagem_iniciada", self.dados_da_ocorrencia)

        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Triagem_concluida", self.resultados_ia)

    def resultados_ia(self, triagem_dict):
        
        self.prioridade = triagem_dict["prioridade"]
        self.qtdAmbulancias = triagem_dict["qtd_ambulancias"]
        self.ambulancias = triagem_dict["ambulancias"]

        self.gerenciador_eventos.emitir_evento("Enviar_triagem_analise", self)

    def ajustarResultados():
        pass