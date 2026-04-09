from ui.screens.main_window import Janela_principal
from ui.screens.mapa_window import Mapa_window
from ui.screens.registro_chamada_window import Registro_chamada_window
from domain.Modulo_Mapa.mapa import Mapa

class Gerenciador_telas:

    def __init__(self, mapa_tela_principal: Mapa, mapa_tela_mapa: Mapa):

        self.tela_principal = Janela_principal(mapa_tela_principal, self.abrir_tela_registro, self.abrir_tela_mapa)
        self.tela_mapa = Mapa_window(mapa_tela_mapa, self.abrir_tela_principal)
        self.tela_registro = Registro_chamada_window(self.abrir_tela_principal, self.abrir_tela_mapa)

    def abrir_tela_principal(self):

        self.tela_mapa.hide()

        self.tela_registro.hide()

        self.tela_principal.showMaximized()

    def abrir_tela_registro(self):

        self.tela_principal.hide()

        self.tela_registro.showMaximized()

    def abrir_tela_mapa(self):

        self.tela_principal.hide()

        self.tela_registro.hide()

        self.tela_mapa.showMaximized()
