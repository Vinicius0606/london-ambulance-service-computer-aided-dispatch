from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, 
QFrame, QVBoxLayout, QScrollArea, QSizePolicy, QGraphicsDropShadowEffect, QPushButton)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QPixmap, QIcon
from domain.Modulo_Mapa.mapa import Mapa
from typing import Callable

class Mapa_window(QMainWindow):

    def __init__(self, mapa: Mapa, funcao_abrir_pagina_principal: Callable):
        super().__init__()

        telaUsuarioTamanho = QApplication.instance().primaryScreen().size()

        self.larguraTela = telaUsuarioTamanho.width()
        self.alturaTela = telaUsuarioTamanho.height()

        self.funcao_abrir_pagina_principal = funcao_abrir_pagina_principal

        self.mapa = mapa

        self.setWindowTitle("Sistema de Ambulância")

        div_geral = QWidget()
        div_geral.setStyleSheet("background-color: #1d1e27;")

        layout_geral = QHBoxLayout()
        layout_geral.setContentsMargins(0, 0, 0, 0)
        layout_geral.setSpacing(0)

        menu_lateral = self.__criar_menu_lateral()

        div_mapa_informacoes = self.__criar_div_mapa_informacoes()

        layout_geral.addWidget(menu_lateral, 1)
        layout_geral.addWidget(div_mapa_informacoes, 17)

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

        botao_sair.clicked.connect(self.funcao_abrir_pagina_principal)

        layout_menu_lateral.addWidget(botao_perfil, 1, alignment= Qt.AlignTop)
        layout_menu_lateral.addWidget(botao_mapa, 30, alignment= Qt.AlignTop)
        layout_menu_lateral.addWidget(botao_sair, 1, alignment= Qt.AlignBottom)

        menu_lateral.setLayout(layout_menu_lateral)

        return menu_lateral
    
    def __criar_div_mapa_informacoes(self):

        div = QWidget()

        layout = QVBoxLayout()
        layout.setContentsMargins(20,20,20,20)

        div_mapa = self.mapa.retornar_mapa_QWidget()
        div_mapa.setFixedHeight(self.alturaTela / 1.35)
        div_mapa.setFixedWidth(self.larguraTela / 1.25)

        div_informacoes = QWidget()
        div_informacoes.setStyleSheet("""              
            QLabel{
                color: white;
                font-size: 18px;
                font-family: Arial;
                font-weight: bold;   
                background-color: #222533;
                padding: 20px 10px;
                border-radius: 15px;    
            }
        """)

        layout_informacoes = QHBoxLayout()
        layout_informacoes.setSpacing(40)

        label_ambulancias_ativas = QLabel("Quantidade de Ambulancias ativas: 0")

        label_chamadas_pendentes = QLabel("Quantidade de chamadas pendentes: 0")

        label_chamadas_andamento = QLabel("Quantidade de chamadas em andamento: 0")

        layout_informacoes.addWidget(label_ambulancias_ativas, 1)
        layout_informacoes.addWidget(label_chamadas_pendentes, 1)
        layout_informacoes.addWidget(label_chamadas_andamento, 1)

        div_informacoes.setLayout(layout_informacoes)

        layout.addWidget(div_mapa, 19, alignment=Qt.AlignCenter | Qt.AlignTop )
        layout.addWidget(div_informacoes, 1, alignment=Qt.AlignCenter)    

        div.setLayout(layout)

        return div


