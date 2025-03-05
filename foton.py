class foton():
  def __init__(self, n= 0, p = [0., 0., 0.], d = [0., 0., 0.], l = None, spa = 0):
    """

    Args:
        n (int): Id del fotón. Defaults to 0.
        p (list, float): Posición del fotón. Defaults to [0., 0., 0.].
        d (list, float): Vector unitario de dirección del fotón. Defaults to [0., 0., 0.].
        l (_type_, optional): Camino óptico. Defaults to None.
        spa (int, optional): Espacio del fotón. Defaults to 0.
    """    """"""
    self.n = n # Número de fotón
    self.p = p # Posición
    self.d = d # Direccion unitaria
    self.l = l # Camino óptico
    self.spa = spa # Espacio en el que está
  
  def set_p(self, p):
    self.p = p
    
  def set_d(self, d):
    self.d = d
  
  def set_l(self, l):
    self.l = l
  
  def set_spa(self, spa):
    self.spa = spa
  
  def get_p(self):
    return self.p
  
  def get_d(self):
    return self.d
  
  def get_l(self):
    return self.l
  
  def get_spa(self):
    return self.spa
  
  def get_n(self):
    return self.n
    