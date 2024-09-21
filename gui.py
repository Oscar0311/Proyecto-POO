from tkinter import Tk
from tkinter import Canvas
from tkinter import Entry
from tkinter import Label
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

        self.crear_entrada("Gravedad", self.simulacion.vector_g[1], self.set_gravedad)
        self.crear_entrada("Resistencia del Aire", self.simulacion.res_aire, self.set_resistencia_aire)
        self.crear_entrada("Temperatura", self.simulacion.temperatura, self.set_temperatura)
        self.crear_entrada("Fricción del Suelo", self.simulacion.friccion_suelo, self.set_friccion_suelo)
        
        
        self.escala_velocidad = tk.Scale(self.tk, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL, label="Velocidad de Simulación", command=self.set_velocidad)
        self.escala_velocidad.set(self.simulacion.velocidad)
        self.escala_velocidad.pack()


        self.foto=None

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

    def crear_entrada(self, texto_etiqueta, valor_inicial, comando):
        marco = tk.Frame(self.tk)
        marco.pack()
        etiqueta = Label(marco, text=texto_etiqueta)
        etiqueta.pack(side=tk.LEFT)
        entrada = Entry(marco)
        entrada.insert(0, str(valor_inicial))
        entrada.pack(side=tk.LEFT)
        entrada.bind("<Return>", lambda event: comando(entrada.get()))

    def ejecutar(self):
        x = true
        while x == True:
            if not self.simulacion.pausado:
                self.simulacion.actualizar()
            self.dibujar_particulas()
            self.tk.update_idletasks()
            self.tk.update()