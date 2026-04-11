from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget, 
QHBoxLayout, QVBoxLayout, QLabel, QLineEdit)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
from typing import Callable
from domain.Modulo_Chamada import autocomplete as ac

class Registro_chamada_window(QMainWindow):
    
    def __init__(self, funcao_abrir_pagina_principal: Callable, 
                 funcao_abrir_tela_mapa: Callable, funcao_abrir_pagina_ambulancia: Callable,
                 funcao_disparar_evento: Callable):

        super().__init__()

        telaUsuarioTamanho = QApplication.instance().primaryScreen().size()

        self.larguraTela = telaUsuarioTamanho.width()
        self.alturaTela = telaUsuarioTamanho.height()

        self.funcao_abrir_pagina_principal = funcao_abrir_pagina_principal
        self.funcao_abrir_tela_mapa = funcao_abrir_tela_mapa
        self.funcao_abrir_pagina_ambulancia = funcao_abrir_pagina_ambulancia
        self.funcao_disparar_evento = funcao_disparar_evento

        div_geral = QWidget()
        div_geral.setStyleSheet("background-color: #1d1e27;")

        layout_geral = QHBoxLayout()
        layout_geral.setContentsMargins(0, 0, 0, 0)
        layout_geral.setSpacing(0)

        menu_lateral = self.__criar_menu_lateral()

        div_componentes = QWidget()

        layout_componentes = QVBoxLayout()
        layout_componentes.setContentsMargins(200,50,150,50)
        
        div_registro = self.__criar_div_registro()

        layout_componentes.addWidget(div_registro)

        div_componentes.setLayout(layout_componentes)

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

        botao_mapa.clicked.connect(self.funcao_abrir_tela_mapa)

        botao_ambulancia = QPushButton()
        botao_ambulancia.setIcon(QIcon("ui/assets/ambulancia.png"))
        botao_ambulancia.setIconSize(QSize(48,48))

        botao_ambulancia.clicked.connect(self.funcao_abrir_pagina_ambulancia)

        botao_sair = QPushButton()
        botao_sair.setIcon(QIcon("ui/assets/exit.png"))
        botao_sair.setIconSize(QSize(48,48))

        botao_sair.clicked.connect(self.funcao_abrir_pagina_principal)

        layout_menu_lateral.addWidget(botao_perfil, 1, alignment= Qt.AlignTop)
        layout_menu_lateral.addWidget(botao_mapa, 1, alignment= Qt.AlignTop)
        layout_menu_lateral.addWidget(botao_ambulancia, 29, alignment= Qt.AlignTop)
        layout_menu_lateral.addWidget(botao_sair, 1, alignment= Qt.AlignBottom)

        menu_lateral.setLayout(layout_menu_lateral)

        return menu_lateral
    
    def __criar_div_registro(self):

        div_principal = QWidget()
        div_principal.setStyleSheet("""
            background-color: #20212f;
            border-radius: 20px;
        """)

        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(10)

        label_titulo = QLabel("Registrar Nova Chamada")
        label_titulo.setAlignment(Qt.AlignCenter)
        label_titulo.setStyleSheet("""
            color: #dde1f2;
            font-family: Arial;
            font-size: 32px;
            font-weight: bold;                     
        """)

        div_inputs = QWidget()
        layout_inputs = QHBoxLayout()

        div_input_nome_descricao = self.__criar_div_input_nome_descricao()
        div_input_endereco = self.__criar_div_input_endereco()

        layout_inputs.addWidget(div_input_nome_descricao, 1)
        layout_inputs.addWidget(div_input_endereco, 1)

        div_botaos = QWidget()

        layout_botaos = QHBoxLayout()

        botao_cancelar = QPushButton("Cancelar")
        botao_cancelar.setStyleSheet("""
            background-color: #222533;
            padding: 10px 20px;
            color: #7e7e98;
            font-size: 24px;
            border-radius: 10px;
        """)     
        botao_cancelar.setFixedWidth(self.larguraTela / 8)
        
        botao_registrar = QPushButton("+ Registrar Chamada")
        botao_registrar.setStyleSheet("""
            background-color: #1039b4;
            padding: 10px 20px;
            color: white;
            font-size: 24px;
            border-radius: 10px;
        """)
        botao_registrar.setFixedWidth(self.larguraTela / 4)

        botao_registrar.clicked.connect(self.finalizar_registro)

        layout_botaos.addWidget(botao_cancelar, 9, Qt.AlignRight)
        layout_botaos.addWidget(botao_registrar, 1, Qt.AlignRight)

        div_botaos.setLayout(layout_botaos)

        layout_principal.addWidget(label_titulo, 1)
        layout_principal.addWidget(div_inputs, 19)
        layout_principal.addWidget(div_botaos, 2)

        div_inputs.setLayout(layout_inputs)
        div_principal.setLayout(layout_principal)

        return div_principal
    
    def __criar_div_input_nome_descricao(self):

        div = QWidget()
        div.setStyleSheet("""
            color: white;
            font-family: Arial;
            font-size: 16px;
            font-weight: bold; 
        """)

        layout = QVBoxLayout()
        layout.setSpacing(2)

        self.label_nome = QLabel("Nome")
        self.label_nome.setStyleSheet("margin-left: 5px;")

        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Nome")
        self.input_nome.setStyleSheet("""
            background-color: #242735;
            border-radius: 10px;
            padding: 15px 10px;
        """)

        self.label_descricao = QLabel("Descrição")
        self.label_descricao.setStyleSheet("margin-left: 5px;")

        self.input_descricao = QLineEdit()
        self.input_descricao.setPlaceholderText("Descrição")
        self.input_descricao.setStyleSheet("""
            background-color: #242735;
            border-radius: 10px;
            padding: 15px 10px;
        """)

        self.input_descricao.setFixedHeight(self.alturaTela / 4)
        self.input_descricao.setAlignment(Qt.AlignTop)

        layout.addWidget(self.label_nome, 1, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_nome, 2, alignment=Qt.AlignTop)
        layout.addWidget(self.label_descricao, 1, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_descricao, 10, alignment=Qt.AlignTop)

        div.setLayout(layout)

        return div
    
    def __criar_div_input_endereco(self):
        
        div_principal = QWidget()
        div_principal.setStyleSheet("""
            color: white;
            font-family: Arial;
            font-size: 16px;
            font-weight: bold; 
        """)

        layout_principal = QVBoxLayout()
        layout_principal.setSpacing(2)

        label_titulo = QLabel("Endereço")

        div_inputs = QWidget()
        div_inputs.setStyleSheet("""
            background-color: #1c1e2a;
        """)

        layout_inputs = QVBoxLayout()

        self.label_CEP = QLabel("CEP")

        self.input_CEP = QLineEdit()
        self.input_CEP.setPlaceholderText("NNNNN-NNN")
        self.input_CEP.setStyleSheet("""
            background-color: #222635;
            border-radius: 10px;
            padding: 15px 10px;
        """)

        self.input_CEP.editingFinished.connect(self.preencher_endereco)

        self.label_logradouro = QLabel("Logradouro")

        self.input_logradouro = QLineEdit()
        self.input_logradouro.setPlaceholderText("Logradouro")
        self.input_logradouro.setStyleSheet("""
            background-color: #222635;
            border-radius: 10px;
            padding: 15px 10px;
        """)

        self.label_numero = QLabel("Número")

        self.input_numero = QLineEdit()
        self.input_numero.setPlaceholderText("Número")
        self.input_numero.setStyleSheet("""
            background-color: #222635;
            border-radius: 10px;
            padding: 15px 10px;
        """)

        self.label_cidade_bairro = QLabel("Cidade / Bairro")

        div_cidade_bairro = QWidget()

        layout_div_cidade_bairro = QHBoxLayout()

        self.input_cidade = QLineEdit()
        self.input_cidade.setPlaceholderText("Cidade")
        self.input_cidade.setStyleSheet("""
            background-color: #222635;
            border-radius: 10px;
            padding: 15px 10px;
        """)

        self.input_bairro = QLineEdit()
        self.input_bairro.setPlaceholderText("Bairro")
        self.input_bairro.setStyleSheet("""
            background-color: #222635;
            border-radius: 10px;
            padding: 15px 10px;
        """)

        layout_div_cidade_bairro.addWidget(self.input_cidade)
        layout_div_cidade_bairro.addWidget(self.input_bairro)

        div_cidade_bairro.setLayout(layout_div_cidade_bairro)

        self.label_complemento = QLabel("Complemento (opcional)")

        self.input_complemento = QLineEdit()
        self.input_complemento.setPlaceholderText("Complemento")
        self.input_complemento.setStyleSheet("""
            background-color: #222635;
            border-radius: 10px;
            padding: 15px 10px;
        """)

        layout_inputs.addWidget(self.label_CEP, 1, alignment=Qt.AlignTop)
        layout_inputs.addWidget(self.input_CEP, 4, alignment=Qt.AlignTop)
        layout_inputs.addWidget(self.label_logradouro, 1, alignment=Qt.AlignTop)
        layout_inputs.addWidget(self.input_logradouro, 4, alignment=Qt.AlignTop) 
        layout_inputs.addWidget(self.label_numero, 1, alignment=Qt.AlignTop)
        layout_inputs.addWidget(self.input_numero, 4, alignment=Qt.AlignTop) 
        layout_inputs.addWidget(self.label_cidade_bairro, 1, alignment=Qt.AlignTop)
        layout_inputs.addWidget(div_cidade_bairro, 4, alignment=Qt.AlignTop) 
        layout_inputs.addWidget(self.label_complemento, 1, alignment=Qt.AlignTop)
        layout_inputs.addWidget(self.input_complemento, 4, alignment=Qt.AlignTop) 

        div_inputs.setLayout(layout_inputs)

        layout_principal.addWidget(label_titulo, 1)
        layout_principal.addWidget(div_inputs, 19)

        div_principal.setLayout(layout_principal)

        return div_principal
    


    def preencher_endereco(self):
        valores = ac.buscar_por_cep(self.input_CEP.text())
        if valores:
            self.input_logradouro.setText(valores.get("logradouro", ""))
            self.input_bairro.setText(valores.get("bairro", ""))
            self.input_cidade.setText(valores.get("cidade", ""))

    def finalizar_registro(self):

        registro = {}

        endereco = ac.buscar_por_cep(self.input_CEP.text())

        nome = None
        numero = None
        complemento = None
        cidade = None

        if self.input_nome.text() != "": nome = self.input_nome.text()
        if self.input_numero.text() != "": numero = self.input_numero.text()
        if self.input_complemento.text() != "": complemento = self.input_numero.text()
        if self.input_cidade.text() != "": cidade = self.input_cidade.text()

        if endereco != None:

            latitude = endereco["latitude"]
            longitude = endereco["longitude"]

            if latitude is None and longitude is None:

                latitude, longitude = ac.buscar_por_endereco(
                    endereco.get("logradouro"),
                    endereco.get("bairro"),
                    endereco.get("cidade"),
                    "DF",
                    endereco.get("cep")
                )

            registro = {

                "nome": nome,
                "descricao": self.input_descricao.text(),
                "logradouro": endereco.get("logradouro"),
                "numero": numero,
                "complemento": complemento,
                "bairro": endereco.get("bairro"),
                "cidade": cidade,
                "estado": "DF",
                "cep": endereco.get("cep"),
                "latitude": latitude,
                "longitude": longitude
            }
            
            self.funcao_disparar_evento("Chamada_enviada", registro)

        elif (self.input_descricao.text() != "" and 
            self.input_logradouro.text() != "" and
            self.input_bairro.text() != ""):

         
            latitude, longitude = ac.buscar_por_endereco(
                endereco.get("logradouro"),
                endereco.get("bairro"),
                endereco.get("cidade"),
                "DF"
            )

            registro = {

                "nome": nome,
                "descricao": self.input_descricao.text(),
                "logradouro": self.input_logradouro.text(),
                "numero": numero,
                "complemento": complemento,
                "bairro": self.input_bairro.text(),
                "cidade": cidade,
                "estado": "DF",
                "cep": None,
                "latitude": latitude,
                "longitude": longitude
            }

            self.funcao_disparar_evento("Chamada_enviada", registro)

        else:

            print("Dados incompletos")
            return