import numpy as np
from Particula import *


class Simulacion:
    def _init_(self, ancho=650, alto=600):
        self.ancho = ancho
        self.alto = alto
        self.particulas = []
        self.pausado = False
        self.velocidad = 0.1
        self.temperatura = 0.5
        self.vector_g = np.array([0, 0.1])
        self.fuerza_viento = np.array([0, 0])
        self.res_aire = 0.05
        self.friccion_suelo = 0.05
    
    def agregar_particula(self, x, y):
        particula = Particula(self, x, y)
        self.particulas.append(particula)

    def actualizar(self):
        for particula in self.particulas:
            particula.actualizar()