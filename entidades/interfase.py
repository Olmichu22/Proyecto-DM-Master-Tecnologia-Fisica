from utilidades.optica import reflect, refract, fresnel
import numpy as np
from utilidades.aleatorios import UniformMontecarlo
from propiedades.IndicesRefraccion import nCte

class Interfase():
  """
  Representa la frontera entre dos medios.
  """
  def __init__(self, estructura, indice_exterior = nCte(1.0)):
    """
    Args:
        estructura (estructura): Estructura que representa la interfase.
        indice_exterior (float): Índice de refracción del medio exterior.
    """
    self.estructura = estructura
    self.indice_exterior = indice_exterior
    
  # Encapsulamos reflect y refract en la clase Interfase
  def reflect(self, foton, n):
    """
    Calcula la reflexión de un foton en la interfase.
    
    Args:
        foton (SimulatedPhoton): Foton que se refleja.
        n (list, float): Vector normal a la superficie.
    
    Returns:
        list, float: Dirección del foton reflejado.
    """
    return reflect(foton.dire, n)
  
  def refract(self, foton, n, indice_exterior, indice_interior):
    """
    Calcula la refracción de un foton en la interfase.
    
    Args:
        foton (SimulatedPhoton): Foton que se refracta.
        n (list, float): Vector normal a la superficie.
        indice_exterior (float): Índice de refracción del medio exterior.
        indice_interior (float): Índice de refracción del medio interior.
    
    Returns:
        list, float: Dirección del foton refractado.
    """
    return refract(foton.dire, n, indice_exterior, indice_interior)
    
  def indiceExterior(self, f=1000):
    """
    Calcula el índice de refracción del medio exterior.
    
    Args:
        f (float): Frecuencia de la luz.
    
    Returns:
        float: Índice de refracción del medio exterior.
    """
    return self.indice_exterior.calcular(f)
  
  def indiceInterior(self, f=1000):
    """
    Calcula el índice de refracción del medio interior.
    
    Args:
        f (float): Frecuencia de la luz.
    
    Returns:
        float: Índice de refracción del medio interior.
    """
    return self.estructura.material.indice_refraccion.calcular(f)  
  
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
    indice_refraccion = self.indiceInterior(foton.f)
    indice_refraccion_exterior = self.indiceExterior(foton.f)
    # Determinar ángulo de incidencia y refracción
    direccion_refract = self.refract(foton.dire, n, indice_refraccion_exterior, indice_refraccion)
    direccion_reflect = self.reflect(foton.dire, n)
    teta_i = np.arccos(np.dot(direccion_reflect, n))
    teta_t = np.arccos(np.dot(direccion_refract, -n))
    
    # Determinar coeficiente de Fresnel
    Ru = fresnel(indice_refraccion_exterior, indice_refraccion, teta_t, teta_i)
    
    reflexion =  UniformMontecarlo(Ru)
    if reflexion:
      foton.dire = direccion_reflect
    else:
      foton.dire = direccion_refract
    return foton
    
    