from propiedades.IndicesRefraccion import nCte, nComplex
from utilidades.optica import indiceEfectivo

class SimpleMaterial():
  
  def __init__(self, n = nCte(1.44)):
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
  

class MixedComplexMaterial():
  
  def __init__(self, n = [nComplex(1, 0)], fs = [1]):
    """Constructor de la clase MixedMaterial.

    Args:
        n (list, Function): Lista de funciones que calculan índices de refracción dada f.
    """
    self.indices_refraccion = n
    self.fs = fs
    # print(len(self.indices_refraccion), len(self.fs))
    self.indice_refraccion = self.compose()
  
  def compose(self):
    """Calcula el índice de refracción promedio de los índices de refracción de la lista.
    
    Returns:
        Function: Función que calcula el índice de refracción promedio.
    """
    self.indice_promedio = self.indices_refraccion[0]
    self.cum_fs = self.fs[0]
    for i, n in enumerate(self.indices_refraccion):
      if i == 0:
        continue
      nr, ni = indiceEfectivo(self.indice_promedio.nc, n.nc, self.cum_fs, self.fs[i])
      self.indice_promedio = nComplex(nr, ni)
      self.cum_fs += self.fs[i]
    return self.indice_promedio
  
  def alfa(self, lamda):
    """Calcula el coeficiente de absorción de la mezcla de materiales.

    Args:
        f (float): Frecuencia de la luz.

    Returns:
        float: Coeficiente de absorción.
    """
    return self.indice_refraccion.alpha(lamda)
  
  def __str__(self):
    return "Material con " + str(self.indice_refraccion)
  
  def __repr__(self):
    return "MixedComplexMaterial(" + str(self.indice_refraccion) + ")"
  
  def __eq__(self, other):
    return self.indice_refraccion == other.indice_refraccion