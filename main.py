import random
from gui import *
from Particula import *
from Simulacion import *

if __name__ == "__main__":
    # Crear una instancia de la simulación
    simulacion = Simulacion()
    
    # Crear la interfaz gráfica, pasándole la simulación como argumento
    interfaz = Interfaz(simulacion)

    # Añadir algunas partículas iniciales a la simulación de forma aleatoria
    for i in range(10):
        x = random.uniform(50, simulacion.ancho - 50)
        y = random.uniform(50, simulacion.alto - 50)
        simulacion.agregar_particula(x, y, 4, 1, 0.7)

    # Iniciar la ejecución de la interfaz, lo que a su vez inicia la simulación
    interfaz.ejecutar()