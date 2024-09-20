from tkinter import Tk
from tkinter import Canvas

class Interfaz:
    def __init__(self, simulacion):
        self.simulacion = simulacion
        self.tk = Tk()
        self.tk.title("Simulación de Partículas")

        self.lienzo = Canvas(self.tk, width=self.simulacion.ancho, height=self.simulacion.alto)
        self.lienzo.pack()

    def set_gravedad(self, valor):
        self.simulacion.vector_g[1] = float(valor)

    def set_resistencia_aire(self, valor):
        self.simulacion.res_aire = float(valor)

    def set_temperatura(self, valor):
        self.simulacion.temperatura = float(valor)

    def set_friccion_suelo(self, valor):
        self.simulacion.friccion_suelo = float(valor)

    def set_velocidad(self, valor):
        self.simulacion.velocidad = float(valor)