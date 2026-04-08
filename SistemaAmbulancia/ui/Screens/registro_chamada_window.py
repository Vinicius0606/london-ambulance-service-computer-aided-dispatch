from PySide6.QtWidgets import ( QApplication, QMainWindow, QPushButton, QWidget, 
QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QComboBox )
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize

class Registro_chamada_window(QMainWindow):
    def __init__(self):

        super().__init__()

        telaUsuarioTamanho = QApplication.instance().primaryScreen().size()

        self.larguraTela = telaUsuarioTamanho.width()
        self.alturaTela = telaUsuarioTamanho.height()

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
        botao_perfil.setIcon(QIcon("./assets/user.png"))
        botao_perfil.setIconSize(QSize(48,48))

        botao_mapa = QPushButton()
        botao_mapa.setIcon(QIcon("./assets/map.png"))
        botao_mapa.setIconSize(QSize(48,48))

        botao_sair = QPushButton()
        botao_sair.setIcon(QIcon("./assets/exit.png"))
        botao_sair.setIconSize(QSize(48,48))

        layout_menu_lateral.addWidget(botao_perfil, 1, alignment= Qt.AlignTop)
        layout_menu_lateral.addWidget(botao_mapa, 30, alignment= Qt.AlignTop)
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

        label_nome = QLabel("Nome")
        label_nome.setStyleSheet("margin-left: 5px;")

        input_nome = QLineEdit()
        input_nome.setPlaceholderText("Nome")
        input_nome.setStyleSheet("""
            background-color: #242735;
            border-radius: 10px;
            padding: 15px 10px;
        """)

        label_descricao = QLabel("Descrição")
        label_descricao.setStyleSheet("margin-left: 5px;")

        input_descricao = QLineEdit()
        input_descricao.setPlaceholderText("Descrição")
        input_descricao.setStyleSheet("""
            background-color: #242735;
            border-radius: 10px;
            padding: 15px 10px;
        """)
        input_descricao.setFixedHeight(self.alturaTela / 4)
        input_descricao.setAlignment(Qt.AlignTop)

        layout.addWidget(label_nome, 1, alignment=Qt.AlignLeft)
        layout.addWidget(input_nome, 2, alignment=Qt.AlignTop)
        layout.addWidget(label_descricao, 1, alignment=Qt.AlignLeft)
        layout.addWidget(input_descricao, 10, alignment=Qt.AlignTop)

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

        label_CEP = QLabel("CEP")

        input_CEP = QLineEdit()
        input_CEP.setPlaceholderText("NNNNN-NNN")
        input_CEP.setStyleSheet("""
            background-color: #222635;
            border-radius: 10px;
            padding: 15px 10px;
        """)

        label_logradouro = QLabel("logradouro")

        input_logradouro = QLineEdit()
        input_logradouro.setPlaceholderText("Logradouro")
        input_logradouro.setStyleSheet("""
            background-color: #222635;
            border-radius: 10px;
            padding: 15px 10px;
        """)

        label_numero = QLabel("Número")

        input_numero = QLineEdit()
        input_numero.setPlaceholderText("Número")
        input_numero.setStyleSheet("""
            background-color: #222635;
            border-radius: 10px;
            padding: 15px 10px;
        """)

        label_cidade_estado = QLabel("Cidade / Estado")

        div_cidade_estado = QWidget()

        layout_div_cidade_estado = QHBoxLayout()

        input_cidade = QComboBox()
        input_cidade.setStyleSheet("""
            QComboBox {
                background-color: #222635;
                padding: 10px 20px;
            }
                                   
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }

            QComboBox::down-arrow {
                image: url(./assets/angulo-para-baixo.png);
                width: 12px;
                height: 12px;
            }
        """)

        input_cidade.addItem("DF")
        input_cidade.addItem("AA")
        input_cidade.addItem("BB")
        input_cidade.addItem("CC")
        input_cidade.addItem("DD")

        input_estado = QComboBox()
        input_estado.setStyleSheet("""
            QComboBox {
                background-color: #222635;
                padding: 10px 20px;
            }
                                   
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }

            QComboBox::down-arrow {
                image: url(./assets/angulo-para-baixo.png);
                width: 12px;
                height: 12px;
            }
        """)

        input_estado.addItem("AA")
        input_estado.addItem("BB")
        input_estado.addItem("CC")
        input_estado.addItem("DD")
        input_estado.addItem("FF")

        layout_div_cidade_estado.addWidget(input_cidade)
        layout_div_cidade_estado.addWidget(input_estado)

        div_cidade_estado.setLayout(layout_div_cidade_estado)

        label_complemento = QLabel("Complemento (opcional)")

        input_complemento = QLineEdit()
        input_complemento.setPlaceholderText("Complemento")
        input_complemento.setStyleSheet("""
            background-color: #222635;
            border-radius: 10px;
            padding: 15px 10px;
        """)

        layout_inputs.addWidget(label_CEP, 1, alignment=Qt.AlignTop)
        layout_inputs.addWidget(input_CEP, 4, alignment=Qt.AlignTop)
        layout_inputs.addWidget(label_logradouro, 1, alignment=Qt.AlignTop)
        layout_inputs.addWidget(input_logradouro, 4, alignment=Qt.AlignTop) 
        layout_inputs.addWidget(label_numero, 1, alignment=Qt.AlignTop)
        layout_inputs.addWidget(input_numero, 4, alignment=Qt.AlignTop) 
        layout_inputs.addWidget(label_cidade_estado, 1, alignment=Qt.AlignTop)
        layout_inputs.addWidget(div_cidade_estado, 4, alignment=Qt.AlignTop) 
        layout_inputs.addWidget(label_complemento, 1, alignment=Qt.AlignTop)
        layout_inputs.addWidget(input_complemento, 4, alignment=Qt.AlignTop) 

        div_inputs.setLayout(layout_inputs)

        layout_principal.addWidget(label_titulo, 1)
        layout_principal.addWidget(div_inputs, 19)

        div_principal.setLayout(layout_principal)

        return div_principal