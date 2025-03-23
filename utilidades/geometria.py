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
  if discriminante <= 0:
    return [None, None, None], [None, None, None]
  t0 = (-b - np.sqrt(discriminante)) / (2*a)
  t1 = (-b + np.sqrt(discriminante)) / (2*a)
  # Mantenemos el t positivo más pequeño
  # print(t0, t1)
  if t1 <= 1e-5 and t0 <= 1e-5:
    return [None, None, None], [None, None, None]
  
  if t1 > 1e-5 and t0 > 1e-5:
    t = min(t1, t0) 
  else:
    t = t0 if t1 <= 1e-5 else t1
  
  p_interseccion = origen + t*direccion
  n = p_interseccion - centro
  n = n / np.linalg.norm(n)
  if foton.estructura == esfera:
    n = -n
  return p_interseccion, n


def generate_spheres(n, radio, x_min, x_max, y_min=50, y_max=20000, y_fixed=False):
    """
    Genera n esferas con centros (x, y, 0) tales que:
      - x está entre x_min y x_max.
      - y está entre y_min y y_max (con y_min >= 50).
      - Los centros no están tan próximos: la distancia entre dos centros >= 2 * radius.
    """
    centros = []  # Lista de centros (x, y, z)
    attempts = 0
    max_attempts = n * 1000  # Límite para evitar bucles infinitos

    while len(centros) < n and attempts < max_attempts:
        attempts += 1
        
        # Generamos coordenadas aleatorias dentro de los límites
        x = np.random.uniform(x_min, x_max)
        if y_fixed:
            y = y_min
        else:
            y = np.random.uniform(y_min, y_max)
        z = 0  # En el plano z = 0
        
        new_center = (x, y, z)
        
        # Verificamos que la nueva esfera no se solape con ninguna ya generada
        overlap = False
        for cx, cy, cz in centros:
            distance = np.linalg.norm(np.array(new_center) - np.array((cx, cy, cz)))
            if distance < 2.2 * radio:
                overlap = True
                break
        
        if not overlap:
            centros.append(new_center)

    if len(centros) < n:
        print("No se pudieron generar todas las esferas sin superposición.")
    return centros