import numpy as np
from entidades.interfase import interactuar_interfase
from utilidades.aleatorios import probAbs
class Trazador:
    """
    Lógica de propagación de los fotones, interacción con la interfase, 
    absorción, etc.
    """
    def __init__(self, escenario, d_arbitraria_ampliacion):
        self.escenario = escenario
        self.d_arbitraria_ampliacion = d_arbitraria_ampliacion
        self.fotones_absorbidos = []
        self.fotones_inactivos = []
        self.n_abs = 0

    def propagar(self, foton):
        """
        Mueve un fotón paso a paso hasta que:
        - Se absorbe,
        - Sale del dominio de la simulación,
        - O se cumplen las condiciones de parada.
        """
        while True:
            min_pint, min_n = [None, None, None], None
            estructura_interaccion = None
            for i, estructura in enumerate(self.escenario.estructuras):
                p_int, n = estructura.interseccion(foton)
                if p_int[0]==None:
                    continue
                
                if min_pint[0] == None:
                    min_pint = p_int
                    min_n = n
                    estructura_interaccion = estructura
                elif np.linalg.norm(foton.pos - p_int) < np.linalg.norm(foton.pos - min_pint):
                    min_pint = p_int
                    min_n = n
                    estructura_interaccion = estructura
                    
                    
            if min_pint[0] == None:
                foton.actualizarPos(foton.pos+foton.dire*self.d_arbitraria_ampliacion)
                self.fotones_inactivos.append(foton)
                break
            
            # Comprobamos si se absorbe antes de interaccionar con una interfase
            l_pos = np.linalg.norm(min_pint-foton.pos)
            alfa = foton.estructura.material_int.alfa(foton.lamda)
            absorbido, labs = probAbs(l_pos, alfa)
            if absorbido:
                # print("\n")
                # print("Fotón no absborbido")
                # print("Estado final ", f)
                self.n_abs += 1
                foton.actualizarPos(foton.pos + foton.dire*labs)
                self.fotones_inactivos.append(foton)
                self.fotones_absorbidos.append(foton)
                break
            
            # Si no es absorbido, calculamos la interacción con la interfase
            try:
                if foton.estructura != estructura_interaccion:
                    # print("Foton fuera de la esfera")
                    estructura_foton = estructura_interaccion.estructura_ext
                    # print(estructura.estructura_ext)
                    estructura_transmitida = estructura_interaccion
                    # print(estructura_transmitida)
                else:
                # print("Foton dentro de la esfera")
                    estructura_foton = estructura_interaccion
                    estructura_transmitida = estructura_interaccion.estructura_ext
            
                n_foton = estructura_foton.material_int.indice_refraccion.calcular(foton.lamda)
                n_trans = estructura_transmitida.material_int.indice_refraccion.calcular(foton.lamda)

                new_dire, result = interactuar_interfase(min_n, foton, n_foton=n_foton, n_t = n_trans)
            except Exception as e:

                raise Exception("Error")
            
            # Si se refleja cambiamos su posición y dirección
            if result == "reflect":

                foton.actualizarPos(min_pint)
                foton.actualizarDire(new_dire)
                continue
            
            # Si se refracta cambiamos su posición, dirección y espacio en el que está
            if result == "refract":
                foton.actualizarPos(min_pint)
                foton.actualizarDire(new_dire)
                foton.estructura = estructura_transmitida
                continue
        pass

    def ejecutar(self, reset=False):
        """
        Ejecuta la simulación completa (propaga todos los fotones).
        Retorna algún objeto con la información final (estadísticas, etc.)
        """
        if reset:
            self.fotones_absorbidos = []
            self.fotones_inactivos = []
            self.n_abs = 0
        fotones = self.escenario.fuente_fotones.fotones
        for foton in fotones:
            self.propagar(foton)
        return self.fotones_absorbidos, self.fotones_inactivos, fotones
