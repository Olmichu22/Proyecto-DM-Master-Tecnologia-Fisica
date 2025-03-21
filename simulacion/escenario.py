class Escenario:
    """
    Define la disposición espacial de la esfera, el medio exterior, 
    la fuente de fotones, etc.
    """
    def __init__(self, estructuras, entorno, fuente_fotones):
        self.estructuras = estructuras
        self.fuente_fotones = fuente_fotones
        self.entorno = entorno

    def inicializar_fotones(self, config_fuente):
        """
        Genera un conjunto de fotones iniciales 
        a partir de la 'fuente_fotones'.
        """
        N_fotones = config_fuente["N_fotones"]
        mean_pos_x = config_fuente["mean_pos_x"]
        std_pos_x = config_fuente["std_pos_x"]
        mean_angle = config_fuente["mean_angle"]
        std_angle = config_fuente["std_angle"]
        reset = True if config_fuente["reset"] == "True" else False
        self.fuente_fotones.emitirN(N_fotones,
                                    mean_pos_x,
                                    std_pos_x,
                                    mean_angle,
                                    std_angle,
                                    reset)
        pass
