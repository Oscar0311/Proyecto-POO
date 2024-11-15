import numpy as np
import math

class Particula:
    def __init__(self, simulacion, x, y, radio, masa, rebote, velocidad, color='random'):
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
    
    def detener_movimiento(self):
        # Método para detener el movimiento de la partícula
        self.__velocidad = np.array([0.0, 0.0])
    
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
        self.__aceleracion += fuerza / float(self.__masa)

    def aplicar_temperatura(self):
        # Obtiene la temperatura de la simulación
        temperatura = self.__simulacion.get_temperatura()

        # Factor de variación de velocidad en función de la temperatura
        variacion = temperatura * 0.001  # Ajusta el factor para controlar la intensidad del temblor

        # Aplica una variación aleatoria a la velocidad
        self.__velocidad += np.random.uniform(-variacion, variacion, 2) 

    def actualizar(self):
        if not self.__simulacion.get_pausado():
            # Aplicar gravedad, temperatura y fuerza aplicada
            self.__aceleracion = self.__simulacion.get_vector_g()
            self.fuerza_aplicada(self.__simulacion.get_fuerza_viento()*self.__radio)
            self.aplicar_temperatura()

            for particula in self.__simulacion.get_particulas():
                if particula != self:
                    direccion = np.array([particula.get_x(), particula.get_y()]) - np.array([self.__x, self.__y])
                    distancia = math.sqrt(((particula.get_x() - self.__x) ** 2) + ((particula.get_y() - self.__y) ** 2))
                    
                    if distancia != 0:
                        direccion = direccion / distancia

                    if distancia <= self.__radio + particula.get_radio():
                        temp = self.__velocidad[0]
                        self.__velocidad[0] = (self.__masa - particula.get_masa()) / (self.__masa + particula.get_masa()) * self.__velocidad[0] + 2 * particula.get_masa() / (self.__masa + particula.get_masa()) * particula.get_velocidad()[0] * self.__rebote
                        velocidad_particula = particula.get_velocidad()
                        velocidad_particula[0] = 2 * self.__masa / (self.__masa + particula.get_masa()) * temp + (particula.get_masa() - self.__masa) / (self.__masa + particula.get_masa()) * temp * particula.get_rebote()

                        temp = self.__velocidad[1]
                        self.__velocidad[1] = (self.__masa - particula.get_masa()) / (self.__masa + particula.get_masa()) * self.__velocidad[1] + 2 * particula.get_masa() / (self.__masa + particula.get_masa()) * particula.get_velocidad()[1] * self.__rebote
                        velocidad_particula[1] = 2 * self.__masa / (self.__masa + particula.get_masa()) * temp + (particula.get_masa() - self.__masa) / (self.__masa + particula.get_masa()) * temp * particula.get_rebote()
                        particula.set_velocidad(velocidad_particula)

                        translate_vector = -direccion * (self.__radio + particula.get_radio()) + direccion * distancia
                        self.__x += translate_vector[0] * (self.__masa / (self.__masa + particula.get_masa()))
                        self.__y += translate_vector[1] * (self.__masa / (self.__masa + particula.get_masa()))

                        particula.set_x(particula.get_x() - translate_vector[0] * (particula.get_masa() / (self.__masa + particula.get_masa())))
                        particula.set_y(particula.get_y() - translate_vector[1] * (particula.get_masa() / (self.__masa + particula.get_masa())))

            if self.__x + self.__radio >=  self.__simulacion.get_ancho():
                self.__x = self.__simulacion.get_ancho() - self.__radio
                self.__velocidad[0] *= -self.__rebote

            if self.__x - self.__radio <= 0:
                self.__x = self.__radio
                self.__velocidad[0] *= -self.__rebote
            
            if self.__y + self.__radio >=  self.__simulacion.get_alto():
                self.__y = self.__simulacion.get_alto() - self.__radio
                self.__velocidad[1] *= -self.__rebote
                self.__velocidad[0] *= self.__simulacion.get_friccion_suelo()

            if self.__y - self.__radio <= 0:
                self.__y = self.__radio
                self.__velocidad[1] *= -self.__rebote

            self.__velocidad +=  self.__aceleracion * 0.1
            self.__x += self.__velocidad[0]
            self.__y += self.__velocidad[1]