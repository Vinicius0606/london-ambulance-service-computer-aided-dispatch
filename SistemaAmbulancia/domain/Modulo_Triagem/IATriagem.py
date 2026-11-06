from collections import deque
import json
import logging
import requests
from events.gerenciador_eventos import Gerenciador_eventos
from domain.Modulo_Ambulancia.ambulancia import Ambulancia
from PySide6.QtCore import QThread, Qt, Slot
from .tipos_escolher_ambulancia.interface_escolha_ambulancia import Interface_escolha_ambulancia
from .tipos_definir_prioridade.interface_definir_prioridade import Interface_definir_prioridade
from services.IA_Ollama.enviar_mensagem_IA import enviar_mensagem_IA

class IATriagem(QThread):

    def __init__(self, gerenciador_eventos: Gerenciador_eventos, ambulancias: list[Ambulancia],
                 tipo_escolher_ambulancia: Interface_escolha_ambulancia,
                 tipo_definir_prioridade: Interface_definir_prioridade):
        super().__init__()
        self.gerenciador_eventos = gerenciador_eventos
        self.ambulancias = ambulancias
        self.tipo_escolher_ambulancia = tipo_escolher_ambulancia
        self.tipo_definir_prioridade = tipo_definir_prioridade
        self.fila = deque()
        self.solicitacao_atual = None
        self.resultado = None

        self.gerenciador_eventos.adicionar_ouvinte_para_evento(
            "Triagem_iniciada", self.enfileirar_solicitacao,
        )
        self.finished.connect(self.finalizar_solicitacao, Qt.ConnectionType.QueuedConnection)

    def enfileirar_solicitacao(self, dados_da_ocorrencia):
        self.fila.append(dados_da_ocorrencia.copy())
        self.processar_proxima()

    def processar_proxima(self):
        if self.solicitacao_atual is not None or not self.fila:
            return

        self.solicitacao_atual = self.fila.popleft()
        self.gerenciador_eventos.emitir_evento(
            "Triagem_Thread_IA", {"triagem_id": self.solicitacao_atual["triagem_id"]},
        )
        self.start()

    def run(self):
        solicitacao = self.solicitacao_atual
        try:
            self.resultado = self.extrair_ocorrencia(solicitacao)
        except Exception:
            logging.getLogger(__name__).exception("Falha no processamento da triagem.")
            self.resultado = {
                "triagem_id": solicitacao["triagem_id"],
                "erro": "Não foi possível concluir a triagem desta chamada.",
            }

    @Slot()
    def finalizar_solicitacao(self):
        self.wait()
        try:
            self.gerenciador_eventos.emitir_evento("Triagem_concluida", self.resultado)
        finally:
            self.resultado = None
            self.solicitacao_atual = None
            self.processar_proxima()

    def extrair_ocorrencia(self, solicitacao):
        mensagem = solicitacao["ocorrencia"]

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

        # resposta = enviar_mensagem_IA(prompt)

        # texto = resposta["message"]["content"]

        # inicio = texto.find("{")

        # fim = texto.rfind("}") + 1

        # texto = texto[inicio:fim]

        texto = {
            "tipo_ocorrencia": "mal_súbito",
            "quantidade_vitimas": 1,
            "inconsciente": True,
            "respira": False,
            "sangramento_intenso": False,
            "dificuldade_respiratoria": False,
            "suspeita_trauma": False,
            "idade": None
            }

        ocorrencia = texto #json.loads(texto)

        prioridade = self.tipo_definir_prioridade.definir_prioridade(ocorrencia)

        qtd_ambulancias_solicitada = ocorrencia["quantidade_vitimas"]
        ambulancia_info = self.tipo_escolher_ambulancia.escolher_ambulancias(
            self.ambulancias, qtd_ambulancias_solicitada,
            solicitacao["latitude_do_chamado"], solicitacao["longitude_do_chamado"],
        )

        qtd_ambulancias = ambulancia_info["qtd_ambulancias"]

        ambulancias = ambulancia_info["ambulancias"]

        return {
            "triagem_id": solicitacao["triagem_id"],
            "prioridade": prioridade,
            "qtd_ambulancias": qtd_ambulancias,
            "qtd_ambulancias_solicitada": qtd_ambulancias_solicitada,
            "ambulancias": ambulancias
        }