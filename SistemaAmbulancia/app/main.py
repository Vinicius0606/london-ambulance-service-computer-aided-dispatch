import sys
from PySide6.QtWidgets import QApplication
from domain.Modulo_Mapa.mapa import Mapa
from domain.Modulo_Banco_Dados.conexao_BD import Conexao_BD
from ui.main_window import Janela_principal


app = QApplication(sys.argv)

banco_de_dados = Conexao_BD()

ambulancias = banco_de_dados.retornar_ambulancias()

chamadas_pendetes = banco_de_dados.retornar_chamadas_pendentes()

mapa = Mapa(ambulancias)

tela_principal = Janela_principal(mapa)

for chamada in chamadas_pendetes:
    
    tela_principal.adicionarCard(chamada.nome_solicitante, 10, chamada.endereco.logradouro, chamada.horaChamada)

tela_principal.showMaximized()

sys.exit(app.exec())