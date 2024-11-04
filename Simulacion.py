import numpy as np
from Particula import*

class Simulacion:
    def __init__(self, ancho=650, alto=600):
        # Inicialización de los parámetros de la simulación
        self.__ancho = ancho  # Ancho de la ventana de simulación
        self.__alto = alto    # Alto de la ventana de simulación
        self.__particulas = []  # Lista para almacenar todas las partículas
        self.__pausado = True   # Estado inicial de la simulación (pausada)
        self.__temperatura = 300  # Temperatura inicial en Kelvin
        self.__vector_g = np.array([0, 9.8])  # Vector de gravedad estándar en m/s^2
        self.__fuerza_viento = np.array([0, 0])  # Fuerza inicial del viento (ninguna)
        self.__res_aire = 0.05  # Coeficiente de resistencia del aire
        self.__friccion_suelo = 0.05  # Coeficiente de fricción del suelo
    
    def agregar_particula(self, x, y, radio, masa, rebote):
        # Método para agregar una nueva partícula a la simulación
        particula = Particula(self, x, y, radio, masa, rebote)
        self.__particulas.append(particula)

    def actualizar(self):
        # Método para actualizar el estado de todas las partículas en la simulación
        if self.__temperatura > 0:  # Solo actualizar si la temperatura es mayor que 0
            for particula in self.__particulas:
                particula.actualizar()
        else:
            # Si la temperatura es 0, las partículas no se mueven
            for particula in self.__particulas:
                particula.detener_movimiento()  # Método para detener partículas 

    def get_ancho(self):
        return self.__ancho
    
    def get_alto(self):
        return self.__alto
    
    def get_particulas(self):
        return self.__particulas
    
    def get_pausado(self):
        return self.__pausado
    
    def get_temperatura(self):
        return self.__temperatura
    
    def get_vector_g(self):
        return self.__vector_g
    
    def get_fuerza_viento(self):
        return self.__fuerza_viento
    
    def get_res_aire(self):
        return self.__res_aire
    
    def get_friccion_suelo(self):
        return self.__friccion_suelo
    
    def set_ancho(self, ancho):
        self.__ancho = ancho
    
    def set_alto(self, alto):
        self.__alto = alto
    
    def set_particulas(self, particulas):
        self.__particulas = particulas
    
    def set_pausado(self, pausado):
        self.__pausado = pausado
    
    def set_temperatura(self, temperatura):
        self.__temperatura = temperatura
    
    def set_vector_g(self, vector_g):
        self.__vector_g = vector_g
    
    def set_fuerza_viento(self, fuerza_viento):
        self.__fuerza_viento = fuerza_viento
    
    def set_res_aire(self, res_aire):
        self.__res_aire = res_aire
    
    def set_friccion_suelo(self, friccion_suelo):
        self.__friccion_suelo = friccion_suelo