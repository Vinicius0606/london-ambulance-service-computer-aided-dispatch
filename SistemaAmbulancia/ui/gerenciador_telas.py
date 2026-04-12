from datetime import datetime
from ui.screens.main_window import Janela_principal
from ui.screens.mapa_window import Mapa_window
from ui.screens.registro_chamada_window import Registro_chamada_window
from ui.screens.aceitar_chamada_window import Aceitar_Chamada_Window
from ui.screens.carregar_triagem_window import Carregar_triagem_window
from domain.Modulo_Mapa.mapa import Mapa
from events.gerenciador_eventos import Gerenciador_eventos
from domain.Modulo_Triagem.triagem import Triagem
from domain.Modulo_Ambulancia.ambulancia import Ambulancia

class Gerenciador_telas:

    def __init__(self, mapa_tela_principal: Mapa, mapa_tela_mapa: Mapa, 
                 mapa_tela_ambulancia: Mapa, gerenciador_eventos: Gerenciador_eventos,
                 ambulancias: list[Ambulancia]):

        self.tela_principal = Janela_principal(mapa_tela_principal, self.abrir_tela_registro, self.abrir_tela_mapa, self.abrir_tela_ambulancia)
        self.tela_mapa = Mapa_window(mapa_tela_mapa, self.abrir_tela_principal, self.abrir_tela_ambulancia)
        self.tela_registro = Registro_chamada_window(self.abrir_tela_principal, self.abrir_tela_mapa, self.abrir_tela_ambulancia, self.disparar_evento)
        self.tela_ambulancia = Aceitar_Chamada_Window(mapa_tela_ambulancia, self.abrir_tela_principal, self.abrir_tela_mapa)

        self.gerenciador_eventos = gerenciador_eventos

        self.ambulancias = ambulancias

        self.carregar_triagem_window = None

        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Triagem_Thread_IA", self.abrir_tela_carregando_triagem)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Enviar_triagem_analise", self.abrir_tela_confirmar_triagem)

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

    def abrir_tela_carregando_triagem(self):

        self.carregar_triagem_window = Carregar_triagem_window(carregando=True)

        self.carregar_triagem_window.show()
    
    def abrir_tela_confirmar_triagem(self, triagem: Triagem):

        self.carregar_triagem_window.close()
        
        self.confirmar_triagem_window = Carregar_triagem_window(carregando=False, prioridade=triagem.prioridade, 
                        qtd_ambulancias=triagem.qtdAmbulancias, placas_ambulancias=triagem.ambulancias, 
                        funcao_verificar_ambulancias=self.analisar_ambulancias, funcao_disparar_evento=self.disparar_evento)

        self.confirmar_triagem_window.show()

    def disparar_evento(self, nome_evento: str, dados):

        self.gerenciador_eventos.emitir_evento(nome_evento, dados)

    def analisar_ambulancias(self, placas_ambulancias: list[str]):

        ambulancias_alocadas: list[Ambulancia] = []

        for placa in placas_ambulancias:

            existe_ambulancia = False

            for ambulancia in self.ambulancias:

                if ambulancia.placa == placa:
                    
                    existe_ambulancia = True
                    ambulancias_alocadas.append(ambulancia)

                    break

            if not existe_ambulancia: return None

        return ambulancias_alocadas