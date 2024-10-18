import numpy as np
import math
#aaa
class Particula:
    def __init__(self, simulacion, x, y, radio, masa, rebote, color='random', velocidad=np.zeros(2)):
        self.__simulacion = simulacion
        self.__x = x
        self.__y = y
        self.__radio = radio
        self.__color = np.random.randint(0, 255, 3).tolist() if color == 'random' else color
        self.__masa = masa
        self.__velocidad = np.array(velocidad).astype('float32')
        self.__aceleracion = np.zeros(2)
        self.__rebote = rebote
        self.__radio_atraccion = 50
        self.__radio_repulsion = 10
        self.__atraccion = 0.5
        self.__repulsion = 1

    def fuerza_aplicada(self, fuerza):
        self.__aceleracion += fuerza / float(abs(self.__masa))

    def get_X(self):
        return self.__x 
    
    def get_Y(self):
        return self.__y
    
    def get_radio(self):
        return self.__radio
    
    def get_color(self):
        return self.__color

    def actualizar(self):
        if not self.__simulacion.get_pausado():
            self.__aceleracion = self.__simulacion.get_vector_g() * math.copysign(1, self.__masa)  # Gravedad
            self.fuerza_aplicada(self.__simulacion.get_fuerza_viento() * self.__radio)

            for particula in self.__simulacion.get_particulas():
                if particula == self:
                    continue

                direccion = np.array([particula.__x, particula.__y]) - np.array([self.__x, self.__y])
                distancia = np.linalg.norm(direccion)
                if distancia != 0:
                    direccion = direccion / distancia

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
                if self.__simulacion.get_res_aire() > 0:
                    factor_resistencia_aire = (1 - self.__simulacion.get_res_aire())
                else:
                    factor_resistencia_aire = 1

                if self.__simulacion.get_temperatura() > 0:  # Evitamos temperaturas negativas
                    self.__velocidad += np.clip(self.__aceleracion, -2, 2) * factor_resistencia_aire
                    self.__velocidad += np.random.uniform(-1, 1, 2) * math.sqrt(self.__simulacion.get_temperatura()) * factor_resistencia_aire  # El movimiento térmico depende de sqrt(T)
                else:
                    self.__velocidad = np.zeros(2)  # Si la temperatura es 0K, no hay movimiento
                    
                self.__x += self.__velocidad[0]
                self.__y += self.__velocidad[1]

            if self.__x + self.__radio >= self.__simulacion.get_ancho():
                self.__x = self.__simulacion.get_ancho() - self.__radio
                self.__velocidad[0] *= -self.__rebote
            if self.__x - self.__radio <= 0:
                self.__x = self.__radio
                self.__velocidad[0] *= -self.__rebote
            if self.__y + self.__radio >= self.__simulacion.get_alto():

                if abs(self.__velocidad[1]) < 0.1 and abs(self.__simulacion.vector_g[1]) > 0:
                    self.__y = self.__simulacion.get_alto() - self.__radio

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

                    self.y = self.__radio
                    self.__velocidad[1] *= -self.__rebote