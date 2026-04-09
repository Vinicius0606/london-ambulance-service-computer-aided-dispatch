import sys
from PySide6.QtWidgets import QApplication
from domain.Modulo_Mapa.mapa import Mapa
from domain.Modulo_Banco_Dados.conexao_BD import Conexao_BD
from ui.gerenciador_telas import Gerenciador_telas


app = QApplication(sys.argv)

banco_de_dados = Conexao_BD()

ambulancias = banco_de_dados.retornar_ambulancias()

chamadas_pendetes = banco_de_dados.retornar_chamadas_pendentes()

mapa_tela_Principal = Mapa(ambulancias)
mapa_tela_mapa = Mapa(ambulancias)

Gerenciador_telas = Gerenciador_telas(mapa_tela_Principal, mapa_tela_mapa)

for chamada in chamadas_pendetes:
    
    Gerenciador_telas.tela_principal.adicionarCard(chamada.nome_solicitante, 10, chamada.endereco.logradouro, chamada.horaChamada)

Gerenciador_telas.abrir_tela_principal()

sys.exit(app.exec())