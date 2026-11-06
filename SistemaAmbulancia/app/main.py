import sys
from PySide6.QtWidgets import QApplication
from services.Modulo_Mapa.mapa import Mapa
from services.Modulo_Banco_Dados.conexao_BD import Conexao_BD
from ui.gerenciador_telas import Gerenciador_telas
from events.gerenciador_eventos import Gerenciador_eventos
from domain.Modulo_Triagem.triagem import ErroConfirmacaoTriagem, Triagem
from domain.Modulo_Triagem.IATriagem import IATriagem
from domain.Modulo_Chamada.chamada import Chamada
from domain.Modulo_Chamada.prioridade import Prioridade
from domain.Modulo_Chamada.status import Status
from domain.Modulo_Ambulancia.ambulancia import Ambulancia
from domain.Modulo_Ambulancia.atendimento import Atendimento
from domain.Modulo_Usuario.atendente import Atendente
from app.simulacao import Simulacao
from domain.Modulo_Triagem.tipos_escolher_ambulancia.escolher_ambulancia_hipotenusa import Escolher_ambulancia_hipotenusa
from domain.Modulo_Triagem.tipos_definir_prioridade.definir_prioridade_pontuacao import Definir_prioridade_pontuacao

class Sistema_principal:

    def __init__(self):

        self.app = QApplication(sys.argv)

        self.gerenciador_eventos = Gerenciador_eventos()

        self.simulacao = Simulacao(self.gerenciador_eventos)

        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Chamada_registrada", self.chamada_registrada)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Triagem_Thread_IA", self.comecar_thread_IA)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Triagem_analisada", self.criar_atendimento)

        self.banco_de_dados = Conexao_BD(self.gerenciador_eventos)

        self.atendente = Atendente(1, "a", "asdas", "asdasd", "Atendente", self.gerenciador_eventos)

        self.chamadas: list[Chamada] = [
            chamada for chamada in self.banco_de_dados.retornar_chamadas()
            if chamada.status != Status.FINALIZADO.value
        ]

        self.triagens_esperando_confirmacao = []

        self.ambulancias = self.banco_de_dados.retornar_ambulancias()
        self.atendimentos_andamento = self.banco_de_dados.retornar_atendimentos()
        
        self.tipo_escolha_ambulancia = Escolher_ambulancia_hipotenusa()
        self.tipo_definir_prioridade = Definir_prioridade_pontuacao()

        self.ia_triagem = IATriagem(self.gerenciador_eventos, self.ambulancias, 
                                    self.tipo_escolha_ambulancia, self.tipo_definir_prioridade)
        self.id_triagem = -1
        self.id_atendimento = -1

    def comecar_thread_IA(self):

        self.ia_triagem.start()

    def chamada_registrada(self, chamada: Chamada):

        triagem = Triagem(self.id_triagem, chamada.descricao, self.gerenciador_eventos, 
                          chamada.endereco.latitude, chamada.endereco.longitude)
        
        self.id_triagem -= 1

        self.triagens_esperando_confirmacao.append([triagem, chamada])

        self.chamadas.insert(0, chamada)

    def criar_atendimento(self, dados_triagem):
        triagem_id = dados_triagem.get("id")
        chamada = next(
            (chamada for triagem, chamada in self.triagens_esperando_confirmacao
             if triagem.id == triagem_id),
            None,
        )
        if chamada is None or chamada not in self.chamadas or chamada.status != Status.PENDENTE.value:
            raise ErroConfirmacaoTriagem("A chamada precisa estar pendente para ser alocada.")

        prioridade = dados_triagem.get("prioridade")
        if prioridade not in (opcao.value for opcao in Prioridade):
            raise ErroConfirmacaoTriagem("Selecione uma prioridade válida.")

        quantidade = dados_triagem.get("qtd_ambulancias")
        ambulancias = dados_triagem.get("ambulancias")
        if (
            type(quantidade) is not int or quantidade <= 0
            or not isinstance(ambulancias, list) or len(ambulancias) != quantidade
        ):
            raise ErroConfirmacaoTriagem("A quantidade deve corresponder às ambulâncias selecionadas.")
        if not all(isinstance(ambulancia, Ambulancia) for ambulancia in ambulancias):
            raise ErroConfirmacaoTriagem("Selecione ambulâncias válidas.")

        ids_selecionados = {ambulancia.id for ambulancia in ambulancias}
        if len(ids_selecionados) != quantidade:
            raise ErroConfirmacaoTriagem("Selecione cada ambulância uma única vez.")

        disponiveis = {
            ambulancia.id: ambulancia for ambulancia in self.ambulancias
            if ambulancia.status == "Disponivel"
        }
        if quantidade > len(disponiveis):
            raise ErroConfirmacaoTriagem("A frota disponível é insuficiente para essa quantidade.")
        if not ids_selecionados.issubset(disponiveis):
            raise ErroConfirmacaoTriagem("Uma ou mais ambulâncias selecionadas estão indisponíveis.")

        ambulancias_alocadas = [disponiveis[ambulancia.id] for ambulancia in ambulancias]
        chamada.atualizar_dados(prioridade, Status.ALOCADO.value)
        atendimento = Atendimento(
            self.id_atendimento, chamada, quantidade,
            ambulancias_alocadas, self.gerenciador_eventos,
        )
        self.id_atendimento -= 1

        atendimento.criar_despachos()
        self.atendimentos_andamento.append(atendimento)

    def iniciar_telas(self):

        self.mapa_tela_Principal = Mapa(self.ambulancias, self.chamadas, self.atendimentos_andamento, self.gerenciador_eventos)
        self.mapa_tela_mapa = Mapa(self.ambulancias, self.chamadas, self.atendimentos_andamento, self.gerenciador_eventos)
        self.mapa_tela_ambulancia = Mapa(self.ambulancias, self.chamadas, self.atendimentos_andamento, self.gerenciador_eventos)

        self.Gerenciador_telas = Gerenciador_telas(self.mapa_tela_Principal, self.mapa_tela_mapa, 
                                            self.mapa_tela_ambulancia, self.gerenciador_eventos, self.ambulancias)

        for atendimento in self.atendimentos_andamento:

            self.Gerenciador_telas.criar_card_atendimento(atendimento)

        self.Gerenciador_telas.abrir_tela_principal()

        sys.exit(self.app.exec())
    
sistema = Sistema_principal()

sistema.iniciar_telas()