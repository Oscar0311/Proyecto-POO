import random
from gui import *
from particle import *
from simulation import *

if _name_ == "_main_":
    simulacion = Simulacion()
    interfaz = Interfaz(simulacion)

    # Añadir algunas partículas a la simulación
    for _ in range(50):
        x = random.uniform(50, simulacion.ancho - 50)
        y = random.uniform(50, simulacion.alto - 50)
        simulacion.agregar_particula(x, y, 4, 1, 0.7)

    interfaz.ejecutar()