class esfera():
  """Clase que representa una esfera en el espacio tridimensional."""
  
  def __init__(self, centro = [0. ,0. ,0.], radio = 1, indice_refraccion = 1):
    """Constructor de la clase esfera.
    Args:
        centro (list, float): Centro de la esfera. Defaults to [0., 0., 0.].
        radio (float): Radio de la esfera. Defaults to 1.
    """
    self.centro = centro
    self.radio = radio
    self.indice_refraccion = indice_refraccion

  def __str__(self):
    return "Esfera con centro " + str(self.centro) + " y radio " + str(self.radio)
      
  def __repr__(self):
    return "esfera(" + str(self.centro) + "," + str(self.radio) + "," + str(self.indice_refraccion) + ")"      
      