from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout,
QVBoxLayout, QPushButton, QComboBox, QLineEdit, QMessageBox)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QMovie, QIntValidator
from typing import Callable
import re

class Carregar_triagem_window(QMainWindow):

    def __init__(self, carregando: bool, prioridade:str = None , qtd_ambulancias:int = None, 
                 placas_ambulancias: list = None, funcao_verificar_ambulancias: Callable = None, funcao_disparar_evento: Callable = None):
        super().__init__()

        tela_usuario_tamanho = QApplication.instance().primaryScreen().size()

        self.larguraTela = tela_usuario_tamanho.width()
        self.alturaTela = tela_usuario_tamanho.height()

        self.prioridade = prioridade
        self.qtd_ambulancias = qtd_ambulancias
        self.placas_ambulancias = placas_ambulancias

        self.funcao_verificar_ambulancias = funcao_verificar_ambulancias
        self.funcao_disparar_evento = funcao_disparar_evento

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setFixedSize(self.larguraTela / 3, self.alturaTela / 2)

        div_geral = QWidget()
        div_geral.setStyleSheet("background-color: #1d1e27;")

        layout_geral = QHBoxLayout()

        div_generica = None

        if carregando: div_generica = self.__criar_div_carregando()
        else: div_generica = self.__criar_div_confirmar_triagem()
        layout_geral.addWidget(div_generica, 1)

        div_geral.setLayout(layout_geral)

        self.setCentralWidget(div_geral)

    def __criar_div_carregando(self):

        div = QWidget()

        layout = QVBoxLayout()

        label_fazendo_triagem = QLabel("Fazendo Triagem")
        label_fazendo_triagem.setStyleSheet("""
            color: white;
            font-size: 32px;
            font-family: Arial;
            font-weight: bold;
        """)

        label_gif_carregar = QLabel()

        gif_carregar = QMovie("ui/assets/fire-alarm-police-chase.gif")
        gif_carregar.setScaledSize(QSize(self.larguraTela / 5, self.alturaTela / 3))

        label_gif_carregar.setMovie(gif_carregar)

        gif_carregar.start()

        layout.addWidget(label_fazendo_triagem, 1, alignment=Qt.AlignCenter)
        layout.addWidget(label_gif_carregar, 19, alignment=Qt.AlignCenter)

        div.setLayout(layout)

        return div
    
    def __criar_div_confirmar_triagem(self):

        div = QWidget()
        div.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-family: Arial;
            font-weight: bold;       
        """)

        layout = QVBoxLayout()

        label_prioridade = QLabel("Prioridade: ")

        combo_box_prioridade = QComboBox()
        
        combo_box_prioridade.setStyleSheet("""
            QComboBox {
                background-color: #222533;
                padding: 10px;
            }

            QComboBox::drop-down {
                border: none;
                width: 30px;
            }

            QComboBox::down-arrow {
                image: url(assets/angulo-para-baixo.png);
                width: 12px;
                height: 12px;
            }
        """)
        
        prioridade_string = ""

        if self.prioridade == 1: prioridade_string = "Transporte"
        elif self.prioridade == 2: prioridade_string = "Moderada"
        elif self.prioridade == 3: prioridade_string = "Alta"
        else: prioridade_string = "Extrema"

        combo_box_prioridade.addItems(["Transporte", "Moderada", "Alta", "Extrema"])

        combo_box_prioridade.setCurrentText(prioridade_string)

        label_qtd_ambulancias = QLabel("Quantidade de Ambulancias: ")

        input_qtd_ambulancias = QLineEdit()
        input_qtd_ambulancias.setStyleSheet("""
                
                background-color: #222533;
                padding: 10px;                   
        """)

        validador_numeros = QIntValidator()

        input_qtd_ambulancias.setValidator(validador_numeros)

        input_qtd_ambulancias.setText((str)(self.qtd_ambulancias))

        label_placa_ambulancias = QLabel("Placa das Ambulancias: ")

        input_ambulancias = QLineEdit()
        input_ambulancias.setStyleSheet("""
                
                background-color: #222533;
                padding: 10px;                   
        """)

        string_placas_ambulancias = ""

        for placa_ambulancia in self.placas_ambulancias:

            string_placas_ambulancias += (placa_ambulancia + " ")

        input_ambulancias.setText(string_placas_ambulancias)

        botao_confirmar = QPushButton("Enviar Triagem")
        botao_confirmar.setStyleSheet("""

                background-color: #1039b4;
                padding: 10px;                   
        """)

        botao_confirmar.clicked.connect(lambda: self.__enviar_dados_inseridos(
            combo_box_prioridade.currentText(), int(input_qtd_ambulancias.text()), input_ambulancias.text(), input_ambulancias))

        layout.addWidget(label_prioridade, 1)
        layout.addWidget(combo_box_prioridade, 2, alignment=Qt.AlignTop)
        layout.addWidget(label_qtd_ambulancias, 1)
        layout.addWidget(input_qtd_ambulancias, 2, alignment=Qt.AlignTop)
        layout.addWidget(label_placa_ambulancias, 1)
        layout.addWidget(input_ambulancias, 2, alignment=Qt.AlignTop)
        layout.addWidget(botao_confirmar, 1)

        div.setLayout(layout)

        return div

    def __enviar_dados_inseridos(self, prioridade: str, qtd_ambulancias: int, 
                                 placas_das_ambulancias: str, input_ambulancias: QLineEdit):

        placas_das_ambulancias_lista = re.split(r"[ ,;|]+", placas_das_ambulancias)

        placas_das_ambulancias_lista_corrigidas = []

        for placa in placas_das_ambulancias_lista:

            placas_das_ambulancias_lista_corrigidas.append((placa.strip()))

            if(qtd_ambulancias == 1): break

        ambulancias_objetos = self.funcao_verificar_ambulancias(placas_das_ambulancias_lista_corrigidas)

        if not ambulancias_objetos:
            
            input_ambulancias.setStyleSheet("""
                        border: 2px solid red; 
                        padding: 10px
                    """)

            QMessageBox.warning(self, "Placas Inexistente", "Digite placas de ambulâncias validas!!")

            return
        
        dados_triagem = {
            "prioridade": prioridade,
            "qtd_ambulancias": qtd_ambulancias,
            "ambulancias": placas_das_ambulancias_lista_corrigidas
        }

        self.close()

        self.funcao_disparar_evento("Triagem_analisada", dados_triagem)

