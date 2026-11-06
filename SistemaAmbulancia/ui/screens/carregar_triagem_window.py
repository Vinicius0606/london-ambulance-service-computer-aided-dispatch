from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout,
QVBoxLayout, QPushButton, QComboBox, QLineEdit, QMessageBox)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QMovie, QIntValidator
from typing import Callable
from domain.Modulo_Triagem.triagem import ErroConfirmacaoTriagem
from domain.Modulo_Chamada.prioridade import Prioridade, normalizar_prioridade
import re

class Carregar_triagem_window(QMainWindow):

    def __init__(self, carregando: bool, prioridade:str = None , qtd_ambulancias:int = None, 
                 placas_ambulancias: list = None, funcao_verificar_ambulancias: Callable = None, 
                 funcao_disparar_evento: Callable = None, triagem_id: int = None,
                 qtd_ambulancias_solicitada: int | None = None):
        super().__init__()

        tela_usuario_tamanho = QApplication.instance().primaryScreen().size()

        self.larguraTela = tela_usuario_tamanho.width()
        self.alturaTela = tela_usuario_tamanho.height()

        self.prioridade = prioridade
        self.qtd_ambulancias = qtd_ambulancias
        self.qtd_ambulancias_solicitada = qtd_ambulancias_solicitada
        self.placas_ambulancias = placas_ambulancias
        self.triagem_id = triagem_id

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
        
        combo_box_prioridade.addItems([prioridade.value for prioridade in Prioridade])
        nivel = normalizar_prioridade(self.prioridade)
        if nivel is None:
            combo_box_prioridade.setCurrentIndex(-1)
        else:
            combo_box_prioridade.setCurrentText(nivel.value)

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

        for index, placa_ambulancia in enumerate(self.placas_ambulancias):
            
            string_placas_ambulancias += (placa_ambulancia)

            if index != len(self.placas_ambulancias) - 1:

                string_placas_ambulancias += " "


        input_ambulancias.setText(string_placas_ambulancias)

        botao_confirmar = QPushButton("Enviar Triagem")
        botao_confirmar.setStyleSheet("""

                background-color: #1039b4;
                padding: 10px;                   
        """)

        botao_confirmar.clicked.connect(lambda: self.__enviar_dados_inseridos(
                    combo_box_prioridade.currentText(), input_qtd_ambulancias.text(),
                    input_ambulancias.text()))

        layout.addWidget(label_prioridade, 1)
        layout.addWidget(combo_box_prioridade, 2, alignment=Qt.AlignTop)
        layout.addWidget(label_qtd_ambulancias, 1)
        layout.addWidget(input_qtd_ambulancias, 2, alignment=Qt.AlignTop)
        layout.addWidget(label_placa_ambulancias, 1)
        layout.addWidget(input_ambulancias, 2, alignment=Qt.AlignTop)
        if (
            self.qtd_ambulancias_solicitada is not None
            and self.qtd_ambulancias_solicitada > self.qtd_ambulancias
        ):
            aviso = QLabel(
                f"Frota insuficiente. Há {self.qtd_ambulancias} de "
                f"{self.qtd_ambulancias_solicitada} veículos solicitados disponíveis."
            )
            aviso.setWordWrap(True)
            layout.addWidget(aviso, 1)

        layout.addWidget(botao_confirmar, 1)

        div.setLayout(layout)

        return div

    def __enviar_dados_inseridos(self, prioridade: str, quantidade_digitada: str,
                                 placas_das_ambulancias: str):
        titulo = "Confirmação de triagem"
        try:
            quantidade = int(quantidade_digitada)
        except ValueError:
            quantidade = 0

        if quantidade <= 0:
            QMessageBox.warning(self, titulo, "Digite uma quantidade inteira maior que zero.")
            return

        placas = [placa for placa in re.split(r"[\s,;|]+", placas_das_ambulancias) if placa]
        if not prioridade.strip() or not placas:
            QMessageBox.warning(self, titulo, "Preencha a prioridade e as placas das ambulâncias.")
            return

        try:
            ambulancias = self.funcao_verificar_ambulancias(placas, quantidade)
            dados_triagem = {
                "id": self.triagem_id,
                "prioridade": prioridade,
                "qtd_ambulancias": quantidade,
                "ambulancias": ambulancias,
            }
            self.funcao_disparar_evento("Triagem_analisada", dados_triagem)
        except ErroConfirmacaoTriagem as erro:
            QMessageBox.warning(self, titulo, str(erro))
            return

        self.close()

