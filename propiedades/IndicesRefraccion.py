class nCte:
  """ Clase que representa un índice de refracción constante """
  def __init__(self, n):
      self.n = n
  def calcular(self, f):
      return self.n
  def __str__(self):
      return "Índice de refracción constante: " + str(self.n)
  def __repr__(self):
      return "nCte(" + str(self.n) + ")"
  def __eq__(self, other):
      return self.n == other.n