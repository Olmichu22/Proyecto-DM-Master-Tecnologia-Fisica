import numpy as np

class SimulatedPhoton():
  """Clase que define un fotón simulado.
  """
  def __init__(self, n= 0, pos = [0., 0., 0.], dire = [0., 0., 0.], l = None, spa = 0):
    """
    Args:
        n (int): Id del fotón. Defaults to 0.
        p (list, float): Posición del fotón. Defaults to [0., 0., 0.].
        d (list, float): Vector unitario de dirección del fotón. Defaults to [0., 0., 0.].
        l (_type_, optional): Camino óptico. Defaults to None.
        spa (int, optional): Espacio del fotón. Defaults to 0.
    """
    self.n = n # Número de fotón
    self.pos = pos # Posición
    dire = dire/np.linalg.norm(dire)
    self.dire = dire # Direccion unitaria
    self.l = l # Camino óptico
    self.spa = spa # Espacio en el que está
  
  def set_pos(self, pos):
    self.pos = pos
    
  def set_dir(self, dire):
    self.dire = dire
  
  def set_l(self, l):
    self.l = l
  
  def set_spa(self, spa):
    self.spa = spa
  
  def get_pos(self):
    return self.pos
  
  def get_dir(self):
    return self.dire
  
  def get_l(self):
    return self.l
  
  def get_spa(self):
    return self.spa
  
  def get_n(self):
    return self.n
    