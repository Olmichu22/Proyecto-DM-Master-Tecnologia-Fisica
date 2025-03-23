import time
from entidades.estructura import Esfera, Entorno
from entidades.fuente import FuenteMonocromatica
from materiales.SimpleMaterial import MixedComplexMaterial
from propiedades.IndicesRefraccion import nComplex
from utilidades.aleatorios import *
from utilidades.geometria import generate_spheres
from simulacion.escenario import Escenario
from simulacion.trazador import Trazador

def setup_experiment(config):
  config_estructuras = config["estructuras"]
  config_fotones = config["fotones"]
  config_entorno = config["entorno"]
  entorno = set_up_entorno(config_entorno)
  estructuras = set_up_estructuras(config_estructuras, entorno)
  fuente = set_up_fuente(config_fotones, entorno)
  return fuente, entorno, estructuras

# Función auxiliar que realiza UNA repetición del experimento para un valor específico de N fotones.
def process_repetition(config_emision_fuente, estructuras, entorno, fuente, d_arbitraria_ampliacion):
  # Crear instancias propias para evitar conflictos en paralelo
  escenario = Escenario(estructuras, entorno, fuente)
  trazador = Trazador(escenario, d_arbitraria_ampliacion)
  
  time_start = time.time()
  trazador.escenario.inicializar_fotones(config_emision_fuente)
  fotones_absorbidos, fotones_inactivos, fotones, fotones_int = trazador.ejecutar(reset=True)
  time_end = time.time()
  
  elapsed = time_end - time_start
  abs_fraction = len(fotones_absorbidos) / (fotones_int + 1e-6)
  
  return {"elapsed": elapsed, "abs_fraction": abs_fraction, "nfotones_absorbidos": len(fotones_absorbidos), "N_fotones": len(fotones), "N_fotones_int": fotones_int, "Fotones inactivos": fotones_inactivos} 

def set_up_fuente(config, entorno):
  """Configura la fuente de fotones.

  Args:
      config (dict): Configuración de la fuente.
      entorno (Estructura): Estructura que representa el entorno.
  Returns:
      Fuente: Fuente de fotones.
  """
  lamda = config.get("lamda", 532)
  origen = config.get("origen", 0)
  dispersion_pos = config.get("dispersion_pos", "uniform")
  dispersion_ang = config.get("dispersion_ang", "uniform")
  
  dispersion_pos_func = None
  if dispersion_pos == "uniform":
    dispersion_pos_func = GenerateRandomUniformPosition2D
  elif dispersion_pos == "normal":
    dispersion_pos_func = GenerateRandomNormalPosition2D
  else:
    raise Exception("Función de dispersión de posición no válida")
  dispersion_ang_func = None
  if dispersion_ang == "uniform":
    dispersion_ang_func = GenerateRandomUniformAngle
  elif dispersion_ang == "normal":
    dispersion_ang_func = GenerateRandomNormalAngle
  else:
    raise Exception("Función de dispersión de ángulo no válida")
  
  fuente = FuenteMonocromatica(lamda,
                               origen,
                               dispersion_pos_func,
                               dispersion_ang_func,
                               entorno)
  return fuente  

def set_up_entorno(config):
  """Configura el entorno del experimento.

  Args:
      config (dict): Configuración del entorno.
  Returns:
      Estructura: Entorno del experimento.
  """
  n_entorno_config = config.get("n_entorno", {"nr":1, "ni":0})
  n_entorno = nComplex(n_entorno_config["nr"], n_entorno_config["ni"])
  material_entorno = MixedComplexMaterial(n=[n_entorno], fs=[1])
  entorno = Entorno(ide = 0, material = material_entorno)
  return entorno

def set_up_estructuras(config, entorno):
  """Configura las estructuras del experimento.

  Args:
      config (dict): Configuración de las estructuras.
      entorno (Estructura): Estructura que representa el entorno.

  Returns:
      List: Lista de estructuras.
  """
  n_estructuras = config["n_estructuras"]
  # Obtenemos las estructuras anidadas si existen
  estructuras_anidadas = config.get("estructuras_anidadas")
  estructuras_aisladas = config.get("estructuras_aisladas")
  estructuras = []
  
  max_x = config.get("max_x")
  min_x = config["min_x"]
  max_y = config.get("max_y")
  min_y = config["min_y"]
  y_fixed = config.get("y_fixed", False)
  
  # Configuración de estructuras anidadas
  if estructuras_anidadas:
    # Obtenemos los parámetros de las estructuras anidadas
    radio_ext = estructuras_anidadas["radio_ext"]
    espesor = estructuras_anidadas["espesor"]
    radio_int = radio_ext-espesor
    nr_ints = estructuras_anidadas["nr_int_list"] # Lista parte real del indice interno
    ni_ints = estructuras_anidadas["ni_int_list"] # Lista parte imaginaria del indice interno
    fs_ints = estructuras_anidadas["fs_int_list"] # Lista fracción de volumen de cada material
    nr_exts = estructuras_anidadas["nr_ext_list"] # Lista parte real del indice externo
    ni_exts = estructuras_anidadas["ni_ext_list"] # Lista parte imaginaria del indice externo
    fs_exts = estructuras_anidadas["fs_ext_list"] # Lista fracción de volumen de cada material
    
    # Declaramos los índices de regracción
    n_ints = []
    for ns in range(len(nr_ints)):
      n_ints.append(nComplex(nr_ints[ns], ni_ints[ns]))
    n_exts = []
    for ns in range(len(nr_exts)):
      n_exts.append(nComplex(nr_exts[ns], ni_exts[ns]))

    material_int = MixedComplexMaterial(n=n_ints, fs=fs_ints)
    material_ext = MixedComplexMaterial(n=n_exts, fs=fs_exts)
    
    if n_estructuras == 1:
      estructura_ext = Esfera(1, np.array([min_x, min_y, 0]), radio_ext, material_int = material_ext, estructura_ext=entorno)
      estructura_int = Esfera(2, np.array([min_x, min_y, 0]), radio_int, material_int = material_int, estructura_ext=estructura_ext)
      
      estructuras.append(estructura_int)
      estructuras.append(estructura_ext)
    else:
      centros = generate_spheres(n_estructuras, radio_ext, min_x, max_x, min_y, max_y, y_fixed)
      for i in range(n_estructuras):
        estructura_ext = Esfera(i+1, centros[i], radio_ext, material_int = material_ext, estructura_ext=entorno)
        estructura_int = Esfera(n_estructuras+i+1, centros[i], radio_int, material_int = material_int, estructura_ext=estructura_ext)
        estructuras.append(estructura_ext)
        estructuras.append(estructura_int)
        
  # Configuración de estructuras aisladas
  elif estructuras_aisladas:
    # Obtenemos los parámetros de las estructuras aisladas
    radio = estructuras_aisladas["radio"]
    nrs = estructuras_aisladas["nr_list"]
    nis = estructuras_aisladas["ni_list"]
    fss = estructuras_aisladas["fs_list"]
    n = []
    for ns in range(len(nrs)):
        n.append(nComplex(nrs[ns], nis[ns]))
    material = MixedComplexMaterial(n=n, fs=fss)
    # Creamos las estructuras
    if n_estructuras == 1:
      estructura = Esfera(1, np.array([min_x, min_y, 0]), radio, material_int = material, estructura_ext=entorno)
      estructuras.append(estructura)
    else:
      centros = generate_spheres(n_estructuras, radio, min_x, max_x, min_y, max_y, y_fixed)
      for i in range(n_estructuras):
        estructura = Esfera(i+1, centros[i], radio, material_int = material, estructura_ext=entorno)
        estructuras.append(estructura)
  else:
    raise Exception("No se ha especificado el tipo de estructuras a crear")
  return estructuras