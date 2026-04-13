from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from ..Modulo_Ambulancia.ambulancia import Ambulancia
from ..Modulo_Ambulancia.atendimento import Atendimento
from ..Modulo_Chamada.chamada import Chamada
from events.gerenciador_eventos import Gerenciador_eventos
from ..Modulo_Ambulancia.despacho import Despacho

class Mapa:

    def __init__(self, ambulancias: list[Ambulancia], chamadas: list[Chamada] , 
                 atendimentos: list[Atendimento], gerenciador_eventos: Gerenciador_eventos):
        
        self.ambulancias: list[Ambulancia] = ambulancias
        self.chamadas: list[Chamada] = chamadas
        self.atendimentos: list[Atendimento] = atendimentos
        
        self.mapa_web = QWebEngineView()

        self.mapa_web.load(QUrl("http://127.0.0.1:8000/mapa.html"))
        self.mapa_web.resize(1000, 700)

        self.mapa_web.loadFinished.connect(self.codigo_mapa_carregado)

        self.gerenciador_eventos = gerenciador_eventos

        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Chamada_criada", self.adicionar_chamada)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Despacho_criado", self.adicionar_rotas)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Ambulancia_movimentada", self.mover_ambulancias)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Atendimento_finalizado", self.finalizar_atendimento)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Ambulancia_retornar_hospital", self.adicionar_rotas)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Ambulancia_mudou_status", self.atualizar_status_ambulancia)
    
    def codigo_mapa_carregado(self):
        
        for ambulancia in self.ambulancias:
            
            self.mapa_web.page().runJavaScript(
                f"""adicionar_ambulancia({ambulancia.id}, {ambulancia.latitudeAtual}, 
                {ambulancia.longitudeAtual}, '{ambulancia.status}')"""
            )

        for chamada in self.chamadas:
            
            if chamada.status != 'Finalizado':

                self.mapa_web.page().runJavaScript(
                    f"""adicionar_chamada({chamada.id}, {chamada.endereco.latitude},
                    {chamada.endereco.longitude}, '{chamada.status}')"""
                )

        for atendimento in self.atendimentos:

            if len(atendimento.ambulancias_alocadas) == 0: continue

            for ambulancia in atendimento.ambulancias_alocadas:

                self.mapa_web.page().runJavaScript(
                    f"""adicionar_rota_ambulancia({ambulancia.id}, 
                    {atendimento.chamada.endereco.latitude}, {atendimento.chamada.endereco.longitude})"""
                )

                self.mapa_web.page().runJavaScript(
                    f"""atualizar_status_ambulancia({ambulancia.id}, 'Atendendo')"""
                )
        
        self.gerenciador_eventos.emitir_evento("Mapa_carregado")

    def adicionar_chamada(self, chamada):

         self.mapa_web.page().runJavaScript(
                f"""adicionar_chamada({chamada.id}, {chamada.endereco.latitude},
                {chamada.endereco.longitude}, '{chamada.status}')"""
            )

    def adicionar_rotas(self, despacho: Despacho):

        if despacho.status == "Retornando":
            
            self.mapa_web.page().runJavaScript(
                f"""adicionar_rota_ambulancia({despacho.ambulancia.id}, 
                {-15.834400}, {-47.911496})"""
            )

            return

        self.mapa_web.page().runJavaScript(
            f"""adicionar_rota_ambulancia({despacho.ambulancia.id}, 
            {despacho.chamada.endereco.latitude}, {despacho.chamada.endereco.longitude})"""
        )

        self.mapa_web.page().runJavaScript(
            f"""atualizar_status_ambulancia({despacho.ambulancia.id}, 'Atendendo')"""
        )

        self.mapa_web.page().runJavaScript(
            f"""atualizar_status_chamada({despacho.chamada.id}, 'Alocado')"""
        )

    def mover_ambulancias(self, ambulancia: Ambulancia):

        self.mapa_web.page().runJavaScript(
            f"""mover_ambulancia({ambulancia.id}, 
            {ambulancia.latitudeAtual}, {ambulancia.longitudeAtual})"""
        )

    def finalizar_atendimento(self, atendimento: Atendimento):

        self.mapa_web.page().runJavaScript(
            f"remover_chamada({atendimento.chamada.id})"
        )

    def atualizar_status_ambulancia(self, ambulancia: Ambulancia):

        self.mapa_web.page().runJavaScript(
            f"atualizar_status_ambulancia({ambulancia.id}, '{ambulancia.status}')"
        )

    def retornar_mapa_QWidget(self):

        if(self.mapa_web): return self.mapa_web