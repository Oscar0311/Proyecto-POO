from tkinter import Tk
from tkinter import Canvas

class Interfaz:
    def __init__(self, simulacion):
        self.simulacion = simulacion
        self.tk = Tk()
        self.tk.title("Simulación de Partículas")

        self.lienzo = Canvas(self.tk, width=self.simulacion.ancho, height=self.simulacion.alto)
        self.lienzo.pack()