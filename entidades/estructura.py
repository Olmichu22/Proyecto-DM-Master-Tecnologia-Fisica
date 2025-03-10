from utilidades.geometria import intersecion_foton_esfera
from materiales.SimpleMaterial import SimpleMaterial
import numpy as np

class Estructura():
  def __init__(self, material):
    self.material = material

class Esfera(Estructura):
  """Clase que representa una esfera en el espacio tridimensional."""
  
  def __init__(self, centro = [0. ,0. ,0.], radio = 1, material = SimpleMaterial()):
    """Constructor de la clase esfera.
    Args:
        centro (list, float): Centro de la esfera. Defaults to [0., 0., 0.].
        radio (float): Radio de la esfera. Defaults to 1.
        material (SimpleMaterial, optional): Material de la esfera. Defaults to SimpleMaterial.
    """
    super().__init__(material)
    self.centro = np.asarray(centro)
    self.radio = radio
    
  def interseccion(self, foton):
    """Calcula la intersección de un foton
    con la esfera.

    Args:
        foton (SimulatedPhoton): Foton que se intersecta con la esfera.

    Returns:
        (tuple, list|list): Punto de intersección y vector normal.
    """
    return intersecion_foton_esfera(self, foton)

  def __str__(self):
    return "Esfera con centro " + str(self.centro) + ", radio " + str(self.radio) +" y " + str(self.material)
      
  def __repr__(self):
    return "esfera(" + str(self.centro) + "," + str(self.radio) + "," + str(self.material.indice_refraccion) + ")"      
  
  def getPlotCoords(self, nPoints = 100):
    theta = np.linspace(0, 2*np.pi, nPoints)
    x = self.centro[0] + self.radio*np.cos(theta)
    y = self.centro[1] + self.radio*np.sin(theta)
    return x, y