class Escenario:
    """
    Define la disposición espacial de la esfera, el medio exterior, 
    la fuente de fotones, etc.
    """
    def __init__(self, esfera, fuente_fotones, interfase):
        self.esfera = esfera
        self.fuente_fotones = fuente_fotones
        self.indice_medio_exterior = interfase

    def inicializar_fotones(self):
        """
        Genera un conjunto de fotones iniciales 
        a partir de la 'fuente_fotones'.
        """
        # Por ejemplo, si la fuente se modela como un haz o una 
        # distribución isotrópica, se instancia aquí.
        pass
