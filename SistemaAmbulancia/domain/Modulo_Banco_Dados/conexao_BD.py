import pymysql
from ..Modulo_Ambulancia.ambulancia import Ambulancia
from ..Modulo_Chamada.chamada import Chamada
from ..Modulo_Chamada.endereco import Endereco
from ..Modulo_Ambulancia.atendimento import Atendimento
from datetime import datetime

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
    
    def retornar_chamadas(self):
    
        cursor = self.cursor
        
        sql = """SELECT c.ID_chamada, c.nome_solicitante, c.descricao, c.data_hora, c.prioridade , e.ID_endereco, e.CEP, 
            e.logradouro, e.bairro, e.cidade, e.estado, e.latitude, e.longitude, e.complemento, e.numero 
            FROM chamada c left join endereco e on c.ID_endereco = e.ID_endereco"""

        cursor.execute(sql)

        chamadas_resultado = cursor.fetchall()

        chamadas_lista: list[Chamada] = []

        for chamada in chamadas_resultado:

            endereco_objeto = Endereco(chamada[6], chamada[7], chamada[8], chamada[9], 
                                       chamada[10], chamada[11], chamada[12], chamada[13], chamada[14])

            chamada_objeto = Chamada(chamada[1], endereco_objeto ,chamada[2], chamada[3], id=chamada[0], prioridade=chamada[4])

            chamadas_lista.append(chamada_objeto)

        return chamadas_lista
    
    def retornar_atendimentos(self):

        cursor = self.cursor

        ambulancias = self.retornar_ambulancias()
        chamadas = self.retornar_chamadas()
        
        sql = """SELECT a.ID_atendimento, c.ID_chamada, a.qtd_ambulancias, a.data_hora_inicio 
                FROM atendimento a 
                LEFT JOIN chamada c ON a.ID_chamada = c.ID_chamada
                WHERE c.status != 'Finalizado';"""
        
        cursor.execute(sql)

        atendimentos_resultado = cursor.fetchall()

        sql = """SELECT a.ID_atendimento, aa.ID_ambulancia 
                FROM atendimento_ambulancia aa
                LEFT JOIN atendimento a ON aa.ID_atendimento = a.ID_atendimento
                LEFT JOIN ambulancia c ON aa.ID_ambulancia = c.ID_ambulancia;"""
        
        cursor.execute(sql)

        atendimentos_ambulancias_id = cursor.fetchall()
        
        lista_atendimentos: list[Atendimento] = []

        for atendimento in atendimentos_resultado:
            
            chamada_do_atendimento = next((chamada for chamada in chamadas if chamada.id == atendimento[1]), None)
            
            id_ambulancias_do_atendimento = [next((id[1] for id in atendimentos_ambulancias_id if id[0] == atendimento[0]))]

            ambulancias_do_atendimento = list(
                ambulancia for ambulancia in ambulancias if ambulancia.id in id_ambulancias_do_atendimento)

            if chamada_do_atendimento == None: continue

            atendimento_objeto = Atendimento(atendimento[0], chamada_do_atendimento, 
                                             atendimento[2], ambulancias_do_atendimento , 
                                             atendimento[3] if atendimento[3] != None else datetime.now())

            lista_atendimentos.append(atendimento_objeto)

        return lista_atendimentos