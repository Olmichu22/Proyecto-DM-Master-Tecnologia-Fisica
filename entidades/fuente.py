from entidades.SimulatedPhoton import SimulatedPhoton
from utilidades.aleatorios import GenerateRandomNormalPosition2D
import numpy as np

class Fuente():
  def __init__(self, frecuencia):
      self.frecuencia = frecuencia
      self.fotones = []


class FuenteMonocromatica(Fuente):
  def __init__(self, frecuencia=1000, origen=0, dispersion_pos=GenerateRandomNormalPosition2D, dispersion_ang=None):
    """Constructor de la clase FuenteMonocromaticaNormal.
    Fuente de fotones monocromáticos con posición y dirección dada por una distribución.
    Args:
        frecuencia (_type_): Frecuencia de los fotones.
        origen (int, optional): Origen de los fotones. Defaults to 0.
        dispersion_pos (function, optional): Función para calcular la dispersión en la coordenada x. Defaults to GenerateRandomNormalPosition2D.
        dispersion_ang (function, optional): Función para calcular la dispersión en el ángulo. Defaults to None.
    """
    super().__init__(frecuencia)
    self.origen = origen
    self.dispersion_pos = dispersion_pos
    self.dispersion_ang = dispersion_ang

  def emitir(self, n, mean_pos=0, std_pos=5, mean_ang=np.pi/2, std_ang=np.pi/4):
    """ Emite un fotón en la posición y dirección dadas.
    Args:
        n (int): Id del fotón.
        mean_pos (float): Media de la posición.
        std_pos (float): Desviación estándar de la posición.
        mean_ang (float): Media del ángulo.
        std_ang (float): Desviación estándar del ángulo.
    """ 
    # Calcular posición y dirección del fotón
    if self.dispersion_pos:
      pos = self.dispersion_pos(self.origen, mean_pos, std_pos)
    else:
      pos = [mean_pos, self.origen, 0]
    if self.dispersion_ang:
      ang = self.dispersion_ang(mean_ang, std_ang)
    else:
      ang = mean_ang
      
    dire = [np.sin(ang), np.cos(ang), 0]
    foton = SimulatedPhoton(n, pos, dire, f=self.frecuencia)
    self.fotones.append(foton)
    return foton
  
  def emitirN(self, N, mean_pos=0, std_pos=5, mean_ang=np.pi/2, std_ang=np.pi/4):
    """ Emite N fotones en la posición y dirección dadas."""
    for i in range(N):
      self.emitir(i, mean_pos, std_pos, mean_ang, std_ang)
    return self.fotones