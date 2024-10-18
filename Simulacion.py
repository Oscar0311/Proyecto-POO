import numpy as np
from Particula import*

class Simulacion:
    def __init__(self, ancho=650, alto=600):
        self.ancho = ancho
        self.alto = alto
        self.particulas = []
        self.pausado = False
        self.velocidad = 0.1
        self.temperatura = 300  # Temperatura inicial en Kelvin
        self.vector_g = np.array([0, 9.8])  # Gravedad estándar en m/s^2
        self.fuerza_viento = np.array([0, 0])
        self.res_aire = 0.05
        self.friccion_suelo = 0.05
    
    def agregar_particula(self, x, y, radio, masa, rebote):
        particula = Particula(self, x, y, radio, masa, rebote)
        self.particulas.append(particula)

    def actualizar(self):
        for particula in self.particulas:
            particula.actualizar()