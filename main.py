import random
from gui import *
from Particula import *
from Simulacion import *

if __name__ == "__main__":
    simulacion = Simulacion()
    interfaz = Interfaz(simulacion)

    # Añadir algunas partículas a la simulación
    for i in range(10):
        x = random.uniform(50, simulacion.ancho - 50)
        y = random.uniform(50, simulacion.alto - 50)
        simulacion.agregar_particula(x, y, 4, 1, 0.7)

    interfaz.ejecutar()