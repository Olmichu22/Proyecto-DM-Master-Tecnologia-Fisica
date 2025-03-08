from ..utilidades.geometria import intersecion_foton_esfera
from ..utilidades.optica import reflect, refract, fresnel
import numpy as np

class Interfase():
  """
  Representa la frontera entre dos medios.
  """
  def __init__(self, esfera, indice_exterior):
    """
    Args:
        esfera (esfera): Esfera que representa la interfase.
        indice_exterior (float): Índice de refracción del medio exterior.
    """
    self.esfera = esfera
    self.indice_exterior = indice_exterior
  
  def interactuar(self, foton):
    """
    Determina la interacción del foton con la interfase.
    
    Args:
        foton (SimulatedPhoton): Foton que interactua con la interfase.
    
    Returns:
        list, float: Punto de intersección.
        list, float: Vector normal a la superficie en el punto de intersección.
    """
    # Determinar puntos de interseccion y vector normal
    punto_interseccion, n = intersecion_foton_esfera(self.esfera, foton)
    # Determinar ángulo de incidencia
    
    # Determinar ángulo de refracción
    direccion_refract = refract(foton.dire, n, self.indice_exterior, self.esfera.indice_refraccion)
    direccion_reflect = reflect(foton.dire, n)
    teta_i = np.arccos(np.dot(direccion_reflect, n))
    teta_t = np.arccos(np.dot(direccion_refract, -n))
    
    # Determinar coeficiente de Fresnel
    Ru = fresnel(self.indice_exterior, self.esfera.indice_refraccion, teta_t, teta_i)
    
    