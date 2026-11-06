from datetime import datetime
from ui.screens.main_window import Janela_principal
from ui.screens.mapa_window import Mapa_window
from ui.screens.registro_chamada_window import Registro_chamada_window
from ui.screens.aceitar_chamada_window import Aceitar_Chamada_Window
from ui.screens.carregar_triagem_window import Carregar_triagem_window
from services.Modulo_Mapa.mapa import Mapa
from events.gerenciador_eventos import Gerenciador_eventos
from domain.Modulo_Triagem.triagem import ErroConfirmacaoTriagem, Triagem
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

        self.cards_atendimento = []

        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Triagem_Thread_IA", self.abrir_tela_carregando_triagem)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Enviar_triagem_analise", self.abrir_tela_confirmar_triagem)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Atendimento_criado", self.criar_card_atendimento)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Atendimento_finalizado", self.remover_card_atendimento)

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

        self.tela_registro.hide()

        self.tela_principal.showMaximized()

        self.carregar_triagem_window = Carregar_triagem_window(carregando=True)

        self.carregar_triagem_window.show()
    
    def abrir_tela_confirmar_triagem(self, triagem: Triagem):

        self.carregar_triagem_window.close()

        placas_ambulancias = []

        for ambulancia in triagem.ambulancias:

            placas_ambulancias.append(ambulancia.placa)
        
        self.confirmar_triagem_window = Carregar_triagem_window(carregando=False, prioridade=triagem.prioridade, 
                        qtd_ambulancias=triagem.qtdAmbulancias, placas_ambulancias=placas_ambulancias, 
                        funcao_verificar_ambulancias=self.analisar_ambulancias, 
                        funcao_disparar_evento=self.disparar_evento, triagem_id=triagem.id,
                        qtd_ambulancias_solicitada=triagem.qtd_ambulancias_solicitada)

        self.confirmar_triagem_window.show()

    def disparar_evento(self, nome_evento: str, dados):

        self.gerenciador_eventos.emitir_evento(nome_evento, dados)
    
    def criar_card_atendimento(self, atendimento):

        card = self.tela_principal.adicionar_card_atendimento(
                atendimento.chamada.nome_solicitante, atendimento.chamada.prioridade, 
                atendimento.chamada.endereco.logradouro, atendimento.hora_inicio)
        
        self.cards_atendimento.append({"card": card, "id": atendimento.chamada.id})
        
    def remover_card_atendimento(self, atendimento):

        for card in self.cards_atendimento:

            if card["id"] == atendimento.chamada.id:

                card["card"].deleteLater()

    def analisar_ambulancias(self, placas_ambulancias: list[str], quantidade: int):
        placas = [placa.strip().upper() for placa in placas_ambulancias]
        if len(set(placas)) != len(placas):
            raise ErroConfirmacaoTriagem("Digite cada placa uma única vez.")

        por_placa = {ambulancia.placa.strip().upper(): ambulancia for ambulancia in self.ambulancias}
        ids_disponiveis = {
            ambulancia.id for ambulancia in por_placa.values()
            if ambulancia.status == "Disponivel"
        }
        if quantidade > len(ids_disponiveis):
            raise ErroConfirmacaoTriagem("A frota disponível é insuficiente para essa quantidade.")
        if len(placas) != quantidade:
            raise ErroConfirmacaoTriagem("A quantidade deve corresponder ao número de placas.")

        ambulancias_alocadas = []
        for placa in placas:
            ambulancia = por_placa.get(placa)
            if ambulancia is None:
                raise ErroConfirmacaoTriagem(f"Placa inexistente ({placa}).")
            if ambulancia.status != "Disponivel":
                raise ErroConfirmacaoTriagem(f"A ambulância de placa {placa} está indisponível.")
            ambulancias_alocadas.append(ambulancia)

        return ambulancias_alocadas