from tkinter import Tk, Canvas, Entry, Label, Button, Frame
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
        self.lienzo.pack(side=tk.LEFT)

        self.controles = Frame(self.tk)
        self.controles.pack(side=tk.RIGHT, fill=tk.Y)

        self.crear_entrada("Gravedad (m/s^2)", self.simulacion.vector_g[1], self.set_gravedad)
        self.crear_entrada("Resistencia del Aire", self.simulacion.res_aire, self.set_resistencia_aire)
        self.crear_entrada("Temperatura (K)", self.simulacion.temperatura, self.set_temperatura)
        self.crear_entrada("Fricción del Suelo", self.simulacion.friccion_suelo, self.set_friccion_suelo)
        
        self.escala_velocidad = tk.Scale(self.controles, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL, label="Velocidad de Simulación", command=self.set_velocidad)
        self.escala_velocidad.set(self.simulacion.velocidad)
        self.escala_velocidad.pack()

        self.boton_pausa = Button(self.controles, text="Pausar", command=self.toggle_pausa)
        self.boton_pausa.pack()

        self.foto = None

        self.modo_mouse = tk.StringVar(value="Agregar Partículas")
        opciones_modo = ["Agregar Partículas", "Mover Partículas"]
        self.menu_modo = tk.OptionMenu(self.controles, self.modo_mouse, *opciones_modo)
        self.menu_modo.pack()

        self.propiedades_particulas = Frame(self.tk)
        self.propiedades_particulas.pack(side=tk.RIGHT, fill=tk.Y)

        self.crear_entrada_propiedad("Radio", 4, self.set_radio)
        self.crear_entrada_propiedad("Masa", 1, self.set_masa)
        self.crear_entrada_propiedad("Rebote", 0.7, self.set_rebote)

        self.radio = 4
        self.masa = 1
        self.rebote = 0.7

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

    def set_radio(self, valor):
        self.radio = int(valor)

    def set_masa(self, valor):
        self.masa = float(valor)

    def set_rebote(self, valor):
        self.rebote = float(valor)

    def toggle_pausa(self):
        self.simulacion.pausado = not self.simulacion.pausado
        self.boton_pausa.config(text="Reanudar" if self.simulacion.pausado else "Pausar")

    def dibujar_particulas(self):
        imagen = np.full((self.simulacion.alto, self.simulacion.ancho, 3), [255, 255, 255], dtype=np.uint8)
        
        for particula in self.simulacion.particulas:
            cv2.circle(imagen, (int(particula.x), int(particula.y)), particula.radio, particula.color, -1)
        
        self.foto = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(imagen))
        self.lienzo.create_image(0, 0, image=self.foto, anchor=tk.NW)

    def crear_entrada(self, texto_etiqueta, valor_inicial, comando):
        marco = tk.Frame(self.controles)
        marco.pack()
        etiqueta = Label(marco, text=texto_etiqueta)
        etiqueta.pack(side=tk.LEFT)
        entrada = Entry(marco)
        entrada.insert(0, str(valor_inicial))
        entrada.pack(side=tk.LEFT)
        entrada.bind("<Return>", lambda event: comando(entrada.get()))

    def agregar_particula_mouse(self, event):
        x, y = event.x, event.y
        self.simulacion.agregar_particula(x,y)

    def ejecutar(self):
        self.lienzo.bind("<Button-1>", self.manejar_clic_izquierdo)
        self.lienzo.bind("<B1-Motion>", self.arrastrar_particula)
        self.lienzo.bind("<ButtonRelease-1>", self.finalizar_arrastre)
        ejecutando = True
        while ejecutando:
            if not self.simulacion.pausado:
                self.simulacion.actualizar()
            self.dibujar_particulas()
            self.tk.update_idletasks()
            self.tk.update()
