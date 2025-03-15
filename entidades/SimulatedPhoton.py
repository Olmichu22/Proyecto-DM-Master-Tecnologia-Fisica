import numpy as np
from entidades.estructura import Entorno

class SimulatedPhoton():
  """Clase que define un fotón simulado.
  """
  def __init__(self, n=0, pos=[0., 0., 0.], dire=[0., 0., 0.], l=None, estructura=Entorno(), lamda=532):
    """
    Args:
        n (int): Id del fotón. Defaults to 0.
        p (list, float): Posición del fotón. Defaults to [0., 0., 0.].
        d (list, float): Vector unitario de dirección del fotón. Defaults to [0., 0., 0.].
        l (_type_, optional): Camino óptico. Defaults to None.
        estructura (Estructura, optional): Estructura en la que está el fotón. Defaults to MixedComplexMaterial(nr=1, ni=0).
        lamda (int, optional): Longitud de onda del fotón. Defaults to 532.
    """
    self.n = n # Número de fotón
    self.pos = np.asarray(pos) # Posición
    dire = np.asarray(dire)/np.linalg.norm(dire)
    self.dire = dire # Direccion unitaria
    self.l = l # Camino óptico
    self.estructura = estructura # Mateiral en el que está
    self.lamda = lamda # Longitud de onda del fotón
    self.poshist = [(self.pos, self.estructura.ide)]
    self.dirhist = [self.dire]
    self.tot_dist = 0
  
  def actualizarPos(self, newPos):
    """Actualiza la posición del fotón.
    
    Args:
        newPos (list, float): Nueva posición del fotón.
    """
    self.pos = np.asarray(newPos)
    self.poshist.append((self.pos, self.estructura.ide))
    self.tot_dist += np.linalg.norm(self.poshist[-1][0] - self.poshist[-2][0])
  
  def actualizarDire(self, newDire):
    """Actualiza la dirección del fotón.
    
    Args:
        newDire (list, float): Nueva dirección del fotón.
    """
    self.dire = np.asarray(newDire)/np.linalg.norm(newDire)
    self.dirhist.append(self.dire)
  
  def getNumeroReflexionesInternas(self):
    """Calcula el número de reflexiones internas del foton"""
    count = 0
    for hist_el in self.poshist:
      count += hist_el[1]
    return count-1
  
  def getNumeroReflexiones(self):
    count = 0
    for hist_el in range(1, len(self.dirhist)):
      if np.dot(self.dirhist[hist_el], self.dirhist[hist_el-1]) < 0:
        count += 1
    return count
  
  # def alternarSpa(self):
  #   """Cambia el espacio del fotón.
  #   """
  #   self.spa = 1 - self.spa

  def __str__(self):
    return "Fotón con id " + str(self.n) + " en posición " + str(self.pos) + " y dirección " + str(self.dire) +"en estructura"+ str(self.estructura)
  
  def __repr__(self):
    return "Fotón(" + str(self.n) + "," + str(self.pos) + "," + str(self.dire) + "," + str(self.l) + "," + str(self.estructura) + ")"
  
    