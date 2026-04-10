from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, 
QFrame, QVBoxLayout, QScrollArea, QSizePolicy, QGraphicsDropShadowEffect, QPushButton)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QIcon
from datetime import datetime
from domain.Modulo_Mapa.mapa import Mapa
from ui.screens.registro_chamada_window import Registro_chamada_window
from typing import Callable
import copy

class Janela_principal(QMainWindow):

    def __init__(self, mapa: Mapa, funcao_abrir_pagina_registrar: Callable, 
                 funcao_abrir_pagina_mapa: Callable, funcao_abrir_pagina_ambulancia: Callable):
        super().__init__()

        tela_usuario_tamanho = QApplication.instance().primaryScreen().size()

        self.larguraTela = tela_usuario_tamanho.width()
        self.alturaTela = tela_usuario_tamanho.height()

        self.mapa = mapa

        self.funcao_abrir_pagina_registrar = funcao_abrir_pagina_registrar
        self.funcao_abrir_pagina_mapa = funcao_abrir_pagina_mapa
        self.funcao_abrir_pagina_ambulancia = funcao_abrir_pagina_ambulancia

        self.setWindowTitle("Sistema de Ambulância")

        self.scroll_lista_atendimentos = QScrollArea()
        self.div_lista_atendimentos = QFrame()
        self.layout_lista_atendimentos = QVBoxLayout()

        div_geral = QWidget()
        div_geral.setStyleSheet("background-color: #1d1e27;")

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

        botao_mapa.clicked.connect(self.funcao_abrir_pagina_mapa)

        botao_ambulancia = QPushButton()
        botao_ambulancia.setIcon(QIcon("ui/assets/ambulancia.png"))
        botao_ambulancia.setIconSize(QSize(48,48))

        botao_ambulancia.clicked.connect(self.funcao_abrir_pagina_ambulancia)

        botao_sair = QPushButton()
        botao_sair.setIcon(QIcon("ui/assets/exit.png"))
        botao_sair.setIconSize(QSize(48,48))

        layout_menu_lateral.addWidget(botao_perfil, 1, alignment= Qt.AlignTop)
        layout_menu_lateral.addWidget(botao_mapa, 1, alignment= Qt.AlignTop)
        layout_menu_lateral.addWidget(botao_ambulancia, 29, alignment= Qt.AlignTop)
        layout_menu_lateral.addWidget(botao_sair, 1, alignment= Qt.AlignBottom)

        menu_lateral.setLayout(layout_menu_lateral)

        return menu_lateral
    
    def __criar_div_componentes(self):
       
        div = QWidget()

        layout = QVBoxLayout()
        layout.setContentsMargins(40,50,0,0)

        texto_chamadas = QLabel("Atendimentos em andamento")
        texto_chamadas.setAlignment(Qt.AlignLeft)
        texto_chamadas.setStyleSheet("""
            color: #dde1f2;
            font-family: Arial;
            font-size: 32px;
            font-weight: bold;
        """)

        div_chamadas_mapa = self.__criar_div_chamadas_mapa()

        layout.addWidget(texto_chamadas, 1)
        layout.addWidget(div_chamadas_mapa, 18)

        div.setLayout(layout)

        return div

    def __criar_div_chamadas_mapa(self):

        div = QWidget()

        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)

        div_listas = self.__criar_div_lista_atendimentos_andamento()
        div_mapa_botao_registrar = self.__criar_div_mapa_botao_registrar()

        layout.addWidget(div_listas, 1)
        layout.addWidget(div_mapa_botao_registrar, 1)
        
        div.setLayout(layout)

        return div
    
    
    def __criar_div_lista_atendimentos_andamento(self):
        
        scroll = self.scroll_lista_atendimentos 
        div = self.div_lista_atendimentos
        layout = self.layout_lista_atendimentos

        layout.setContentsMargins(0,10,10,0)
        layout.setSpacing(20)

        layout.setAlignment(Qt.AlignTop)

        div.setLayout(layout)

        scroll.setWidget(div)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }

            QScrollBar:vertical {
                background: transparent;
                width: 5px;
                margin: 0px;
            }

            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 2px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background: rgba(255, 255, 255, 0.1);
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }
        """)

        scroll.setWidgetResizable(True)

        return scroll

    def adicionar_card_atendimento(self, nome_paciente: str, prioridade: int, endereco: str, horario_inicio: datetime):

        card = QWidget()
        card.setFixedHeight(self.scroll_lista_atendimentos.height() * 0.25)
        card.setStyleSheet("""
            background-color: #161920;
            font-family: Arial;
            font-weight: bold; 
            border-radius: 20px;      
        """)

        layout_card = QHBoxLayout()
        layout_card.setContentsMargins(20,10,20,10)

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(50)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0,0,0,140))

        card_div_nome_prioridade_endereco = self.__criar_card_div_nome_prioridade_endereco(nome_paciente, endereco, prioridade=prioridade)
        card_div_tempo = self.__criar_card_div_tempo(horario_inicio)
        
        layout_card.addWidget(card_div_nome_prioridade_endereco)
        layout_card.addWidget(card_div_tempo)

        card.setLayout(layout_card)
        card.setGraphicsEffect(shadow)

        self.layout_lista_atendimentos.addWidget(card)

    def __criar_card_div_nome_prioridade_endereco(self, nome_paciente: str, endereco: str, status: str = None, prioridade: int = None):

        div = QWidget()
        layout = QVBoxLayout()

        label_nome = QLabel(nome_paciente)
        label_nome.setStyleSheet("""
            color: white;
            font-size: 16px;
        """)

        prioridade_texto = ""
        cor_texto = ""

        if status == "Pendente": cor_texto = "rgba(220, 53, 69"
        
        elif status == "Em Triagem": cor_texto = "rgba(255, 193, 7"

        if prioridade != None:
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

        label_status = QLabel(status if status else prioridade_texto)

        label_status.setStyleSheet(f"""
            color: {cor_texto + ", 1)"};
            background-color: {cor_texto + ", 0.25)"};
            font-size: 14px;
            border-radius: 10px;
            padding: 5px 5px;
        """)

        label_status.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        label_endereco = QLabel(endereco)
        label_endereco.setStyleSheet("""
            color: #4f5469;
            font-size: 14px;
        """)

        layout.addWidget(label_nome, 1)
        layout.addWidget(label_status, 1)
        layout.addWidget(label_endereco, 1)

        div.setLayout(layout)

        return div
    
    def __criar_card_div_tempo(self, horario_recebido_da_chamada: datetime):

        tempo_atual = datetime.now()

        tempo_total_desde_chamada_recebida = tempo_atual - horario_recebido_da_chamada
        
        tempo_texto = ""

        if(tempo_total_desde_chamada_recebida.total_seconds() < 60):
            
            tempo_texto = f"{(int)(tempo_total_desde_chamada_recebida.total_seconds())} segundo(s) atrás >"
        
        else:
            
            minutos = (int)(tempo_total_desde_chamada_recebida.total_seconds() / 60)

            tempo_texto = f"{minutos} minuto(s) atrás >"

        div = QWidget()
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0,20,0,0)

        label_tempo = QLabel(tempo_texto)
        label_tempo.setAlignment(Qt.AlignRight)
        label_tempo.setStyleSheet("""
            color: #a1a6b9;
            font-size: 14px;
        """)

        layout.addWidget(label_tempo)

        div.setLayout(layout)

        return div
    
    def __criar_div_mapa_botao_registrar(self):
        
        div = QWidget()

        layout = QVBoxLayout()
        layout.setContentsMargins(0,20,0,50)
        layout.setSpacing(0)
        
        mapa_frame = self.mapa.retornar_mapa_QWidget()

        mapa_frame.setFixedWidth(self.larguraTela / 3)
        mapa_frame.setFixedHeight(self.larguraTela / 4)

        mapa_frame.setStyleSheet("border-radius: 20px")

        botao_registrar_nova_chamada = QPushButton("+ Registrar Nova Chamada")
        botao_registrar_nova_chamada.setFixedWidth(self.larguraTela / 3)

        botao_registrar_nova_chamada.setStyleSheet("""
            background-color: #0f3aaf;
            padding: 20px 20px;
            border-radius: 10px;
            color: white;
            font-size: 32px;
            font-family: Arial;
        """)

        botao_registrar_nova_chamada.setCursor(Qt.PointingHandCursor)

        botao_registrar_nova_chamada.clicked.connect(self.funcao_abrir_pagina_registrar)

        layout.addWidget(mapa_frame, 1, alignment=Qt.AlignTop | Qt.AlignHCenter)
        layout.addWidget(botao_registrar_nova_chamada, 1, alignment=Qt.AlignBottom | Qt.AlignHCenter)

        div.setLayout(layout)

        return div