import ollama
import json
import requests
from events.gerenciador_eventos import Gerenciador_eventos
from domain.Modulo_Ambulancia.ambulancia import Ambulancia
from PySide6.QtCore import QThread, Signal
from .tipos_escolher_ambulancia.interface_escolha_ambulancia import Interface_escolha_ambulancia
from .tipos_definir_prioridade.interface_definir_prioridade import Interface_definir_prioridade

class IATriagem(QThread):
    triagem_pronta = Signal(dict)

    def __init__(self, gerenciador_eventos: Gerenciador_eventos, ambulancias: list[Ambulancia], 
                 tipo_escolher_ambulancia: Interface_escolha_ambulancia, tipo_definir_prioridade: Interface_definir_prioridade):
        
        super().__init__()

        self.triagem = None

        self.ocorrencia = None

        self.latitude_do_chamado = None

        self.longitude_do_chamado = None

        self.gerenciador_eventos = gerenciador_eventos

        self.ambulancias = ambulancias

        self.tipo_escolher_ambulancia = tipo_escolher_ambulancia
        self.tipo_definir_prioridade = tipo_definir_prioridade

        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Triagem_iniciada", self.atualizar_ocorrencia)
        self.triagem_pronta.connect(self.enviar_finilizacao_thread)

    def enviar_finilizacao_thread(self, triagem_dict: dict):

        self.gerenciador_eventos.emitir_evento("Triagem_concluida", triagem_dict)

    def atualizar_ocorrencia(self, dados_da_ocorrencia):

        self.ocorrencia = dados_da_ocorrencia["ocorrencia"]
        self.latitude_do_chamado = dados_da_ocorrencia["latitude_do_chamado"]
        self.longitude_do_chamado = dados_da_ocorrencia["longitude_do_chamado"]

        self.gerenciador_eventos.emitir_evento("Triagem_Thread_IA")

    def run(self):

        self.extrair_ocorrencia(self.ocorrencia)
        

    def extrair_ocorrencia(self, mensagem):

        prompt = f"""
        Extraia as informações da ocorrência e responda apenas em JSON.

        Mensagem Exemplo 1:
        "Meu pai está vomitando e tonto"
        Resposta:
        {{
        "tipo_ocorrencia": "mal_súbito",
        "quantidade_vitimas": 1,
        "inconsciente": false,
        "respira": true,
        "sangramento_intenso": false,
        "dificuldade_respiratoria": false,
        "suspeita_trauma": false,
        "idade": null
        }}

        Mensagem Exemplo 2:
        "Eu sou deficiente, tenho 67 anos, e não tem ninguém para me levar na minha consulta poderiam me ajudar"
        Resposta:
        {{
        "tipo_ocorrencia": "transporte",
        "quantidade_vitimas": 0,
        "inconsciente": false,
        "respira": true,
        "sangramento_intenso": false,
        "dificuldade_respiratoria": false,
        "suspeita_trauma": false,
        "idade": 67
        }}

        Mensagem:
        {mensagem}
        """

        # resposta = ollama.chat(
        #     model="qwen3:8b",
        #     messages=[
        #         {"role": "user", "content": prompt}
        #     ]
        # )

        # texto = resposta["message"]["content"]

        # inicio = texto.find("{")

        # fim = texto.rfind("}") + 1

        # texto = texto[inicio:fim]

        texto = {
            "tipo_ocorrencia": "mal_súbito",
            "quantidade_vitimas": 2,
            "inconsciente": True,
            "respira": False,
            "sangramento_intenso": False,
            "dificuldade_respiratoria": False,
            "suspeita_trauma": False,
            "idade": None
            }

        ocorrencia = texto #json.loads(texto)

        prioridade = self.tipo_definir_prioridade.definir_prioridade(ocorrencia)

        ambulancia_info = self.tipo_escolher_ambulancia.escolher_ambulancias(self.ambulancias, ocorrencia["quantidade_vitimas"], 
                                                                             self.latitude_do_chamado, self.longitude_do_chamado)

        qtd_ambulancias = ambulancia_info["qtd_ambulancias"]

        ambulancias = ambulancia_info["ambulancias"]

        triagem_dict = {
            "prioridade": prioridade,
            "qtd_ambulancias": qtd_ambulancias,
            "ambulancias": ambulancias
        }

        self.triagem_pronta.emit(triagem_dict)