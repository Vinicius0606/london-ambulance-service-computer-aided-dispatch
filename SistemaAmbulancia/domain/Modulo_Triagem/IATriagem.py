import ollama
import json
import requests
from events.gerenciador_eventos import Gerenciador_eventos
from domain.Modulo_Ambulancia.ambulancia import Ambulancia
from PySide6.QtCore import QThread, Signal

class IATriagem(QThread):
    triagem_pronta = Signal(dict)

    def __init__(self, gerenciador_eventos: Gerenciador_eventos, ambulancias: list[Ambulancia]):
        
        super().__init__()

        self.triagem = None

        self.ocorrencia = None

        self.latitude_do_chamado = None

        self.longitude_do_chamado = None

        self.gerenciador_eventos = gerenciador_eventos

        self.ambulancias = ambulancias

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

        resposta = ollama.chat(
            model="qwen3:8b",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        texto = resposta["message"]["content"]

        inicio = texto.find("{")

        fim = texto.rfind("}") + 1

        texto = texto[inicio:fim]

        print(texto)

        texto = json.loads(texto)

        self.analisar_ocorrencia(texto)

    def analisar_ocorrencia(self, ocorrencia: dict):
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

        prioridade = self.definir_prioridade(resultado)

        ambulancia_info = self.denifir_ambulancias_para_ocorrencia(ocorrencia["quantidade_vitimas"])

        qtd_ambulancias = ambulancia_info["qtd_ambulancias"]

        ambulancias = ambulancia_info["ambulancia"]

        triagem_dict = {
            "prioridade": prioridade,
            "qtd_ambulancias": qtd_ambulancias,
            "ambulancias": ambulancias
        }

        self.triagem_pronta.emit(triagem_dict)

    def definir_prioridade(self, resultado_triagem: dict):

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


    def denifir_ambulancias_para_ocorrencia(self, qtd_vitimas: int):
        
        menor_distancia_pro_chamado: float = 30 #Raio de operacao do sistema acrescentado em 10

        escolha_de_ambulancia = []

        if qtd_vitimas < 4 :
            qtd_ambulancias = qtd_vitimas

        elif qtd_vitimas >= 4:
            qtd_ambulancias = 4

        aux_qtd_ambulancias = qtd_ambulancias

        while aux_qtd_ambulancias > 0:

            for ambulancia in self.ambulancias:

                distancia = self.buscar_ambulancias_proximas([ambulancia.latitudeAtual, ambulancia.longitudeAtual])

                if distancia["distancia_km"] < menor_distancia_pro_chamado and ambulancia not in escolha_de_ambulancia: 
                    menor_distancia_pro_chamado = distancia["distancia_km"]
                    escolha_de_ambulancia.clear()
                    escolha_de_ambulancia.append(ambulancia)
            
            aux_qtd_ambulancias -= 1

  
        return{
            "ambulancia": escolha_de_ambulancia,
            "qtd_ambulancias": qtd_ambulancias
        }

    def buscar_ambulancias_proximas(self, posicao_ambulancia):
        
        
        url = (
            f"https://router.project-osrm.org/route/v1/driving/"
            f"{posicao_ambulancia[1]},{posicao_ambulancia[0]};{self.longitude_do_chamado},{self.latitude_do_chamado}"
            f"?overview=full&geometries=geojson"
        )

        resposta = requests.get(url)
        resposta.raise_for_status()

        dados = resposta.json()

        if not dados.get("routes"):
            return None

        rota = dados["routes"][0]

        return {
            "distancia_metros": rota["distance"],
            "distancia_km": rota["distance"] / 1000,
        }
