import numpy as np
import matplotlib.pyplot as plt


# Definición de la función de Snell
def snell(ni, nt, teta_i):
  """Calcula el ángulo de refracción usando la ley de Snell.

  Args:
      ni (float): Índice de refracción del medio incidente.
      nt (float): Índice de refracción del medio transmitido.
      teta_i (float): Ángulo de incidencia.

  Returns:
      teta_t: Ángulo de refracción.
      En caso de reflexión interna total, retorna None.
  """  """"""
  try:
      teta_t = np.arcsin(ni * np.sin(teta_i) / nt)
      return teta_t
  except ValueError:
      # Si el seno es mayor a 1, hay reflexión interna total
      return None  # Indica que no hay transmisión


def fresnel(ni, nt, teta_t, teta_i):
  """ Calcula el coeficiente de reflexión de Fresnel para ondas no polarizadas.

  Args:
      ni (float): Índice de refracción del medio incidente.
      nt (float): Índice de refracción del medio transmitido.
      teta_t (float): Ángulo de refracción.
      teta_i (float): Ángulo de incidencia.
  
  Returns:
    Ru  (float): Coeficiente de reflexión de Fresnel.
  """
    # Si hay reflexión interna total
  if teta_t is None:
      return 1
  Rs=((ni*np.cos(teta_i)-nt*np.cos(teta_t))/(ni*np.cos(teta_i)+nt*np.cos(teta_t)))**2
  Rp=((ni*np.cos(teta_t)-nt*np.cos(teta_i))/(ni*np.cos(teta_t)+nt*np.cos(teta_i)))**2
  Ru=(Rs+Rp)/2
  return Ru


def reflect(l=[0.,0.,0.], n=[0.,0.,0.]):
  """
  Reflexión de un vector sobre un plano definido por una normal.
  
  Args:
      l (list, float): Vector a reflejar. Defaults to [0.,0.,0.].
      n (list, float): Vector normal al plano de reflexión. Defaults to [0.,0.,0.].
  
  Returns:
      list, float: Vector reflejado.
  """
  return l + -2*np.dot(l,n)*n

def refract(l=[0.,0.,0.], n=[0.,0.,0.], n1=1., n2=1.):
  """
  Refracción de un vector a través de un plano definido por una normal.
  
  Args:
      l (list, float): Vector a refractar. Defaults to [0.,0.,0.].
      n (list, float): Vector normal al plano de refracción. Defaults to [0.,0.,0.].
      n1 (float, optional): Índice de refracción del medio 1. Defaults to 1..
      n2 (float, optional): Índice de refracción del medio 2. Defaults to 1..
  
  Returns:
      list, float: Vector refractado.
  """
  
  return n1/n2*l + (-n1/n2*np.dot(l,n)-np.sqrt(1-(n1/n2)**2*(1-np.dot(l,n)**2)))*n

def indiceEfectivo (nc1, nc2, f1, f2):
  """ Calcula el índice de refracción efectivo de una mezcla de dos materiales.

  Args:
      nc1 (complex): Índice de refracción del material 1.
      nc2 (complex): Índice de refracción del material 2.
      f1 (float): Proporción del material 1.
      f2 (float): Proporción del material 2.

  Returns:
      (complex, complex): Índice de refracción efectivo.
  """
  
  epsilon1 = (nc1)**2
  epsilon2 = (nc2)**2
  epsilon = f1*epsilon1 + f2*epsilon2
  n_ef = np.sqrt(np.real(epsilon))
  k_ef = np.sqrt(np.imag(epsilon))
  return n_ef, k_ef
