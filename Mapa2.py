from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QEventLoop
from ..Modulo_Ambulancia.ambulancia import Ambulancia
from ..Modulo_Ambulancia.atendimento import Atendimento
from ..Modulo_Chamada.chamada import Chamada
from events.gerenciador_eventos import Gerenciador_eventos
from ..Modulo_Ambulancia.despacho import Despacho

class Mapa:

    def __init__(self, gerenciador_eventos: Gerenciador_eventos):
        self.ambulancias: list[Ambulancia] = []
        self.chamadas: list[Chamada] = []
        self.despachos: list[Despacho] = []

        self.mapa_web = QWebEngineView()
      
        self.mapa_web.loadFinished.connect(self.codigo_mapa_carregado)

        self.mapa_web.load(QUrl("http://127.0.0.1:8000/mapa.html"))
        self.mapa_web.resize(1000, 700)

        self.mapa_carregado = False


        self.gerenciador_eventos = gerenciador_eventos

        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Chamada_criada", self.adicionar_chamada)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Despacho_criado", self.adicionar_rotas)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Ambulancia_criada", self.ambulancia_criada)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Ambulancia_movimentada", self.mover_ambulancias)

    def codigo_mapa_carregado(self):

        self.mapa_carregado = True

        for ambulancia in self.ambulancias:
            
            self.mapa_web.page().runJavaScript(
                f"""adicionar_ambulancia({ambulancia.id}, {ambulancia.latitudeAtual}, 
                {ambulancia.longitudeAtual}, '{ambulancia.status}')"""
            )

        for chamada in self.chamadas:

            self.mapa_web.page().runJavaScript(
                f"""adicionar_chamada({chamada.id}, {chamada.endereco.latitude},
                {chamada.endereco.longitude}, '{chamada.status}')"""
            )

        for despacho in self.despachos:

                self.mapa_web.page().runJavaScript(
                    f"""adicionar_rota_ambulancia({despacho.ambulancia.id}, 
                    {despacho.chamada.endereco.latitude}, {despacho.chamada.endereco.longitude})"""
                )

                self.mapa_web.page().runJavaScript(
                    f"""atualizar_status({despacho.ambulancia.id}, 'Atendendo')"""
                )


    def ambulancia_criada(self, ambulancia):

        if self.mapa_carregado == False:

            self.ambulancias.append(ambulancia)

            return

        self.mapa_web.page().runJavaScript(
                f"""adicionar_ambulancia({ambulancia.id}, {ambulancia.latitudeAtual}, 
                {ambulancia.longitudeAtual}, '{ambulancia.status}')""",
                lambda r: print(r)
            )

    def adicionar_chamada(self, chamada):

        if self.mapa_carregado == False:

            self.chamadas.append(chamada)

            return

        self.mapa_web.page().runJavaScript(
                f"""adicionar_chamada({chamada.id}, {chamada.endereco.latitude},
                {chamada.endereco.longitude}, '{chamada.status}')"""
            )

    def adicionar_rotas(self, despacho: Despacho):

        if self.mapa_carregado == False:

            self.despachos.append(despacho)
            
            return

        self.mapa_web.page().runJavaScript(
            f"""adicionar_rota_ambulancia({despacho.ambulancia.id}, 
            {despacho.chamada.endereco.latitude}, {despacho.chamada.endereco.longitude})""",
        )

        self.mapa_web.page().runJavaScript(
            f"""atualizar_status({despacho.ambulancia.id}, 'Atendendo')""",
        )

    def mover_ambulancias(self, ambulancia: Ambulancia):

        self.mapa_web.page().runJavaScript(
            f"""mover_ambulancia({ambulancia.id}, 
            {ambulancia.latitudeAtual}, {ambulancia.longitudeAtual})"""
        )

    def exibirAtendimentos():
        pass

    def exibirRotas(self, ambulancia: Ambulancia, latitude_destino: float, longitude_destino: float):
        self.mapa_web.page().runJavaScript(
            f"desenhar_rota({ambulancia.id}, {ambulancia.latitudeAtual}, {ambulancia.longitudeAtual}, {latitude_destino}, {longitude_destino})"
        )

    def retornar_mapa_QWidget(self):

        if(self.mapa_web): return self.mapa_web