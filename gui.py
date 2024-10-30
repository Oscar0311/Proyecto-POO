from tkinter import Tk, Canvas, Entry, Label, Button, Frame, LabelFrame
import tkinter as tk
import numpy as np
import cv2
import PIL.Image, PIL.ImageTk

class Interfaz:
    def __init__(self, simulacion):
        # Inicialización de la interfaz gráfica
        self.__simulacion = simulacion
        self.__tk = Tk()
        self.__tk.title("Simulación de Partículas")
        self.__tk.geometry("800x600")

        # Lienzo para dibujar las partículas
        self.__lienzo = Canvas(self.__tk, width=self.__simulacion.get_ancho(), height=self.__simulacion.get_alto(), bg="white")
        self.__lienzo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame para los controles de la simulación
        self.__controles = Frame(self.__tk)
        self.__controles.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Creación de controles para ajustar parámetros de la simulación
        self.crear_entrada("Gravedad (m/s^2)", self.__simulacion.get_vector_g()[1], self.set_gravedad)
        self.crear_entrada("Resistencia del Aire", self.__simulacion.get_res_aire(), self.set_resistencia_aire)
        self.crear_entrada("Temperatura (K)", self.__simulacion.get_temperatura(), self.set_temperatura)
        self.crear_entrada("Fricción del Suelo", self.__simulacion.get_friccion_suelo(), self.set_friccion_suelo)

        # Botón para pausar/reanudar la simulación
        self.__boton_pausa = Button(self.__controles, text="Play", command=self.toggle_pausa, bg="lightblue")
        self.__boton_pausa.pack(pady=5)

        self.__foto = None

        # Menú desplegable para seleccionar el modo de interacción con el mouse
        self.__modo_mouse = tk.StringVar(value="Agregar Partículas")
        opciones_modo = ["Agregar Partículas", "Mover Partículas", "Eliminar Partículas"]
        self.__menu_modo = tk.OptionMenu(self.__controles, self.__modo_mouse, *opciones_modo)
        self.__menu_modo.pack(pady=5)

        # Controles para ajustar propiedades de las partículas
        self.__propiedades_particulas = LabelFrame(self.__controles, text="Propiedades de Partículas", padx=10, pady=10)
        self.__propiedades_particulas.pack(fill=tk.Y, padx=10, pady=10)

        self.crear_entrada_propiedad("Radio", 4, self.set_radio)
        self.crear_entrada_propiedad("Masa", 1, self.set_masa)
        self.crear_entrada_propiedad("Rebote", 0.7, self.set_rebote)

        # Valores por defecto para las propiedades de las partículas
        self.__radio = 4
        self.__masa = 1
        self.__rebote = 0.7

    # Métodos para actualizar parámetros de la simulación
    def set_gravedad(self, valor):
        self.__simulacion.set_vector_g(float(valor))

    def set_resistencia_aire(self, valor):
        self.__simulacion.set_res_aire(float(valor))

    def set_temperatura(self, valor):
        self.__simulacion.set_temperatura(float(valor))

    def set_friccion_suelo(self, valor):
        self.__simulacion.set_friccion_suelo(float(valor))

    # Métodos para actualizar propiedades de las partículas
    def set_radio(self, valor):
        self.__radio = int(valor)

    def set_masa(self, valor):
        self.__masa = float(valor)

    def set_rebote(self, valor):
        self.__rebote = float(valor)

    # Método para pausar/reanudar la simulación
    def toggle_pausa(self):
        self.__simulacion.set_pausado(not self.__simulacion.get_pausado()) 
        self.__boton_pausa.config(text="Play" if self.__simulacion.get_pausado() else "Pausar")

    # Método para dibujar las partículas en el lienzo
    def dibujar_particulas(self):
        imagen = np.full((self.__simulacion.get_alto(), self.__simulacion.get_ancho(), 3), [255, 255, 255], dtype=np.uint8)
        for particula in self.__simulacion.get_particulas():
            cv2.circle(imagen, (int(particula.get_x()), int(particula.get_y())), particula.get_radio(), particula.get_color(), -1)
        self.__foto = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(imagen))
        self.__lienzo.create_image(0, 0, image=self.__foto, anchor=tk.NW)

    # Métodos auxiliares para crear controles en la interfaz
    def crear_entrada(self, texto_etiqueta, valor_inicial, comando):
        marco = tk.Frame(self.__controles)
        marco.pack(pady=5)
        etiqueta = Label(marco, text=texto_etiqueta)
        etiqueta.pack(side=tk.LEFT)
        entrada = Entry(marco)
        entrada.insert(0, str(valor_inicial))
        entrada.pack(side=tk.LEFT)
        entrada.bind("<Return>", lambda event: comando(entrada.get()))

    def crear_entrada_propiedad(self, texto_etiqueta, valor_inicial, comando):
        marco = tk.Frame(self.__propiedades_particulas)
        marco.pack(pady=5)
        etiqueta = Label(marco, text=texto_etiqueta)
        etiqueta.pack(side=tk.LEFT)
        entrada = Entry(marco)
        entrada.insert(0, str(valor_inicial))
        entrada.pack(side=tk.LEFT)
        entrada.bind("<Return>", lambda event: comando(entrada.get()))

    # Método principal para ejecutar la simulación
    def ejecutar(self):
        # Vinculación de eventos del mouse
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

    # Métodos para manejar la interacción del mouse con las partículas
    def agregar_particula_mouse(self, event):
        if self.__modo_mouse.get() == "Agregar Partículas":
            x, y = event.x, event.y
            self.__simulacion.agregar_particula(x, y, self.__radio, self.__masa, self.__rebote)

    def iniciar_arrastre(self, event):
        if self.__modo_mouse.get() == "Mover Partículas":
            self.particula_seleccionada = None
            particula_encontrada = False
            for particula in self.__simulacion.get_particulas():
                if not particula_encontrada:
                    distancia = np.linalg.norm(np.array([particula.get_x(), particula.get_y()]) - np.array([event.x, event.y]))
                    if distancia <= particula.get_radio():
                        self.particula_seleccionada = particula
                        particula_encontrada = True

    def arrastrar_particula(self, event):
        if self.__modo_mouse.get() == "Mover Partículas" and self.particula_seleccionada:
            self.particula_seleccionada.set_x(event.x)
            self.particula_seleccionada.set_y(event.y)

    def eliminar_particula(self, event):
        if self.__modo_mouse.get() == "Eliminar Partículas":
            particulas_a_eliminar = []
            for particula in self.__simulacion.get_particulas():
                distancia = np.linalg.norm(np.array([particula.get_x(), particula.get_y()]) - np.array([event.x, event.y]))
                if distancia <= particula.get_radio():
                    particulas_a_eliminar.append(particula)
            for particula in particulas_a_eliminar:
                self.__simulacion.get_particulas().remove(particula)

    def finalizar_arrastre(self, event):
        if self.__modo_mouse.get() == "Mover Partículas":
            self.particula_seleccionada = None

    def manejar_clic_izquierdo(self, event):
        if self.__modo_mouse.get() == "Agregar Partículas":
            self.agregar_particula_mouse(event)
        elif self.__modo_mouse.get() == "Mover Partículas":
            self.iniciar_arrastre(event)
        elif self.__modo_mouse.get() == "Eliminar Partículas":
            self.eliminar_particula(event)