import numpy as np
import math

class Particula:
    def __init__(self, simulacion, x, y, radio, masa, rebote, color='random', velocidad=np.zeros(2)):
        self.simulacion = simulacion
        self.x = x
        self.y = y
        self.radio = radio
        self.color = np.random.randint(0, 255, 3).tolist() if color == 'random' else color
        self.masa = masa
        self.velocidad = np.array(velocidad).astype('float32')
        self.aceleracion = np.zeros(2)
        self.rebote = rebote
        self.radio_atraccion = 50
        self.radio_repulsion = 10
        self.atraccion = 0.5
        self.repulsion = 1

    def fuerza_aplicada(self, fuerza):
        self.aceleracion += fuerza / float(abs(self.masa)) 

    def actualizar(self):
        if not self.simulacion.pausado:
            self.aceleracion = self.simulacion.vector_g * math.copysign(1, self.masa)  # Gravedad
            self.fuerza_aplicada(self.simulacion.fuerza_viento * self.radio)

            for particula in self.simulacion.particulas:
                if particula != self:
                    direccion = np.array([particula.x, particula.y]) - np.array([self.x, self.y])
                    distancia = np.linalg.norm(direccion)
                    if distancia != 0:
                        direccion = direccion / distancia

                    if distancia < self.radio_repulsion:
                        if distancia > 0:
                            fuerza = -self.repulsion * direccion / distancia * (self.radio_repulsion - distancia)
                        else:
                            fuerza = np.zeros(2)
                    elif distancia < self.radio_atraccion:
                        fuerza = self.atraccion * direccion / distancia * (distancia - self.radio_repulsion)
                    else:
                        fuerza = np.zeros(2)

                    self.fuerza_aplicada(fuerza)

            if not self.simulacion.pausado:
                if self.simulacion.res_aire > 0:
                    factor_resistencia_aire = (1 - self.simulacion.res_aire)
                else:
                    factor_resistencia_aire = 1

                if self.simulacion.temperatura > 0:  # Evitamos temperaturas negativas
                    self.velocidad += np.clip(self.aceleracion, -2, 2) * factor_resistencia_aire
                    self.velocidad += np.random.uniform(-1, 1, 2) * math.sqrt(self.simulacion.temperatura) * factor_resistencia_aire  # El movimiento térmico depende de sqrt(T)
                else:
                    self.velocidad = np.zeros(2)  # Si la temperatura es 0K, no hay movimiento

                self.x += self.velocidad
                self.y += self.velocidad

            if self.x + self.radio >= self.simulacion.ancho:
                self.x = self.simulacion.ancho - self.radio
                self.velocidad *= -self.rebote
            if self.x - self.radio <= 0:
                self.x = self.radio
                self.velocidad *= -self.rebote
            if self.y + self.radio >= self.simulacion.alto:
                if abs(self.velocidad) < 0.1 and abs(self.simulacion.vector_g) > 0:
                    self.y = self.simulacion.alto - self.radio

                    if abs(self.velocidad) > 0.01:
                        fuerza_friccion = -self.simulacion.friccion_suelo * math.copysign(1, self.velocidad)
                        aceleracion_friccion = fuerza_friccion / float(abs(self.masa))
                        if abs(aceleracion_friccion) < abs(self.velocidad):
                            self.velocidad += aceleracion_friccion
                        else:
                            self.velocidad = 0
                    else:
                        self.velocidad = 0
                        self.velocidad = 0
                else:
                    self.y = self.simulacion.alto - self.radio
                    self.velocidad *= -self.rebote

            if self.y - self.radio <= 0:
                if abs(self.velocidad) < 0.1 and abs(self.simulacion.vector_g) > 0:
                    if abs(self.velocidad) > 0.01:
                        fuerza_friccion = -self.simulacion.friccion_suelo * math.copysign(1, self.velocidad)
                        aceleracion_friccion = fuerza_friccion / float(abs(self.masa))
                        if abs(aceleracion_friccion) < abs(self.velocidad):
                            self.velocidad += aceleracion_friccion
                        else:
                            self.velocidad = 0
                    else:
                        self.velocidad = 0
                        self.velocidad = 0
                else:
                    self.y = self.radio
                    self.velocidad *= -self.rebote
