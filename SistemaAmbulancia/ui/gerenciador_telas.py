from datetime import datetime
from ui.screens.main_window import Janela_principal
from ui.screens.mapa_window import Mapa_window
from ui.screens.registro_chamada_window import Registro_chamada_window
from ui.screens.aceitar_chamada_window import Aceitar_Chamada_Window
from domain.Modulo_Mapa.mapa import Mapa

class Gerenciador_telas:

    def __init__(self, mapa_tela_principal: Mapa, mapa_tela_mapa: Mapa, mapa_tela_ambulancia: Mapa):

        self.tela_principal = Janela_principal(mapa_tela_principal, self.abrir_tela_registro, self.abrir_tela_mapa, self.abrir_tela_ambulancia)
        self.tela_mapa = Mapa_window(mapa_tela_mapa, self.abrir_tela_principal, self.abrir_tela_ambulancia)
        self.tela_registro = Registro_chamada_window(self.abrir_tela_principal, self.abrir_tela_mapa, self.abrir_tela_ambulancia)
        self.tela_ambulancia = Aceitar_Chamada_Window(mapa_tela_ambulancia, self.abrir_tela_principal, self.abrir_tela_mapa)

        self.tela_ambulancia.adicionar_card("Vinicius", 14, "QS10 Conjuto 20", datetime.now().minute)

    def abrir_tela_principal(self):

        self.tela_mapa.hide()

        self.tela_registro.hide()

        self.tela_ambulancia.hide()

        self.tela_principal.showMaximized()

    def abrir_tela_registro(self):

        self.tela_principal.hide()

        self.tela_registro.showMaximized()

    def abrir_tela_mapa(self):

        self.tela_principal.hide()

        self.tela_registro.hide()

        self.tela_ambulancia.hide()

        self.tela_mapa.showMaximized()

    def abrir_tela_ambulancia(self):

        self.tela_principal.hide()

        self.tela_registro.hide()
        
        self.tela_mapa.hide()

        self.tela_ambulancia.showMaximized()