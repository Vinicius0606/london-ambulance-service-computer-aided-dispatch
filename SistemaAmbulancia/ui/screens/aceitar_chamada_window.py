from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, 
QFrame, QVBoxLayout, QScrollArea, QSizePolicy, QGraphicsDropShadowEffect, QPushButton)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QColor
import datetime
from domain.Modulo_Mapa.mapa import Mapa

class Aceitar_Chamada_Window(QMainWindow):

    def __init__(self):

        super().__init__()

        tela_usuario_tamanho = QApplication.instance().primaryScreen().size()

        self.larguraTela = tela_usuario_tamanho.width()
        self.alturaTela = tela_usuario_tamanho.height()

        self.mapa = Mapa([])

        div_geral = QWidget()
        div_geral.setStyleSheet("background-color: #1d1e27;")

        self.layout_lista_atendimentos = QVBoxLayout()

        layout_geral = QHBoxLayout()
        layout_geral.setContentsMargins(0, 0, 0, 0)
        layout_geral.setSpacing(0)

        menu_lateral = self.__criar_menu_lateral()

        div_componentes = self.__criar_div_componentes()


        layout_geral.addWidget(menu_lateral, 1)
        layout_geral.addWidget(div_componentes, 17)

        div_geral.setLayout(layout_geral)

        self.setCentralWidget(div_geral)

    def __criar_menu_lateral(self):

        menu_lateral = QWidget()
        menu_lateral.backgroundRole()
        menu_lateral.setStyleSheet("""
            background-color: #161920;
        """)

        layout_menu_lateral = QVBoxLayout()

        botao_perfil = QPushButton()
        botao_perfil.setIcon(QIcon("ui/assets/user.png"))
        botao_perfil.setIconSize(QSize(48,48))

        botao_mapa = QPushButton()
        botao_mapa.setIcon(QIcon("ui/assets/map.png"))
        botao_mapa.setIconSize(QSize(48,48))

        botao_sair = QPushButton()
        botao_sair.setIcon(QIcon("ui/assets/exit.png"))
        botao_sair.setIconSize(QSize(48,48))

        layout_menu_lateral.addWidget(botao_perfil, 1, alignment= Qt.AlignTop)
        layout_menu_lateral.addWidget(botao_mapa, 30, alignment= Qt.AlignTop)
        layout_menu_lateral.addWidget(botao_sair, 1, alignment= Qt.AlignBottom)

        menu_lateral.setLayout(layout_menu_lateral)

        return menu_lateral
    
    def __criar_div_componentes(self):
    
        div = QWidget()

        div.backgroundRole()
        div.setStyleSheet("""
            background-color: #161920;
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        novo_chamado_texto = QLabel("Novo Chamado!")

        novo_chamado_texto.setAlignment(Qt.AlignLeft)
        novo_chamado_texto.setStyleSheet("""
            color: #dde1f2;
            font-family: Arial;
            font-size: 32px;
            font-weight: bold;
        """)

        div_mapa_e_card = self.__criar_div_mapa_e_card()

        layout.addWidget(novo_chamado_texto, 1)
        layout.addWidget(div_mapa_e_card, 19)
        
        div.setLayout(layout)

        return div
    
    def __criar_div_mapa_e_card(self):

        div = QWidget()

        div.backgroundRole()
        div.setStyleSheet("""
            background-color: #161920;
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        mapa_frame = self.mapa.retornar_mapa_QWidget()
        mapa_frame.setFixedWidth(self.larguraTela / 2)
        mapa_frame.setFixedHeight(self.alturaTela / 1.5)

        div_chamados_recebidos = self.__criar_div_chamados_recebidos()

        layout.addWidget(div_chamados_recebidos, 1, alignment=Qt.AlignTop)
        layout.addWidget(mapa_frame, 2, alignment=Qt.AlignTop)

        div.setLayout(layout)

        return div

    
    def __criar_div_chamados_recebidos(self):
        
        div = QWidget()

        layout = self.layout_lista_atendimentos
        layout.setContentsMargins(0,10,10,0)
        layout.setSpacing(20)

        #layout.setAlignment(Qt.AlignTop)

        div.setLayout(layout)

        return div

    def adicionar_card(self, nome_paciente: str, prioridade: int, endereco: str, tempo_estimado: datetime):

        card = QWidget()
        card.setFixedHeight(self.alturaTela * 0.30)
        card.setFixedWidth(self.larguraTela * 0.25)
        card.setStyleSheet("""
            background-color: #20212a;
            font-family: Arial;
            font-weight: bold; 
            border-radius: 20px;      
        """)

        layout_card = QVBoxLayout()
        layout_card.setContentsMargins(20,10,20,10)

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(50)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0,0,0,140))  

        card_div_nome_prioridade_endereco_tempo = self.__criar_card_div_nome_prioridade_endereco(nome_paciente, prioridade, endereco, tempo_estimado)
        card_div_botoes = self.__criar_card_div_botoes()
    
        layout_card.addWidget(card_div_nome_prioridade_endereco_tempo)
        layout_card.addWidget(card_div_botoes)

        card.setLayout(layout_card)
        card.setGraphicsEffect(shadow)

        self.layout_lista_atendimentos.addWidget(card)

    def __criar_card_div_nome_prioridade_endereco(self, nome_paciente: str, prioridade: int, endereco: str, tempo_estimado: datetime):

        prioridade_texto = ""
        cor_texto = ""

        if prioridade < 5:
            
            prioridade_texto = "Baixa Prioridade"
            cor_texto = "rgba(0, 122, 255"

        elif prioridade < 15: 
            
            prioridade_texto = "Media Prioridade"
            cor_texto = "rgba(255, 193, 7"

        elif prioridade < 25:

            prioridade_texto = "Alta Prioridade"
            cor_texto = "rgba(255, 140, 0"

        else: 

            prioridade_texto = "Extrema Prioridade"
            cor_texto = "rgba(220, 53, 69"

        div = QWidget()
        layout = QVBoxLayout()

        label_nome = QLabel(nome_paciente)
        label_nome.setStyleSheet("""
            color: white;
            font-size: 20px;
        """)

        label_prioridade = QLabel(prioridade_texto)

        label_prioridade.setStyleSheet(f"""
            color: {cor_texto + ", 1)"};
            background-color: {cor_texto + ", 0.25)"};
            font-size: 14px;
            border-radius: 10px;
            padding: 10px 10px;
        """)

        label_prioridade.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        label_endereco = QLabel("📍" + endereco)
        label_endereco.setStyleSheet("""
            color: #4f5469;
            font-size: 18px;
        """)

        label_tempo_estimado = QLabel("⏱️" + tempo_estimado)
        label_tempo_estimado.setStyleSheet("""
        
            color: white;
            font-size: 18px;
        """)

        layout.addWidget(label_nome, 1, alignment=Qt.AlignBottom)
        layout.addWidget(label_prioridade, 2, alignment=Qt.AlignTop)
        layout.addWidget(label_endereco, 1)
        layout.addWidget(label_tempo_estimado, 1)

        div.setLayout(layout)

        return div
    
    def __criar_card_div_botoes(self):

        div = QWidget()
        layout = QHBoxLayout()

        botao_aceitar = QPushButton("✅Aceitar")
        botao_recusar = QPushButton("❌ Recusar")

        botao_aceitar.setStyleSheet(f"""

            background-color: green;
            font-size: 14px;
            border-radius: 10px;
            padding: 15px 15px;            
        """)

        botao_recusar.setStyleSheet(f"""

            background-color: red;
            font-size: 14px;
            border-radius: 10px;
            padding: 15px 15px;
        """)

        layout.addWidget(botao_aceitar, 1)
        layout.addWidget(botao_recusar, 1)

        div.setLayout(layout)

        return div
        
app = QApplication([])

tela = Aceitar_Chamada_Window()

tela.adicionar_card("Eu", 3, "NInteressa", "1:00")

tela.showMaximized()

app.exec()