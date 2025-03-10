import numpy as np

def intersecion_foton_esfera(esfera, foton):
  """
  Calcula la intersección de una recta con una esfera.
  
  Args:
      centro (list, float): Centro de la esfera.
      radio (float): Radio de la esfera.
      origen (list, float): Origen de la recta.
      direccion (list, float): Dirección de la recta.
  
  Returns:
      (tuple, list | list): Punto de intersección y vector normal.
  """
  origen = foton.pos
  direccion = foton.dire
  centro = esfera.centro
  radio = esfera.radio
  l = origen - centro
  a = np.dot(direccion, direccion)
  b = 2*np.dot(l, direccion)
  c = np.dot(l, l) - radio**2
  discriminante = b**2 - 4*a*c
  if discriminante < 0:
    return [None, None, None], [None, None, None]
  t0 = (-b - np.sqrt(discriminante)) / (2*a)
  t1 = (-b + np.sqrt(discriminante)) / (2*a)
  
  if foton.spa != 0:
    # Caso dentro de la esfera
    t = t0 if np.abs(t0) > np.abs(t1) else t1
    p_interseccion = origen + t*direccion
    n = p_interseccion - centro
    # Cambiamos signo del vector normal
    n = -n / np.linalg.norm(n)
  elif foton.spa == 0:
    t = t0 if np.abs(t0) < np.abs(t1) else t1
    p_interseccion = origen + t*direccion
    n = p_interseccion - centro
    n = n / np.linalg.norm(n)  
    if np.dot(n, direccion) > 0:
      return [None, None, None], n
  return p_interseccion, n