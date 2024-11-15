from tkinter import Tk, Canvas, Entry, Label, Button, Frame, LabelFrame
import tkinter as tk
import numpy as np
import cv2
import PIL.Image, PIL.ImageTk
from tooltips import tooltips

class Interfaz:
    def __init__(self, simulacion):
        # Inicialización de la interfaz gráfica
        self.__simulacion = simulacion
        self.__tk = Tk()
        self.__tk.title("Simulación de Partículas")
        self.__tk.geometry("900x720")

        self.__encabezado = Label(
            self.__tk, 
            text="Simulación de Partículas\nIntegrantes: Marcelo Ixquiac, Luis Saavedra, Aldo Bolaños, Oscar García", 
            font=("Arial", 14, "bold"), 
            pady=10
        )
        self.__encabezado.pack(side=tk.TOP)

        # Frame para el lienzo
        self.__frame_lienzo = Frame(self.__tk)
        self.__frame_lienzo.pack(side=tk.LEFT, padx=10, pady=10)

        # Lienzo para dibujar las partículas
        self.__lienzo = Canvas(self.__frame_lienzo, width=self.__simulacion.get_ancho(), height=self.__simulacion.get_alto(), bg="white")
        self.__lienzo.pack()

        # Variables para el rectángulo de selección
        self.__inicio_seleccion = None
        self.__rectangulo_seleccion = None

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
        self.crear_entrada_propiedad("Velocidad en x", 0.0, self.set_velocidad_x)
        self.crear_entrada_propiedad("Velocidad en y", 0.0, self.set_velocidad_y)

        # Valores por defecto para las propiedades de las partículas
        self.__radio = 4
        self.__masa = 1
        self.__rebote = 0.7
        self.__velocidad_x = 0.0
        self.__velocidad_y = 0.0

            # Explicaciones para los controles de simulación
        tooltips(self.__boton_pausa, "Pausa o reanuda la simulación")
        tooltips(self.__menu_modo, "Selecciona el modo de interacción con el mouse: \n- Agregar Partículas: Añade nuevas partículas. \n- Mover Partículas: Desplaza partículas existentes. \n- Eliminar Partículas: Elimina partículas seleccionadas.")

        # Explicaciones para los controles de parámetros de la simulación
        tooltips(self.__controles.winfo_children()[0], "Gravedad: Ajusta la gravedad (m/s²) que afecta a las partículas.")
        tooltips(self.__controles.winfo_children()[1], "Resistencia del Aire: Modifica la resistencia del aire que ralentiza las partículas.")
        tooltips(self.__controles.winfo_children()[2], "Temperatura: Cambia la temperatura (K) del sistema.")
        tooltips(self.__controles.winfo_children()[3], "Fricción del Suelo: Controla la fricción del suelo que desacelera las partículas.")

        # Explicaciones para las propiedades de partículas
        for widget in self.__propiedades_particulas.winfo_children():
            etiqueta_texto = widget.winfo_children()[0].cget("text")
            if "Radio" in etiqueta_texto:
                tooltips(widget, "Radio: Define el tamaño de las partículas.")
            elif "Masa" in etiqueta_texto:
                tooltips(widget, "Masa: Establece la masa de cada partícula.")
            elif "Rebote" in etiqueta_texto:
                tooltips(widget, "Rebote: Determina la elasticidad de la colisión de las partículas.")
            elif "Velocidad en x" in etiqueta_texto:
                tooltips(widget, "Velocidad en x: Especifica la velocidad inicial de las partículas en el eje X.")
            elif "Velocidad en y" in etiqueta_texto:
                tooltips(widget, "Velocidad en y: Especifica la velocidad inicial de las partículas en el eje Y.")

    def set_gravedad(self, valor):
        vector_g = self.__simulacion.get_vector_g()
        vector_g[1] = valor
        self.__simulacion.set_vector_g(vector_g)

    def set_resistencia_aire(self, valor):
        self.__simulacion.set_res_aire(float(valor))

    def set_temperatura(self, valor):
        self.__simulacion.set_temperatura(float(valor))

    def set_friccion_suelo(self, valor):
        self.__simulacion.set_friccion_suelo(float(valor))

    def set_radio(self, valor):
        self.__radio = int(valor)

    def set_masa(self, valor):
        self.__masa = float(valor)

    def set_rebote(self, valor):
        self.__rebote = float(valor)

    def set_velocidad_x(self, valor):
        self.__velocidad_x = float(valor)

    def set_velocidad_y(self, valor):
        self.__velocidad_y = float(valor)

    def toggle_pausa(self):
        self.__simulacion.set_pausado(not self.__simulacion.get_pausado()) 
        self.__boton_pausa.config(text="Play" if self.__simulacion.get_pausado() else "Pausar")

    def dibujar_particulas(self):
        imagen = np.full((self.__simulacion.get_alto(), self.__simulacion.get_ancho(), 3), [255, 255, 255], dtype=np.uint8)
        for particula in self.__simulacion.get_particulas():
            cv2.circle(imagen, (int(particula.get_x()), int(particula.get_y())), particula.get_radio(), particula.get_color(), -1)
        self.__foto = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(imagen))
        self.__lienzo.create_image(0, 0, image=self.__foto, anchor=tk.NW)
        
        # Redibujar el rectángulo de selección si existe
        if self.__rectangulo_seleccion is not None:
            self.__lienzo.tag_raise(self.__rectangulo_seleccion)

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

    def ejecutar(self):
        # Vinculación de eventos del mouse
        self.__lienzo.bind("<Button-1>", self.manejar_clic_izquierdo)
        self.__lienzo.bind("<B1-Motion>", self.manejar_arrastre)
        self.__lienzo.bind("<ButtonRelease-1>", self.manejar_soltar)
        ejecutando = True
        while ejecutando:
            if not self.__simulacion.get_pausado():
                self.__simulacion.actualizar()
            self.dibujar_particulas()
            self.__tk.update_idletasks()
            self.__tk.update()

    def agregar_particula_mouse(self, event):
        if self.__modo_mouse.get() == "Agregar Partículas":
            x, y = event.x, event.y
            self.__simulacion.agregar_particula(x, y, self.__radio, self.__masa, self.__rebote, np.array([self.__velocidad_x, -self.__velocidad_y]))

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
            self.__inicio_seleccion = (event.x, event.y)
            # Crear un nuevo rectángulo de selección
            self.__rectangulo_seleccion = self.__lienzo.create_rectangle(
                event.x, event.y, event.x, event.y,
                outline='red', dash=(2, 2)
            )

    def manejar_arrastre(self, event):
        if self.__modo_mouse.get() == "Mover Partículas" and hasattr(self, 'particula_seleccionada') and self.particula_seleccionada:
            self.arrastrar_particula(event)
        elif self.__modo_mouse.get() == "Eliminar Partículas" and self.__inicio_seleccion:
            # Actualizar el rectángulo de selección
            x0, y0 = self.__inicio_seleccion
            self.__lienzo.coords(self.__rectangulo_seleccion, x0, y0, event.x, event.y)

    def manejar_soltar(self, event):
        if self.__modo_mouse.get() == "Mover Partículas":
            self.finalizar_arrastre(event)
        elif self.__modo_mouse.get() == "Eliminar Partículas" and self.__inicio_seleccion:
            # Obtener las coordenadas del rectángulo
            x0, y0 = self.__inicio_seleccion
            x1, y1 = event.x, event.y
            
            # Ordenar las coordenadas
            x_min, x_max = min(x0, x1), max(x0, x1)
            y_min, y_max = min(y0, y1), max(y0, y1)
            
            # Eliminar partículas dentro del rectángulo
            particulas_a_eliminar = []
            for particula in self.__simulacion.get_particulas():
                x, y = particula.get_x(), particula.get_y()
                if (x_min <= x <= x_max) and (y_min <= y <= y_max):
                    particulas_a_eliminar.append(particula)
            
            for particula in particulas_a_eliminar:
                self.__simulacion.get_particulas().remove(particula)
            
            # Eliminar el rectángulo de selección
            if self.__rectangulo_seleccion:
                self.__lienzo.delete(self.__rectangulo_seleccion)
                self.__rectangulo_seleccion = None
            self.__inicio_seleccion = None