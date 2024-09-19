from tkinter import Tk

class Interfaz:
    def __init__(self, simulacion):
        self.simulacion = simulacion
        self.tk = Tk()
        self.tk.title("Simulación de Partículas")