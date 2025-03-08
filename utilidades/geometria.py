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
      list, float: Punto de intersección.
  """
  origen = foton.pos
  direccion = foton.dir
  centro = esfera.centro
  radio = esfera.radio
  l = origen - centro
  a = np.dot(direccion, direccion)
  b = 2*np.dot(l, direccion)
  c = np.dot(l, l) - radio**2
  discriminante = b**2 - 4*a*c
  if discriminante < 0:
    return [0, 0, 0], [0, 0, 0]
  t0 = (-b - np.sqrt(discriminante)) / (2*a)
  t1 = (-b + np.sqrt(discriminante)) / (2*a)
  
  if foton.get_spa() != 0:
    # Caso dentro de la esfera
    t = t0 if np.abs(t0) > np.abs(t1) else t1
    p_interseccion = origen + t*direccion
    n = p_interseccion - centro
    # Cambiamos signo del vector normal
    n = -n / np.linalg.norm(n)
  elif foton.get_spa() == 0:
    t = t0 if np.abs(t0) < np.abs(t1) else t1
    t = t0 if np.abs(t0) > np.abs(t1) else t1
    p_interseccion = origen + t*direccion
    n = p_interseccion - centro
    n = n / np.linalg.norm(n)  
  return p_interseccion, n