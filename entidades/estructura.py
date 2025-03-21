from utilidades.geometria import intersecion_foton_esfera
from materiales.SimpleMaterial import SimpleMaterial, MixedComplexMaterial
import numpy as np

class Estructura():
  def __init__(self, ide, material_int):
    self.ide = ide
    self.material_int = material_int
  
  def __eq__(self, other):
    return self.ide == other.ide
  
class Entorno(Estructura):
  """Clase que representa un entorno en el espacio tridimensional."""
  def __init__(self, ide=0, material=MixedComplexMaterial()):
    super().__init__(ide, material)
  
  def __str__(self):
    return "Entorno " + str(self.ide) + " con " + str(self.material_int)
  
  def __repr__(self):
    return "entorno(" + str(self.ide) + "," + str(self.material_int.indice_refraccion) + ")"

class Esfera(Estructura):
  """Clase que representa una esfera en el espacio tridimensional."""
  
  def __init__(self, ide = 1, centro = [0. ,0. ,0.], radio = 1, material_int = MixedComplexMaterial(), estructura_ext = Entorno()):
    """Constructor de la clase esfera.
    Args:
        centro (list, float): Centro de la esfera. Defaults to [0., 0., 0.].
        radio (float): Radio de la esfera. Defaults to 1.
        material (SimpleMaterial, optional): Material de la esfera. Defaults to SimpleMaterial.
    """
    super().__init__(ide, material_int)
    self.estructura_ext = estructura_ext
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
    return "Esfera " + str(self.ide) + " con centro " + str(self.centro) + ", radio " + str(self.radio) +" y " + str(self.material_int)
      
  def __repr__(self):
    return "esfera(" + str(self.ide) + "," + str(self.centro) + "," + str(self.radio) + "," + str(self.material_int.indice_refraccion) + ")"      
  
  def getPlotCoords(self, nPoints = 100):
    theta = np.linspace(0, 2*np.pi, nPoints)
    x = self.centro[0] + self.radio*np.cos(theta)
    y = self.centro[1] + self.radio*np.sin(theta)
    return x, y