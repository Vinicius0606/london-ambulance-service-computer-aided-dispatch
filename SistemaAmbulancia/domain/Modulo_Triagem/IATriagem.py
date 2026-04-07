from triagem import Triagem
import ollama
import json

class IATriagem:

    def __init__(self):
        self.triagem = None

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
        "idade": None
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

        return json.loads(texto)

    def analisarOcorrencia(self, ocorrencia: dict):
        pontuacao = 0
        justificativa = []

        if not ocorrencia["respira"]:

            pontuacao = 90
            justificativa.append("parada respiratoria")

            return {

                "pontuacao": pontuacao,
                "justificativa": justificativa
            }
        
        if ocorrencia["sangramento_intenso"]:

            pontuacao = 90
            justificativa.append("sangramento intenso")

            return {

                "pontuacao": pontuacao,
                "justificativa": justificativa
            }
        
        if ocorrencia["quantidade_vitimas"] >= 2 and ocorrencia["suspeita_trauma"]:

            pontuacao = 90
            justificativa.append(f"{ocorrencia['quantidade_vitimas']} vitimas e suspeita de trauma")

            return {

                "pontuacao": pontuacao,
                "justificativa": justificativa
            } 
        
        elif ocorrencia["suspeita_trauma"]:
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

        return {

            "pontuacao": pontuacao,
            "justificativa": justificativa
        }

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