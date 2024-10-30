import numpy as np
import math

class Particula:
    def __init__(self, simulacion, x, y, radio, masa, rebote, color='random', velocidad=np.zeros(2)):
        # Inicialización de los atributos de la partícula
        self.__simulacion = simulacion
        self.__x = x
        self.__y = y
        self.__radio = radio
        self.__color = np.random.randint(0, 255, 3).tolist() if color == 'random' else color
        self.__masa = masa
        self.__velocidad = np.array(velocidad).astype('float32')
        self.__aceleracion = np.zeros(2)
        self.__rebote = rebote
        
        # Parámetros para la interacción entre partículas
        self.__radio_atraccion = 50
        self.__radio_repulsion = 10
        self.__atraccion = 0.5
        self.__repulsion = 1

    def get_simulacion(self):
        return self.__simulacion
    
    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    def get_radio(self):
        return self.__radio
    
    def get_color(self):
        return self.__color
    
    def get_masa(self):
        return self.__masa
    
    def get_velocidad(self):
        return self.__velocidad
    
    def get_aceleracion(self):
        return self.__aceleracion
    
    def get_rebote(self):
        return self.__rebote
    
    def get_radio_atraccion(self):
        return self.__radio_atraccion
    
    def get_radio_repulsion(self):
        return self.__radio_repulsion
    
    def get_atraccion(self):
        return self.__atraccion
    
    def get_repulsion(self):
        return self.__repulsion
    
    def set_simulacion(self, simulacion):
        self.__simulacion = simulacion
    
    def set_x(self, x):
        self.__x = x
    
    def set_y(self, y):
        self.__y = y
    
    def set_radio(self, radio):
        self.__radio = radio
    
    def set_color(self, color):
        self.__color = color
    
    def set_masa(self, masa):
        self.__masa = masa
    
    def set_velocidad(self, velocidad):
        self.__velocidad = velocidad
    
    def set_aceleracion(self, aceleracion):
        self.__aceleracion = aceleracion
    
    def set_rebote(self, rebote):
        self.__rebote = rebote
    
    def set_radio_atraccion(self, radio_atraccion):
        self.__radio_atraccion = radio_atraccion
    
    def set_radio_repulsion(self, radio_repulsion):
        self.__radio_repulsion = radio_repulsion
    
    def set_atraccion(self, atraccion):
        self.__atraccion = atraccion
    
    def set_repulsion(self, repulsion):
        self.__repulsion = repulsion
    
    def fuerza_aplicada(self, fuerza):
        # Aplica una fuerza a la partícula, actualizando su aceleración
        self.__aceleracion += fuerza / float(abs(self.__masa)) 

    def actualizar(self):
        if not self.__simulacion.get_pausado():
            # Aplicar gravedad
            self.__aceleracion = self.__simulacion.get_vector_g() * math.copysign(1, self.__masa)
            
            # Aplicar fuerza del viento
            self.fuerza_aplicada(self.__simulacion.get_fuerza_viento() * self.__radio)

            # Calcular interacciones con otras partículas
            for particula in self.__simulacion.get_particulas():
                if particula != self:
                    direccion = np.array([particula.get_x(), particula.get_y()]) - np.array([self.__x, self.__y])
                    distancia = np.linalg.norm(direccion)
                    if distancia != 0:
                        direccion = direccion / distancia

                    # Aplicar fuerzas de repulsión y atracción
                    if distancia < self.__radio_repulsion:
                        if distancia > 0:
                            fuerza = -self.__repulsion * direccion / distancia * (self.__radio_repulsion - distancia)
                        else:
                            fuerza = np.zeros(2)
                    elif distancia < self.__radio_atraccion:
                        fuerza = self.__atraccion * direccion / distancia * (distancia - self.__radio_repulsion)
                    else:
                        fuerza = np.zeros(2)

                    self.fuerza_aplicada(fuerza)

            if not self.__simulacion.get_pausado():
                # Aplicar resistencia del aire
                if self.__simulacion.get_res_aire() > 0:
                    factor_resistencia_aire = (1 - self.__simulacion.get_res_aire())
                else:
                    factor_resistencia_aire = 1

                # Actualizar velocidad y posición considerando la temperatura
                if self.__simulacion.get_temperatura() > 0:  # Evitamos temperaturas negativas
                    self.__velocidad += np.clip(self.__aceleracion, -2, 2) * factor_resistencia_aire
                    self.__velocidad += np.random.uniform(-1, 1, 2) * math.sqrt(self.__simulacion.get_temperatura()) * factor_resistencia_aire  # El movimiento térmico depende de sqrt(T)
                else:
                    self.__velocidad = np.zeros(2)  # Si la temperatura es 0K, no hay movimiento

                self.__x += int(self.__velocidad[0])
                self.__y += int(self.__velocidad[1])

            # Manejar colisiones con los bordes
            if self.__x + self.__radio >= self.__simulacion.get_ancho():
                self.__x = self.__simulacion.get_ancho() - self.__radio
                self.__velocidad[0] *= -self.__rebote
            if self.__x - self.__radio <= 0:
                self.__x = self.__radio
                self.__velocidad[0] *= -self.__rebote
            if self.__y + self.__radio >= self.__simulacion.get_alto():
                if abs(self.__velocidad[1]) < 0.1 and abs(self.__simulacion.get_vector_g()[1]) > 0:
                    self.__y = self.__simulacion.get_alto() - self.__radio
                    
                    # Aplicar fricción si la partícula está en el suelo
                    if abs(self.__velocidad[0]) > 0.01:
                        fuerza_friccion = -self.__simulacion.get_friccion_suelo() * math.copysign(1, self.__velocidad[0])
                        aceleracion_friccion = fuerza_friccion / float(abs(self.__masa))
                        if abs(aceleracion_friccion) < abs(self.__velocidad[0]):
                            self.__velocidad[0] += aceleracion_friccion
                        else:
                            self.__velocidad[0] = 0
                    else:
                        self.__velocidad[0] = 0
                        self.__velocidad[1] = 0
                else:
                    self.__y = self.__simulacion.get_alto() - self.__radio
                    self.__velocidad[1] *= -self.__rebote

            if self.__y - self.__radio <= 0:
                if abs(self.__velocidad[1]) < 0.1 and abs(self.__simulacion.get_vector_g()[1]) > 0:
                    # Aplicar fricción si la partícula está en el techo
                    if abs(self.__velocidad[0]) > 0.01:
                        fuerza_friccion = -self.__simulacion.get_friccion_suelo() * math.copysign(1, self.__velocidad[0])
                        aceleracion_friccion = fuerza_friccion / float(abs(self.__masa))
                        if abs(aceleracion_friccion) < abs(self.__velocidad[0]):
                            self.__velocidad += aceleracion_friccion
                        else:
                            self.__velocidad[0] = 0
                    else:
                        self.__velocidad[0] = 0
                        self.__velocidad[1] = 0
                else:
                    self.__y = self.__radio
                    self.__velocidad[1] *= -self.__rebote