import numpy as np

def UniformMontecarlo(prob):
    """
    Método de Montecarlo para generar eventos con probabilidad uniforme.
    
    Args:
        prob (float): Probabilidad de que ocurra el evento.
        
    Returns:
        bool: True si el evento ocurre, False en caso contrario.
    """
    return np.random.rand() < prob

def GenerateRandomNormalPosition2D(origen, mean, std):
    """
    Genera un vector 3D en la coordenada de origen Y con componente X aleatoria y Z = 0.
    
    Args:
        origen (float): Coordenada de origen Y.
        mean (float): Media de la distribución.
        std (float): Desviación estándar de la distribución.
        
        
    Returns:
        float: Vector 3D con componentes aleatorias (z = 0).
    """
    return [np.random.normal(mean, std), origen , 0]

def GenerateRandomUniformPosition2D(origen, mean, std):
    """
    Genera un vector 3D en la coordenada de origen Y con componente X aleatoria y Z = 0.
    Se genera una coordenada X aleatorio en el intervalo [mean - std, mean + std].
    
    Args:
        origen (float): Coordenada de origen Y.
        min (float): Valor mínimo de la distribución.
        max (float): Valor máximo de la distribución.
        
        
    Returns:
        float: Vector 3D con componentes aleatorias (z = 0).
    """
    min_point = mean - std
    max_point = mean + std
    return [np.random.uniform(min_point, max_point), origen , 0]

def GenerateRandomNormalAngle(mean, std):
    """
    Genera un ángulo aleatorio a partir de una distribución normal.
    
    Args:
        mean (float): Media de la distribución.
        std (float): Desviación estándar de la distribución.
        
    Returns:
        float: Ángulo aleatorio.
    """
    return np.random.normal(mean, std)

def GenerateRandomUniformAngle(mean, std):
    """
    Genera un ángulo aleatorio a partir de una distribución uniforme.
    Se genera un ángulo aleatorio en el intervalo [mean - std, mean + std].
    
    Args:
        mean (float): Media de la distribución.
        std (float): Desviación estándar de la distribución.
        
        
    Returns:
        float: Ángulo aleatorio.
    """
    min_point = mean - std
    max_point = mean + std
    return np.random.uniform(min_point, max_point)

def GenExpMonteCarlo(mu):
  return -np.log(np.random.rand())/mu
  

import warnings

def probAbs(l, mu = 0.1):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        labs = GenExpMonteCarlo(mu)
    # print("L absorcion", labs)
    # print("L recorrida", l)
    # print("\n")
    if labs > l:
        return False, labs
    else:
        return True, labs
  