import numpy as np

class Trazador:
    """
    Lógica de propagación de los fotones, interacción con la interfase, 
    absorción, etc.
    """
    def __init__(self, escenario):
        self.escenario = escenario

    def propagar(self, foton):
        """
        Mueve un fotón paso a paso hasta que:
        - Se absorbe,
        - Sale del dominio de la simulación,
        - O se cumplen las condiciones de parada.
        """
        # Ejemplo:
        # 1. Calcular la distancia hasta la siguiente interacción (interfase)
        # 2. Comprobar si cruza la interfase y aplicar Fresnel
        # 3. Actualizar dirección, posición, energía, etc.
        pass

    def ejecutar(self):
        """
        Ejecuta la simulación completa (propaga todos los fotones).
        Retorna algún objeto con la información final (estadísticas, etc.)
        """
        # 1. Obtener lista de fotones del escenario
        # 2. Para cada fotón, llamar a propagar()
        # 3. Guardar eventos relevantes
        pass
