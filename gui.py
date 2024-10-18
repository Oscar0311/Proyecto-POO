from tkinter import Tk, Canvas, Entry, Label, Button, Frame
import tkinter as tk
import numpy as np
import cv2
import PIL.Image, PIL.ImageTk

class Interfaz:
    def __init__(self, simulacion):
        self.__simulacion = simulacion
        self.__tk = Tk()
        self.__tk.title("Simulación de Partículas")

        self.__lienzo = Canvas(self.__tk, width=self.__simulacion.get_ancho(), height=self.__simulacion.get_alto())
        self.__lienzo.pack(side=tk.LEFT)

        self.__controles = Frame(self.__tk)
        self.__controles.pack(side=tk.RIGHT, fill=tk.Y)

        self.crear_entrada("Gravedad (m/s^2)", self.__simulacion.get_vector_g()[1], self.set_gravedad)
        self.crear_entrada("Resistencia del Aire", self.__simulacion.get_res_aire(), self.set_resistencia_aire)
        self.crear_entrada("Temperatura (K)", self.__simulacion.get_temperatura(), self.set_temperatura)
        self.crear_entrada("Fricción del Suelo", self.__simulacion.get_friccion_suelo(), self.set_friccion_suelo)

        self.__boton_pausa = Button(self.__controles, text="Pausar", command=self.toggle_pausa)
        self.__boton_pausa.pack()

        self.__foto = None

        self.__modo_mouse = tk.StringVar(value="Agregar Partículas")
        opciones_modo = ["Agregar Partículas", "Mover Partículas"]
        self.__menu_modo = tk.OptionMenu(self.__controles, self.__modo_mouse, *opciones_modo)
        self.__menu_modo.pack()

        self.__propiedades_particulas = Frame(self.__tk)
        self.__propiedades_particulas.pack(side=tk.RIGHT, fill=tk.Y)

        self.crear_entrada_propiedad("Radio", 4, self.set_radio)
        self.crear_entrada_propiedad("Masa", 1, self.set_masa)
        self.crear_entrada_propiedad("Rebote", 0.7, self.set_rebote)

        self.__radio = 4
        self.__masa = 1
        self.__rebote = 0.7

    def get_simulacion(self):
        return self.__simulacion
    
    def set_gravedad(self, valor):
        self.simulacion.vector_g = float(valor)

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
        self.simulacion.pausado = not self.simulacion.get_pausado()
        self.boton_pausa.config(text="Reanudar" if self.simulacion.pausado else "Pausar")

    def dibujar_particulas(self):
        imagen = np.full((self.__simulacion.get_alto(), self.__simulacion.get_ancho(), 3), [255, 255, 255], dtype=np.uint8)
        
        for particula in self.__simulacion.get_particulas():
            cv2.circle(imagen, (int(particula.get_X()), int(particula.get_Y())), particula.get_radio(), particula.get_color(), -1)
        
        self.foto = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(imagen))
        self.__lienzo.create_image(0, 0, image=self.foto, anchor=tk.NW)

    def crear_entrada(self, texto_etiqueta, valor_inicial, comando):
        marco = tk.Frame(self.__controles)
        marco.pack()
        etiqueta = Label(marco, text=texto_etiqueta)
        etiqueta.pack(side=tk.LEFT)
        entrada = Entry(marco)
        entrada.insert(0, str(valor_inicial))
        entrada.pack(side=tk.LEFT)
        entrada.bind("<Return>", lambda event: comando(entrada.get()))

    def crear_entrada_propiedad(self, texto_etiqueta, valor_inicial, comando):
        marco = tk.Frame(self.__propiedades_particulas)
        marco.pack()
        etiqueta = Label(marco, text=texto_etiqueta)
        etiqueta.pack(side=tk.LEFT)
        entrada = Entry(marco)
        entrada.insert(0, str(valor_inicial))
        entrada.pack(side=tk.LEFT)
        entrada.bind("<Return>", lambda event: comando(entrada.get()))

    def ejecutar(self):
        self.__lienzo.bind("<Button-1>", self.manejar_clic_izquierdo)
        self.__lienzo.bind("<B1-Motion>", self.arrastrar_particula)
        self.__lienzo.bind("<ButtonRelease-1>", self.finalizar_arrastre)
        ejecutando = True
        while ejecutando:
            if not self.__simulacion.get_pausado():
                self.__simulacion.actualizar()
            self.dibujar_particulas()
            self.__tk.update_idletasks()
            self.__tk.update()

    def agregar_particula_mouse(self, event):
        if self.modo_mouse.get() == "Agregar Partículas":
            x, y = event.x, event.y
            self.__simulacion.agregar_particula(x, y, self.radio, self.masa, self.rebote)

    def iniciar_arrastre(self, event):
        if self.modo_mouse.get() == "Mover Partículas":
            self.particula_seleccionada = None
            encontrado = False
            for particula in self.simulacion.particulas:
                if encontrado:
                    continue
                distancia = np.linalg.norm(np.array([particula.x, particula.y]) - np.array([event.x, event.y]))
                if distancia <= particula.radio:
                    self.particula_seleccionada = particula
                    encontrado = True

    def arrastrar_particula(self, event):
        if self.modo_mouse.get() == "Mover Partículas" and self.particula_seleccionada:
            self.particula_seleccionada.x = event.x
            self.particula_seleccionada.y = event.y

    def finalizar_arrastre(self, event):
        if self.modo_mouse.get() == "Mover Partículas":
            self.particula_seleccionada = None

    def manejar_clic_izquierdo(self, event):
        if self.modo_mouse.get() == "Agregar Partículas":
            self.agregar_particula_mouse(event)
        elif self.modo_mouse.get() == "Mover Partículas":
            self.iniciar_arrastre(event)