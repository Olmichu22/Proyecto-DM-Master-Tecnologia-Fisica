import numpy as np

class nCte:
  """ Clase que representa un índice de refracción constante """
  def __init__(self, n):
      self.n = n
  def calcular(self, f=0):
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
    
    def calcular(self, f):
        return self.nr
    
    def alpha(self, f):
        lambda_ = 3e8/f
        alpha = self.ni*2*np.pi/lambda_
        return alpha
    
    
    
    