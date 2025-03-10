import numpy as np

class SimulatedPhoton():
  """Clase que define un fotón simulado.
  """
  def __init__(self, n=0, pos=[0., 0., 0.], dire=[0., 0., 0.], l=None, spa=0, f=430e12):
    """
    Args:
        n (int): Id del fotón. Defaults to 0.
        p (list, float): Posición del fotón. Defaults to [0., 0., 0.].
        d (list, float): Vector unitario de dirección del fotón. Defaults to [0., 0., 0.].
        l (_type_, optional): Camino óptico. Defaults to None.
        spa (int, optional): Espacio del fotón. Defaults to 0.
    """
    self.n = n # Número de fotón
    self.pos = np.asarray(pos) # Posición
    dire = np.asarray(dire)/np.linalg.norm(dire)
    self.dire = dire # Direccion unitaria
    self.l = l # Camino óptico
    self.spa = spa # Espacio en el que está
    self.f = f # Frecuencia del fotón
    self.poshist = [(self.pos, self.spa)]
    self.dirhist = [self.dire]
  
  def actualizarPos(self, newPos):
    """Actualiza la posición del fotón.
    
    Args:
        newPos (list, float): Nueva posición del fotón.
    """
    self.pos = np.asarray(newPos)
    self.poshist.append((self.pos, self.spa))
  
  def actualizarDire(self, newDire):
    """Actualiza la dirección del fotón.
    
    Args:
        newDire (list, float): Nueva dirección del fotón.
    """
    self.dire = np.asarray(newDire)/np.linalg.norm(newDire)
    self.dirhist.append(self.dire)
  
  def getNumeroReflexiones(self):
    """Calcula el número de reflexiones internas del foton"""
    count = 0
    for hist_el in self.poshist:
      count += hist_el[1]
    return count-1
  
  def alternarSpa(self):
    """Cambia el espacio del fotón.
    """
    self.spa = 1 - self.spa

  def __str__(self):
    return "Fotón con id " + str(self.n) + " en posición " + str(self.pos) + " y dirección " + str(self.dire)
  
  def __repr__(self):
    return "Fotón(" + str(self.n) + "," + str(self.pos) + "," + str(self.dire) + "," + str(self.l) + "," + str(self.spa) + ")"
  
    