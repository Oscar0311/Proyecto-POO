from tkinter import Tk, Canvas, Entry, Label, Button, Frame, LabelFrame
import tkinter as tk
import numpy as np
import cv2
import PIL.Image, PIL.ImageTk

class Interfaz:
    def __init__(self, simulacion):
        self.simulacion = simulacion
        self.tk = Tk()
        self.tk.title("Simulación de Partículas")
        self.tk.geometry("800x600")

        # Lienzo para las partículas
        self.lienzo = Canvas(self.tk, width=self.simulacion.ancho, height=self.simulacion.alto, bg="white")
        self.lienzo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame para los controles
        self.controles = Frame(self.tk)
        self.controles.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Controles para la simulación
        self.crear_entrada("Gravedad (m/s^2)", self.simulacion.vector_g[1], self.set_gravedad)
        self.crear_entrada("Resistencia del Aire", self.simulacion.res_aire, self.set_resistencia_aire)
        self.crear_entrada("Temperatura (K)", self.simulacion.temperatura, self.set_temperatura)
        self.crear_entrada("Fricción del Suelo", self.simulacion.friccion_suelo, self.set_friccion_suelo)

        self.boton_pausa = Button(self.controles, text="Play", command=self.toggle_pausa, bg="lightblue")
        self.boton_pausa.pack(pady=5)

        self.foto = None

        # Menú para seleccionar el modo de interacción
        self.modo_mouse = tk.StringVar(value="Agregar Partículas")
        opciones_modo = ["Agregar Partículas", "Mover Partículas", "Eliminar Partículas"]
        self.menu_modo = tk.OptionMenu(self.controles, self.modo_mouse, *opciones_modo)
        self.menu_modo.pack(pady=5)

        # Controles para propiedades de partículas
        self.propiedades_particulas = LabelFrame(self.controles, text="Propiedades de Partículas", padx=10, pady=10)
        self.propiedades_particulas.pack(fill=tk.Y, padx=10, pady=10)

        self.crear_entrada_propiedad("Radio", 4, self.set_radio)
        self.crear_entrada_propiedad("Masa", 1, self.set_masa)
        self.crear_entrada_propiedad("Rebote", 0.7, self.set_rebote)

        self.radio = 4
        self.masa = 1
        self.rebote = 0.7

    def set_gravedad(self, valor):
        self.simulacion.vector_g = float(valor)

    def set_resistencia_aire(self, valor):
        self.simulacion.res_aire = float(valor)

    def set_temperatura(self, valor):
        self.simulacion.temperatura = float(valor)

    def set_friccion_suelo(self, valor):
        self.simulacion.friccion_suelo = float(valor)

    def set_radio(self, valor):
        self.radio = int(valor)

    def set_masa(self, valor):
        self.masa = float(valor)

    def set_rebote(self, valor):
        self.rebote = float(valor)

    def toggle_pausa(self):
        self.simulacion.pausado = not self.simulacion.pausado
        self.boton_pausa.config(text="Play" if self.simulacion.pausado else "Pausar")

    def dibujar_particulas(self):
        imagen = np.full((self.simulacion.alto, self.simulacion.ancho, 3), [255, 255, 255], dtype=np.uint8)
        for particula in self.simulacion.particulas:
            cv2.circle(imagen, (int(particula.x), int(particula.y)), particula.radio, particula.color, -1)
        self.foto = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(imagen))
        self.lienzo.create_image(0, 0, image=self.foto, anchor=tk.NW)

    def crear_entrada(self, texto_etiqueta, valor_inicial, comando):
        marco = tk.Frame(self.controles)
        marco.pack(pady=5)
        etiqueta = Label(marco, text=texto_etiqueta)
        etiqueta.pack(side=tk.LEFT)
        entrada = Entry(marco)
        entrada.insert(0, str(valor_inicial))
        entrada.pack(side=tk.LEFT)
        entrada.bind("<Return>", lambda event: comando(entrada.get()))

    def crear_entrada_propiedad(self, texto_etiqueta, valor_inicial, comando):
        marco = tk.Frame(self.propiedades_particulas)
        marco.pack(pady=5)
        etiqueta = Label(marco, text=texto_etiqueta)
        etiqueta.pack(side=tk.LEFT)
        entrada = Entry(marco)
        entrada.insert(0, str(valor_inicial))
        entrada.pack(side=tk.LEFT)
        entrada.bind("<Return>", lambda event: comando(entrada.get()))

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

    def agregar_particula_mouse(self, event):
        if self.modo_mouse.get() == "Agregar Partículas":
            x, y = event.x, event.y
            self.simulacion.agregar_particula(x, y, self.radio, self.masa, self.rebote)

    def iniciar_arrastre(self, event):
        if self.modo_mouse.get() == "Mover Partículas":
            self.particula_seleccionada = None
            particula_encontrada = False
            for particula in self.simulacion.particulas:
                if not particula_encontrada:
                    distancia = np.linalg.norm(np.array([particula.x, particula.y]) - np.array([event.x, event.y]))
                    if distancia <= particula.radio:
                        self.particula_seleccionada = particula
                        particula_encontrada = True


    def arrastrar_particula(self, event):
        if self.modo_mouse.get() == "Mover Partículas" and self.particula_seleccionada:
            self.particula_seleccionada.x = event.x
            self.particula_seleccionada.y = event.y

    def eliminar_particula(self, event):
        if self.modo_mouse.get() == "Eliminar Partículas":
            particulas_a_eliminar = []
            for particula in self.simulacion.particulas:
                distancia = np.linalg.norm(np.array([particula.x, particula.y]) - np.array([event.x, event.y]))
                if distancia <= particula.radio:
                    particulas_a_eliminar.append(particula)
            for particula in particulas_a_eliminar:
                self.simulacion.particulas.remove(particula)

    def finalizar_arrastre(self, event):
        if self.modo_mouse.get() == "Mover Partículas":
            self.particula_seleccionada = None

    def manejar_clic_izquierdo(self, event):
        if self.modo_mouse.get() == "Agregar Partículas":
            self.agregar_particula_mouse(event)
        elif self.modo_mouse.get() == "Mover Partículas":
            self.iniciar_arrastre(event)
        elif self.modo_mouse.get() == "Eliminar Partículas":
            self.eliminar_particula(event)
