import ollama
import json
from events.gerenciador_eventos import Gerenciador_eventos
from PySide6.QtCore import QThread, Signal

class IATriagem(QThread):
    triagem_pronta = Signal(dict)

    def __init__(self, gerenciador_eventos: Gerenciador_eventos):
        
        super().__init__()

        self.triagem = None

        self.ocorrencia = None

        self.gerenciador_eventos = gerenciador_eventos

        self.gerenciador_eventos.adicionar_ouvinte_para_evento("Triagem_iniciada", self.atualizar_ocorrencia)
        self.triagem_pronta.connect(self.enviar_finilizacao_thread)

    def enviar_finilizacao_thread(self, triagem_dict: dict):

        self.gerenciador_eventos.emitir_evento("Triagem_concluida", triagem_dict)

    def atualizar_ocorrencia(self, ocorrencia):

        self.ocorrencia = ocorrencia

        self.gerenciador_eventos.emitir_evento("Triagem_Thread_IA")

    def run(self):

        self.extrairOcorrencia(self.ocorrencia)
        

    def extrairOcorrencia(self, mensagem):

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

        resposta = ollama.chat(
            model="qwen3:8b",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        texto = resposta["message"]["content"]

        print(texto)

        inicio = texto.find("{")

        fim = texto.find("}") + 1

        texto = texto[inicio:fim]

        print(texto)

        texto = json.loads(texto)

        self.analisarOcorrencia(texto)

    def analisarOcorrencia(self, ocorrencia: dict):
        pontuacao = 0
        justificativa = []
        resultado = {}

        if not ocorrencia["respira"]:

            pontuacao = 90
            justificativa.append("parada respiratoria")

        elif ocorrencia["sangramento_intenso"]:

            pontuacao = 90
            justificativa.append("sangramento intenso")
      
        elif ocorrencia["quantidade_vitimas"] >= 2 and ocorrencia["suspeita_trauma"]:
            pontuacao = 90
            justificativa.append(f"{ocorrencia['quantidade_vitimas']} vitimas e suspeita de trauma")

        if ocorrencia["suspeita_trauma"]:
            pontuacao += 60
            justificativa.append("suspeita de trauma")
        
        if ocorrencia["inconsciente"]:
            pontuacao += 50
            justificativa.append("vitima inconsciente")
        
        if ocorrencia["dificuldade_respiratoria"]:

            pontuacao += 40
            justificativa.append("Dificuldade respiratoria")

        if ocorrencia["quantidade_vitimas"] >= 2:
            pontuacao += 30
            justificativa.append(f"{ocorrencia['quantidade_vitimas']} vitimas")

        elif ocorrencia["quantidade_vitimas"] == 1:
            pontuacao += 20
            justificativa.append("1 vitima")

        else:
            pontuacao += 10
            justificativa.append("Transporte de incapacitado")
        
        resultado = {
            "pontuacao": pontuacao,
            "justificativa": justificativa
        }

        prioridade = self.definirPrioridade(resultado)

        ambulancia_info = self.calcularQuantidadeAmbulancias(ocorrencia["quantidade_vitimas"], prioridade)

        qtd_ambulancias = ambulancia_info["qtdAmbulancias"]

        ambulancias = ambulancia_info["ambulancia"]

        triagem_dict = {
            "prioridade": prioridade,
            "qtd_ambulancias": qtd_ambulancias,
            "ambulancias": ambulancias
        }

        self.triagem_pronta.emit(triagem_dict)

    def definirPrioridade(self, resultado_triagem: dict):

        prioridade = 0
        
        if resultado_triagem["pontuacao"] <= 10:
            prioridade = 1

        elif resultado_triagem["pontuacao"] > 10   and resultado_triagem["pontuacao"] < 60:
            prioridade = 2

        elif resultado_triagem["pontuacao"] >= 60 and resultado_triagem["pontuacao"] < 90:
            prioridade = 3

        else:
            prioridade = 4

        return prioridade


    def calcularQuantidadeAmbulancias(self, qtdVitimas: int, prioridade: str):
        
        ambulancias = ["Basica", "Avancada"]
        qtdAmbulancias = 0

        if qtdVitimas < 4:
            qtdAmbulancias = qtdVitimas
        else:
            qtdAmbulancias = 4

        if prioridade == 1 or prioridade == 2:
                
            return{
                "ambulancia": ambulancias[0],
                "qtdAmbulancias": qtdAmbulancias
            }
            
        elif prioridade == 3 or prioridade == 4:

            return{
                "ambulancia": ambulancias[1],
                "qtdAmbulancias": qtdAmbulancias
            }

    def buscarAmbulanciasProximas():
        pass