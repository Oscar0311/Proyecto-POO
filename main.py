import random
from gui import *
from Particula import *
from Simulacion import *

if __name__ == "__main__":
    simulacion = Simulacion()
    interfaz = Interfaz(simulacion)
    
    for _ in range(50):
        x = random.uniform(50, simulacion.ancho - 50)
        y = random.uniform(50, simulacion.alto - 50)
        simulacion.agregar_particula(x, y)

    interfaz.ejecutar()