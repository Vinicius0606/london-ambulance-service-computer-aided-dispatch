from events.gerenciador_eventos import Gerenciador_eventos

class Triagem:

    def __init__(self, ocorrencia: str, gerenciador_eventos: Gerenciador_eventos):
        
        self.ocorrencia = ocorrencia
        self.prioridade = None
        self.qtdAmbulancias = None
        self.ambulancias = None

        self.gerenciador_eventos = gerenciador_eventos

        self.gerenciador_eventos.emitir_evento("Triagem_iniciada", self.ocorrencia)

        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Triagem_concluida", self.resultados_ia)

    def resultados_ia(self, triagem_dict):
        
        self.prioridade = triagem_dict["prioridade"]
        self.qtdAmbulancias = triagem_dict["qtd_ambulancias"]
        self.ambulancias = list(triagem_dict["ambulancias"])

        self.gerenciador_eventos.emitir_evento("Enviar_triagem_analise", self)

    def ajustarResultados():
        pass