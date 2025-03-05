import numpy as np

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
