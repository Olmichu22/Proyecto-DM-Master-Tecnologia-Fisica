from ..utilidades.geometria import intersecion_foton_esfera
from ..propiedades.IndicesRefraccion import nCte

class Estructura():
  def __init__(self, indice_refraccion):
    self.indice_refraccion = indice_refraccion

class Esfera(Estructura):
  """Clase que representa una esfera en el espacio tridimensional."""
  
  def __init__(self, centro = [0. ,0. ,0.], radio = 1, indice_refraccion = nCte(1.5)):
    """Constructor de la clase esfera.
    Args:
        centro (list, float): Centro de la esfera. Defaults to [0., 0., 0.].
        radio (float): Radio de la esfera. Defaults to 1.
        indice_refraccion (nCte, optional): Índice de refracción de la esfera. Defaults to nCte(1.5).
    """
    super().__init__(indice_refraccion)
    self.centro = centro
    self.radio = radio
    
  def interseccion(self, foton):
    return intersecion_foton_esfera(self, foton)

  def __str__(self):
    return "Esfera con centro " + str(self.centro) + " y radio " + str(self.radio)
      
  def __repr__(self):
    return "esfera(" + str(self.centro) + "," + str(self.radio) + "," + str(self.indice_refraccion) + ")"      
      