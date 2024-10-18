import numpy as np
from Particula import*

class Simulacion:
    def __init__(self, ancho=650, alto=600):
        # Inicialización de los parámetros de la simulación
        self.ancho = ancho  # Ancho de la ventana de simulación
        self.alto = alto    # Alto de la ventana de simulación
        self.particulas = []  # Lista para almacenar todas las partículas
        self.pausado = True   # Estado inicial de la simulación (pausada)
        self.temperatura = 300  # Temperatura inicial en Kelvin
        self.vector_g = np.array([0, 9.8])  # Vector de gravedad estándar en m/s^2
        self.fuerza_viento = np.array([0, 0])  # Fuerza inicial del viento (ninguna)
        self.res_aire = 0.05  # Coeficiente de resistencia del aire
        self.friccion_suelo = 0.05  # Coeficiente de fricción del suelo
    
    def agregar_particula(self, x, y, radio, masa, rebote):
        # Método para agregar una nueva partícula a la simulación
        particula = Particula(self, x, y, radio, masa, rebote)
        self.particulas.append(particula)

    def actualizar(self):
        # Método para actualizar el estado de todas las partículas en la simulación
        for particula in self.particulas:
            particula.actualizar()