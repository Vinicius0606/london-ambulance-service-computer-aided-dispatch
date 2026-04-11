import sys
from PySide6.QtWidgets import QApplication
from domain.Modulo_Mapa.mapa import Mapa
from domain.Modulo_Banco_Dados.conexao_BD import Conexao_BD
from ui.gerenciador_telas import Gerenciador_telas
from events.gerenciador_eventos import Gerenciador_eventos
from domain.Modulo_Triagem.triagem import Triagem
from domain.Modulo_Triagem.IATriagem import IATriagem
from domain.Modulo_Chamada.chamada import Chamada
from domain.Modulo_Usuario.atendente import Atendente

class Sistema_principal:

    def __init__(self):

        self.app = QApplication(sys.argv)

        self.gerenciador_eventos = Gerenciador_eventos()

        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Chamada_registrada", self.chamada_registrada)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Triagem_Thread_IA", self.comecar_thread_IA)

        self.banco_de_dados = Conexao_BD()
        self.ia_triagem = IATriagem(self.gerenciador_eventos)

        self.atendente = Atendente(1, "a", "asdas", "asdasd", "Atendente", self.gerenciador_eventos)

        self.chamadas:list[Chamada] = self.banco_de_dados.retornar_chamadas()
        
        for index, chamada in enumerate(self.chamadas):

            if(chamada.status == "Encerrado"): self.chamadas.pop(index)

        self.triagens_esperando_confirmacao = []

        self.ambulancias = self.banco_de_dados.retornar_ambulancias()
        self.atendimentos_andamento = self.banco_de_dados.retornar_atendimentos()

        #self.gerenciador_eventos.emitir_evento("Chamada_enviada", [
        #    "1","2","3","4","5",6,7,"8",9,"10","Socorro meu amigo está passando mal, sem respirar"
        #])

    def comecar_thread_IA(self):

        self.ia_triagem.start()

    def chamada_registrada(self, chamada: Chamada):

        triagem = Triagem(chamada.descricao, self.gerenciador_eventos)

        self.triagens_esperando_confirmacao.append(triagem)

        self.chamadas.append(chamada)

        self.chamadas_pendentes.insert(0, chamada)

    def iniciar_telas(self):

        self.mapa_tela_Principal = Mapa(self.ambulancias, self.chamadas, self.atendimentos_andamento)
        self.mapa_tela_mapa = Mapa(self.ambulancias, self.chamadas, self.atendimentos_andamento)
        self.mapa_tela_ambulancia = Mapa(self.ambulancias, self.chamadas, self.atendimentos_andamento)

        self.Gerenciador_telas = Gerenciador_telas(self.mapa_tela_Principal, self.mapa_tela_mapa, self.mapa_tela_ambulancia)

        for atendimento in self.atendimentos_andamento:

            self.Gerenciador_telas.tela_principal.adicionar_card_atendimento(
                atendimento.chamada.nome_solicitante, 10, atendimento.chamada.endereco.logradouro, atendimento.hora_inicio)

        self.Gerenciador_telas.abrir_tela_principal()

        sys.exit(self.app.exec())
    
sistema = Sistema_principal()

sistema.iniciar_telas()