import numpy as np
from Particula import*

class Simulacion:
    def __init__(self, ancho=650, alto=600):
        self.__ancho = ancho
        self.__alto = alto
        self.__particulas = []
        self.__pausado = False
        self.__temperatura = 300  # Temperatura inicial en Kelvin
        self.__vector_g = np.array([0, 9.8])  # Gravedad estándar en m/s^2
        self.__fuerza_viento = np.array([0, 0])
        self.__res_aire = 0.05
        self.__friccion_suelo = 0.05

    def get_ancho(self):
        return self.__ancho
    
    def get_alto(self):
        return self.__alto
    
    def get_vector_g(self):
        return self.__vector_g
    
    def get_res_aire(self):
        return self.__res_aire
    
    def get_temperatura(self):
        return self.__temperatura
    
    def get_friccion_suelo(self):
        return self.__friccion_suelo
    
    def get_pausado(self):
        return self.__pausado
    
    def get_fuerza_viento(self):
        return self.__fuerza_viento
    
    def get_particulas(self):
        return self.__particulas
    
    def agregar_particula(self, x, y, radio, masa, rebote):
        particula = Particula(self, x, y, radio, masa, rebote)
        self.__particulas.append(particula)

    def actualizar(self):
        for particula in self.__particulas:
            particula.actualizar()