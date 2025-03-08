from ..utilidades.optica import reflect, refract, fresnel
import numpy as np
from ..utilidades.aleatorios import UniformMontecarlo

class Interfase():
  """
  Representa la frontera entre dos medios.
  """
  def __init__(self, estructura, indice_exterior):
    """
    Args:
        estructura (estructura): Estructura que representa la interfase.
        indice_exterior (float): Índice de refracción del medio exterior.
    """
    self.estructura = estructura
    self.indice_exterior = indice_exterior
  
  def interactuar(self, n, foton):
    """
    Determina la interacción del foton con la interfase.
    
    Args:
        foton (SimulatedPhoton): Foton que interactua con la interfase.
        punto_incidencia (list, float): Punto de intersección.
        n (list, float): Vector normal a la superficie en el punto de intersección.
    
    Returns:
        
    """
    # Calcular índice de refracción (distinto para medios dispersivos)
    indice_refraccion = self.estructura.indice_refraccion.calcular(foton.f)
    
    # Determinar ángulo de incidencia y refracción
    direccion_refract = refract(foton.dire, n, self.indice_exterior, indice_refraccion)
    direccion_reflect = reflect(foton.dire, n)
    teta_i = np.arccos(np.dot(direccion_reflect, n))
    teta_t = np.arccos(np.dot(direccion_refract, -n))
    
    # Determinar coeficiente de Fresnel
    Ru = fresnel(self.indice_exterior, indice_refraccion, teta_t, teta_i)
    
    reflexion =  UniformMontecarlo(Ru)
    if reflexion:
      foton.dire = direccion_reflect
    else:
      foton.dire = direccion_refract
    return foton
    
    