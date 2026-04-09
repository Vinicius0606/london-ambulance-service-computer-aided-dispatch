from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtCore import QUrl
from ..Modulo_Ambulancia.ambulancia import Ambulancia
import sys
import os
import time

class Mapa:

    def __init__(self, ambulancias: list[Ambulancia]):
        self.ambulancias: list[Ambulancia] = ambulancias
        self.atendimentos = None

        self.mapa_web = QWebEngineView()

        self.mapa_web.load(QUrl("http://127.0.0.1:8000/mapa.html"))
        self.mapa_web.resize(1000, 700)

        self.mapa_web.loadFinished.connect(self.codigo_mapa_carregado)
    
    def codigo_mapa_carregado(self):

        for index, ambulancia in enumerate(self.ambulancias):

            self.mapa_web.page().runJavaScript(
                f"""adicionar_ambulancia({ambulancia.id}, {ambulancia.latitudeAtual}, 
                {ambulancia.longitudeAtual}, '{ambulancia.status}')"""
            )
        

    def adicionarAmbulancias(self, ambulancia: Ambulancia):
        
        self.ambulancias.push(ambulancia)

        self.mapa_web.page().runJavaScript(
            f"adicionar_ambulancia({ambulancia.id}, {ambulancia.latitudeAtual}, {ambulancia.longitudeAtual}, '{ambulancia.status}')"
        )

    def exibirAtendimentos():
        pass

    def exibirRotas():
        pass

    def retornar_mapa_QWidget(self):

        if(self.mapa_web): return self.mapa_web