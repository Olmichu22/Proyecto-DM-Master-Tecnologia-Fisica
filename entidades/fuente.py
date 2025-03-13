from entidades.SimulatedPhoton import SimulatedPhoton
from utilidades.aleatorios import GenerateRandomNormalPosition2D
from entidades.estructura import Entorno
import numpy as np

class Fuente():
  def __init__(self, lamda):
      self.lamda = lamda
      self.fotones = []
      self.nfotones = len(self.fotones)


class FuenteMonocromatica(Fuente):
  def __init__(self, lamda=1000, origen=0, dispersion_pos=GenerateRandomNormalPosition2D, dispersion_ang=None, estructura = Entorno()):
    """Constructor de la clase FuenteMonocromaticaNormal.
    Fuente de fotones monocromáticos con posición y dirección dada por una distribución.
    Args:
      lamda (_type_): Longitud de onda de los fotones.
      origen (int, optional): Origen de los fotones. Defaults to 0.
      dispersion_pos (function, optional): Función para calcular la dispersión en la coordenada x. Defaults to GenerateRandomNormalPosition2D.
      dispersion_ang (function, optional): Función para calcular la dispersión en el ángulo. Defaults to None.
      estructura (Estructura, optional): Estructura en la que están los fotones generados por la fuente. Defaults to Entorno().  
    """
    super().__init__(lamda)
    self.origen = origen
    self.dispersion_pos = dispersion_pos
    self.dispersion_ang = dispersion_ang
    self.estructura = estructura

  def emitir(self, n, mean_pos=0, std_pos=5, mean_ang=np.pi/2, std_ang=np.pi/4, reset = True):
    """ Emite un fotón en la posición y dirección dadas.
    Args:
        n (int): Id del fotón.
        mean_pos (float): Media de la posición.
        std_pos (float): Desviación estándar de la posición.
        mean_ang (float): Media del ángulo.
        std_ang (float): Desviación estándar del ángulo.
    """ 
    if reset: 
      self.fotones = []
      self.nfotones = len(self.fotones)
  
    # Calcular posición y dirección del fotón
    if self.dispersion_pos:
      pos = self.dispersion_pos(self.origen, mean_pos, std_pos)
    else:
      pos = [mean_pos, self.origen, 0]
    if self.dispersion_ang:
      ang = self.dispersion_ang(mean_ang, std_ang)
    else:
      ang = mean_ang
      
    dire = [np.cos(ang), np.sin(ang), 0]
    foton = SimulatedPhoton(n, pos, dire, estructura= self.estructura, lamda=self.lamda)
    self.fotones.append(foton)
    return foton
  
  def emitirN(self, N, mean_pos=0, std_pos=5, mean_ang=np.pi/2, std_ang=np.pi/4, reset=True):
    """ Genera N fotones desde la fuente.
    Args:
        N (int): Número de fotones a generar.
        mean_pos (int, optional): Posición central de generación. Defaults to 0.
        std_pos (int, optional): Desviación de la posición de generación. Si es uniforme, rango a izquierda y derecha. Defaults to 5.
        mean_ang (float, optional): Ángulo (rad) central de generación. Defaults to np.pi/2.
        std_ang (float, optional): Desviación del ángulo (rad) de generación. Defaults to np.pi/4.
        reset (bool, optional): Reinica el contador de fotones. Defaults to True.

    Returns:
        list: Lista de los fotones generados como SimulatedPhoton.
    """
    if reset:
      self.fotones = []
      self.nfotones = len(self.fotones)
    for i in range(N):
      self.emitir(i+self.nfotones+1, mean_pos, std_pos, mean_ang, std_ang, reset=False)
    return self.fotones