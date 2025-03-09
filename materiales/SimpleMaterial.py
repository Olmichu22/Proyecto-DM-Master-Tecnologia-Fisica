from propiedades.IndicesRefraccion import nCte
class SimpleMaterial():
  
  def __init__(self, n = nCte(1.5)):
    """Constructor de la clase SimpleMaterial.

    Args:
        n (Function, optional): Función que calcule un índice de refracción dada f. Defaults to nCte(1.5).
    """
    self.indice_refraccion = n
    
  def __str__(self):
    return "Material con " + str(self.indice_refraccion)
  
  def __repr__(self):
    return "SimpleMaterial(" + str(self.indice_refraccion) + ")"
  
  def __eq__(self, other):
    return self.indice_refraccion == other.indice_refraccion