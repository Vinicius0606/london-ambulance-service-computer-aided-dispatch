import pymysql
from domain.Modulo_Ambulancia.ambulancia import Ambulancia
from domain.Modulo_Chamada.chamada import Chamada
from domain.Modulo_Chamada.endereco import Endereco
from domain.Modulo_Ambulancia.atendimento import Atendimento
from domain.Modulo_Ambulancia.despacho import Despacho
from domain.Modulo_Chamada.status import Status
from events.gerenciador_eventos import Gerenciador_eventos

class Conexao_BD:

    def __init__(self, gerenciador_eventos: Gerenciador_eventos):

        self.conexao = pymysql.connect(
            host="localhost",
            user="root",
            password="123",
            database="sistema_ambulancia",
            port=3306
        )

        self.cursor = self.conexao.cursor()

        self.gerenciador_eventos = gerenciador_eventos

        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Armazenar_endereco_Banco_dados", self.insert)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Armazenar_chamada_Banco_dados", self.insert)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Armazenar_atendimento_Banco_dados", self.insert)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Armazenar_despacho_Banco_dados", self.insert)

        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Atualizar_chamada_Banco_dados", self.update)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Atualizar_atendimento_Banco_dados", self.update)
        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Atualizar_despacho_Banco_dados", self.update)

    def retornar_ambulancias(self):

        cursor = self.cursor
        
        sql = "SELECT ID_ambulancia, placa, latitude, longitude, status FROM ambulancia"

        cursor.execute(sql)

        ambulancias_resultado = cursor.fetchall()

        ambulancias_lista: list[Ambulancia] = []

        for ambulancia in ambulancias_resultado:
            
            print

            ambulancia_objeto = Ambulancia(ambulancia[0], ambulancia[1], ambulancia[2], ambulancia[3],
                                           self.gerenciador_eventos, status=ambulancia[4])


            ambulancias_lista.append(ambulancia_objeto)

        return ambulancias_lista
    
    def retornar_chamadas(self):
    
        cursor = self.cursor
        
        sql = """SELECT c.ID_chamada, c.nome_solicitante, c.descricao, c.hora_chamada, c.prioridade, c.status , e.ID_endereco, e.CEP, 
            e.logradouro, e.bairro, e.cidade, e.estado, e.latitude, e.longitude, e.complemento, e.numero 
            FROM chamada c left join endereco e on c.ID_endereco = e.ID_endereco"""

        cursor.execute(sql)

        chamadas_resultado = cursor.fetchall()

        chamadas_lista: list[Chamada] = []

        for chamada in chamadas_resultado:

            endereco_objeto = Endereco(chamada[7], chamada[8], chamada[9], 
                                       chamada[10], chamada[11], chamada[12], chamada[13], chamada[14], chamada[15])

            chamada_objeto = Chamada(endereco_objeto ,chamada[2], self.gerenciador_eventos, chamada[3], 
                                id=chamada[0], prioridade=chamada[4], nome_solicitante=chamada[1], status=chamada[5], 
                                veio_do_banco_de_dados=True)

            chamadas_lista.append(chamada_objeto)

        return chamadas_lista
    
    def retornar_atendimentos(self, chamadas: list[Chamada], ambulancias: list[Ambulancia]):
        chamadas_por_id = {chamada.id: chamada for chamada in chamadas}
        ambulancias_por_id = {ambulancia.id: ambulancia for ambulancia in ambulancias}

        sql = """
            SELECT a.ID_atendimento, a.ID_chamada, a.qtd_ambulancias, a.data_hora_inicio,
                   aa.ID_atendimento_ambulancia, aa.ID_ambulancia, aa.data_hora_envio,
                   aa.data_hora_chegada, aa.status, aa.observacoes
            FROM atendimento a
            INNER JOIN chamada c ON c.ID_chamada = a.ID_chamada
            LEFT JOIN atendimento_ambulancia aa ON aa.ID_atendimento = a.ID_atendimento
            WHERE a.data_hora_finalizacao IS NULL
              AND (c.status IS NULL OR c.status <> %s)
            ORDER BY a.ID_atendimento, aa.ID_atendimento_ambulancia
        """
        self.cursor.execute(sql, (Status.FINALIZADO.value,))

        atendimentos = {}
        for (
            id_atendimento, id_chamada, quantidade, hora_inicio, id_despacho,
            id_ambulancia, hora_envio, hora_chegada, status, observacoes,
        ) in self.cursor.fetchall():
            chamada = chamadas_por_id.get(id_chamada)
            if chamada is None:
                continue

            if id_atendimento not in atendimentos:
                atendimentos[id_atendimento] = Atendimento(
                    id_atendimento, chamada, quantidade, [], self.gerenciador_eventos,
                    hora_inicio=hora_inicio, veio_do_banco_de_dados=True,
                )

            ambulancia = ambulancias_por_id.get(id_ambulancia)
            if id_despacho is None or ambulancia is None:
                continue

            atendimento = atendimentos[id_atendimento]
            despacho = Despacho(
                id_despacho, chamada, ambulancia, self.gerenciador_eventos,
                observacoes=observacoes, veio_do_banco_de_dados=True,
                id_atendimento=id_atendimento, hora_inicio=hora_envio,
                hora_chegada=hora_chegada, status=status,
            )
            atendimento.despachos.append(despacho)
            if ambulancia not in atendimento.ambulancias_alocadas:
                atendimento.ambulancias_alocadas.append(ambulancia)

        return list(atendimentos.values())

    def update(self, novos_valores: dict):

        cursor = self.cursor

        colunas_para_alterar = {}

        for coluna, valor in novos_valores.items():
            
            if coluna == "tabela" or coluna == "ID": continue

            if valor is not None: colunas_para_alterar[coluna] = valor


        clausulas = ", ".join([f"{coluna} = %s" for coluna in colunas_para_alterar.keys()])
        valores = list(colunas_para_alterar.values())

        sql = f"UPDATE {novos_valores['tabela']} SET {clausulas} WHERE ID_{novos_valores['tabela']} = {novos_valores['ID']}"

        cursor.execute(sql, valores)

        self.conexao.commit()

    def insert(self, novos_valores: dict):

        cursor = self.cursor

        colunas_para_inserir = {}

        for coluna, valor in novos_valores.items():

            if coluna == "tabela" or coluna == "objeto": continue
            
            if valor is not None: colunas_para_inserir[coluna] = valor


        colunas = ", ".join(colunas_para_inserir.keys())

        placeholders = ", ".join(["%s"] * len(colunas_para_inserir))

        valores = list(colunas_para_inserir.values())

        sql = f"INSERT INTO {novos_valores['tabela']} ({colunas}) VALUES ({placeholders})"

        cursor.execute(sql, valores)

        novos_valores["objeto"].atualizar_ID(cursor.lastrowid)

        self.conexao.commit()

        