import pymysql
from ..Modulo_Ambulancia.ambulancia import Ambulancia
from ..Modulo_Chamada.chamada import Chamada
from ..Modulo_Chamada.endereco import Endereco

class Conexao_BD:

    def __init__(self):

        self.conexao = pymysql.connect(
            host="localhost",
            user="root",
            password="123",
            database="sistema_ambulancia",
            port=3306
        )

        self.cursor = self.conexao.cursor()

    def retornar_ambulancias(self):

        cursor = self.cursor
        
        sql = "SELECT ID_ambulancia, placa, tipo, latitude, longitude FROM ambulancia"

        cursor.execute(sql)

        ambulancias_resultado = cursor.fetchall()

        ambulancias_lista: list[Ambulancia] = []

        for ambulancia in ambulancias_resultado:

            ambulancia_objeto = Ambulancia(ambulancia[0], ambulancia[1], ambulancia[2])

            ambulancia_objeto.atualizarLocalizacao(ambulancia[3], ambulancia[4])

            ambulancias_lista.append(ambulancia_objeto)

        return ambulancias_lista
    
    def retornar_chamadas_pendentes(self):
    
        cursor = self.cursor
        
        sql = """SELECT c.ID_chamada, c.nome_solicitante, c.descricao, c.data_hora, e.ID_endereco, e.CEP, 
            e.logradouro, e.bairro, e.cidade, e.estado, e.latitude, e.longitude, e.complemento, e.numero 
            FROM chamada c left join endereco e on c.ID_endereco = e.ID_endereco
            WHERE c.status = 'Pendente'"""

        cursor.execute(sql)

        chamadas_resultado = cursor.fetchall()

        chamadas_lista: list[Chamada] = []

        for chamada in chamadas_resultado:

            endereco_objeto = Endereco(chamada[5], chamada[6], 
                                       chamada[7], chamada[8], chamada[9], chamada[10], chamada[11], chamada[12], chamada[13])

            chamada_objeto = Chamada(chamada[1], endereco_objeto ,chamada[2], chamada[3])

            chamadas_lista.append(chamada_objeto)

        return chamadas_lista