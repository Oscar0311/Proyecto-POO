from tkinter import Tk
from tkinter import Canvas
import tkinter as tk
import numpy as np
import cv2
import PIL.Image, PIL.ImageTk

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

    def dibujar_particulas(self):
        imagen = np.full((self.simulacion.alto, self.simulacion.ancho, 3), [255, 255, 255], dtype=np.uint8)
        
        for particula in self.simulacion.particulas:
            cv2.circle(imagen, (int(particula.x), int(particula.y)), particula.radio, particula.color, -1)
        
        self.foto = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(imagen))
        self.lienzo.create_image(0, 0, image=self.foto, anchor=tk.NW)