import sys
from PySide6.QtWidgets import QApplication
from domain.Modulo_Mapa.mapa import Mapa
from domain.Modulo_Banco_Dados.conexao_BD import Conexao_BD
from ui.gerenciador_telas import Gerenciador_telas
from events.gerenciador_eventos import Gerenciador_eventos
from domain.Modulo_Triagem.triagem import Triagem
from domain.Modulo_Triagem.IATriagem import IATriagem
from domain.Modulo_Chamada.chamada import Chamada
from domain.Modulo_Ambulancia.atendimento import Atendimento
from domain.Modulo_Usuario.atendente import Atendente

class Sistema_principal:

    def __init__(self):

        self.app = QApplication(sys.argv)

        self.gerenciador_eventos = Gerenciador_eventos()

        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Chamada_registrada", self.chamada_registrada)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Triagem_Thread_IA", self.comecar_thread_IA)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Triagem_analisada", self.criar_atendimento)

        self.banco_de_dados = Conexao_BD(self.gerenciador_eventos)

        self.atendente = Atendente(1, "a", "asdas", "asdasd", "Atendente", self.gerenciador_eventos)

        self.chamadas:list[Chamada] = self.banco_de_dados.retornar_chamadas()
        
        for index, chamada in enumerate(self.chamadas):

            if(chamada.status == "Encerrado"): self.chamadas.pop(index)

        self.triagens_esperando_confirmacao = []

        self.ambulancias = self.banco_de_dados.retornar_ambulancias()
        self.atendimentos_andamento = self.banco_de_dados.retornar_atendimentos()

        self.ia_triagem = IATriagem(self.gerenciador_eventos, self.ambulancias)
        self.id_triagem = -1
        self.id_atendimento = -1

    def comecar_thread_IA(self):

        self.ia_triagem.start()

    def chamada_registrada(self, chamada: Chamada):

        triagem = Triagem(self.id_triagem, chamada.descricao, self.gerenciador_eventos, 
                          chamada.endereco.latitude, chamada.endereco.longitude)
        
        self.id_triagem -= 1

        self.triagens_esperando_confirmacao.append([triagem, chamada])

        self.chamadas.append(chamada)

        self.chamadas.insert(0, chamada)

    def criar_atendimento(self, dados_triagem):

        chamada = None

        for triagem_chamada in self.triagens_esperando_confirmacao:

            if triagem_chamada[0].id == dados_triagem["id"]:

                chamada = triagem_chamada[1]
                chamada.atualizar_dados(dados_triagem["prioridade"], 'Alocado')
                
                break

        atendimento = Atendimento(self.id_atendimento, chamada, dados_triagem["qtd_ambulancias"], 
                                  dados_triagem["ambulancias"], self.gerenciador_eventos)

        self.id_atendimento -= 1

        atendimento.criarDespachos()

        self.atendimentos_andamento.append(atendimento)

        self.Gerenciador_telas.tela_principal.adicionar_card_atendimento(
                atendimento.chamada.nome_solicitante, atendimento.chamada.prioridade, 
                atendimento.chamada.endereco.logradouro, atendimento.hora_inicio)

    def iniciar_telas(self):

        self.mapa_tela_Principal = Mapa(self.ambulancias, self.chamadas, self.atendimentos_andamento, self.gerenciador_eventos)
        self.mapa_tela_mapa = Mapa(self.ambulancias, self.chamadas, self.atendimentos_andamento, self.gerenciador_eventos)
        self.mapa_tela_ambulancia = Mapa(self.ambulancias, self.chamadas, self.atendimentos_andamento, self.gerenciador_eventos)

        self.Gerenciador_telas = Gerenciador_telas(self.mapa_tela_Principal, self.mapa_tela_mapa, 
                                            self.mapa_tela_ambulancia, self.gerenciador_eventos, self.ambulancias)

        for atendimento in self.atendimentos_andamento:

            self.Gerenciador_telas.tela_principal.adicionar_card_atendimento(
                atendimento.chamada.nome_solicitante, atendimento.chamada.prioridade, atendimento.chamada.endereco.logradouro, atendimento.hora_inicio)

        self.Gerenciador_telas.abrir_tela_principal()

        sys.exit(self.app.exec())
    
sistema = Sistema_principal()

sistema.iniciar_telas()