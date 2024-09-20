import numpy as np

class Particula:
    def __init__(self, simulacion, x, y, radio=4, color='random', masa=1, velocidad=np.zeros(2), rebote=0.7):
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