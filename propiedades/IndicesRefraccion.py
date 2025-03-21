import numpy as np

class nCte:
  """ Clase que representa un índice de refracción constante """
  def __init__(self, n):
      self.n = n
  def calcular(self, lamda=0):
      return self.n
  def __str__(self):
      return "Índice de refracción constante: " + str(self.n)
  def __repr__(self):
      return "nCte(" + str(self.n) + ")"
  def __eq__(self, other):
      return self.n == other.n



class nComplex():
    """ Índice de refracción complejo 
    """
    def __init__(self, nr, ni):
        self.nr = nr
        self.ni = ni
        self.nc = complex(nr, ni)
    
    def calcular(self, lamda):
        return self.nr
    
    def alpha(self, lamda):
        alpha = self.ni*4*np.pi/lamda
        return alpha
    def __str__(self):
        return "Índice de refracción complejo: " + str(self.nr) + " + " + str(self.ni) + "i"
    def __repr__(self):
        return "nComplex(" + str(self.nr) + "," + str(self.ni) + ")"
    def __eq__(self, other):
        return self.nr == other.nr and self.ni == other.ni
    
    
    