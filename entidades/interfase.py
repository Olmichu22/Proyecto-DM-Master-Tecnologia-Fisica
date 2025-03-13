from utilidades.optica import reflect, refract, fresnel
import numpy as np
from utilidades.aleatorios import UniformMontecarlo
from materiales.SimpleMaterial import MixedComplexMaterial
from propiedades.IndicesRefraccion import nComplex

class Interfase():
  """
  Representa la frontera entre dos medios.
  """
  def __init__(self, estructura_interior, material_exterior = MixedComplexMaterial()):
    """
    Args:
        estructura (estructura): Estructura que representa la interfase.
        indice_exterior (float): Índice de refracción del medio exterior.
    """
    self.estructura_interior = estructura_interior
    self.material_exterior = material_exterior
    
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
    
  def indiceExterior(self, lamda=1000):
    """
    Calcula el índice de refracción del medio exterior.
    
    Args:
        f (float): Frecuencia de la luz.
    
    Returns:
        float: Índice de refracción del medio exterior.
    """
    return self.material_exterior.indice_refraccion.calcular(lamda)
  
  def indiceInterior(self, lamda=1000):
    """
    Calcula el índice de refracción del medio interior.
    
    Args:
        f (float): Frecuencia de la luz.
    
    Returns:
        float: Índice de refracción del medio interior.
    """
    return self.estructura_interior.material.indice_refraccion.calcular(lamda)  
  
  def interactuar(self, n, foton, verbose=0):
    """
    Determina la interacción del foton con la interfase.
    
    Args:
        foton (SimulatedPhoton): Foton que interactua con la interfase.
        punto_incidencia (list, float): Punto de intersección.
        n (list, float): Vector normal a la superficie en el punto de intersección.
    
    Returns:
        
    """
    # Calcular índice de refracción (distinto para medios dispersivos)
    if foton.spa == 0:
      indice_destino = self.indiceInterior(foton.lamda)
      indice_origen = self.indiceExterior(foton.lamda)
    else:
      indice_destino = self.indiceExterior(foton.lamda)
      indice_origen =self.indiceInterior(foton.lamda)
    # Determinar ángulo de incidencia y refracción
    try:
      direccion_refract = self.refract(foton, n, indice_origen, indice_destino)
      direccion_reflect = self.reflect(foton, n)
    except Exception as e:
      if n[0] == n[1] & n[1] == n[2] & n[1] == 0:
        raise Exception("El vector normal es nulo")
      else:
        raise e
    teta_i = np.arccos(np.dot(direccion_reflect, n))
    teta_t = np.arccos(np.dot(direccion_refract, -n))
    
    # Determinar coeficiente de Fresnel
    Ru = fresnel(indice_origen, indice_destino, teta_t, teta_i)
    if verbose > 0:
      print(f" ni {indice_origen}, nt {indice_destino}")
      print(f"Ru {Ru}")
      print(f"tetai {teta_i} tetat {teta_t}")
    
    reflexion =  UniformMontecarlo(Ru)
    if reflexion:
      if verbose > 0:
        print(f"Fotón {foton.n} se refleja.")
      new_dire = direccion_reflect
      result = "reflect"
    else:
      if verbose > 0:
        print(f"Fotón {foton.n} se refracta.")
      new_dire = direccion_refract
      result = "refract"
    return new_dire, result
    
    