
import numpy as np
import yaml
import argparse
import os
from pprint import pprint
from concurrent.futures import ProcessPoolExecutor, as_completed
import tqdm
from simulacion.utilidades import *
from utilidades.graficar import *

def parse_param(valor):
    if isinstance(valor, str):
        valor = valor.replace("pi", "np.pi")
        return eval(valor, {"__builtins__": None, "np": np})
    return valor


# INPUT ARGPARSE DATA
parser = argparse.ArgumentParser(description='Simulación de fotones en esferas')
parser.add_argument("-c", '--configPath', type=str, default='configs/experiment_configs', help='Directorio de los archivos de configuración para los experimentos')
parser.add_argument("-n", '--n_reps', type=int, default=5, help='Número de repeteciones para cada experimento')
parser.add_argument("-j", '--n_jobs', type=int, default=8, help='Número de trabajos en paralelo')
parser.add_argument("-o", '--outputPath', type=str, default='results', help='Directorio de salida para los resultados')
parser.add_argument("-t", "--test", default="False", type=str, help='Ejecutar en modo test')
parser.add_argument("-g", "--graph", default="False", type=str, help='Generar gráficos')
args = parser.parse_args()

configPath = args.configPath
n_reps = args.n_reps
n_jobs = args.n_jobs
outputPath = args.outputPath
test = args.test
test = True if test == "True" else False
graph = args.graph
graph = True if graph == "True" else False

if not os.path.exists(configPath):
  raise Exception(f"El directorio {configPath} no existe")

n_experiments = len(os.listdir(configPath))

if n_experiments == 0:
  raise Exception(f"No hay archivos de configuración en el directorio {configPath}")

configs = []
# Cargamos archivos .yaml o .yml
files = [f for f in os.listdir(configPath) if f.endswith('.yaml') or f.endswith('.yml')]
if len(files) == 0:
  raise Exception(f"No hay archivos de configuración en el directorio {configPath}") 

for exp in files:
  with open(f'{configPath}/{exp}') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
    configs.append(config)  
    
# Generamos directorios de salida
config_dir = configPath.split("/")[-1]
if config_dir == "":
  config_dir = configPath.split("/")[-2]
  
outputPath = f"{outputPath}/{config_dir}"
configOutPath = f"{outputPath}/configurations"

if graph:
  graphPath = f"{outputPath}/plots"
  if not os.path.exists(graphPath):
    os.makedirs(graphPath)


if not os.path.exists(outputPath):
  os.makedirs(outputPath)

if not os.path.exists(configOutPath):
  os.makedirs(configOutPath)

print("========================================")
print(f"Se van a realizar {n_experiments} experimentos")
print(f"Se van a realizar {n_reps} repeticiones por experimento")
print(f"Se van a realizar {n_jobs} trabajos en paralelo")
print("========================================")

results = {}

for i, config in enumerate(configs):
  print(f"Experimento {i+1}:")
  pprint(config)
  
  fuente, entorno, estructuras = setup_experiment(config)
  if test:
    print("Modo test")
    print(fuente)
    print(entorno)
    for estructura in estructuras:
      print(estructura)
    print("\n")
  
  results_data = {"mean_data" : {"N fotones": [], "Time": [], "Fraccion fotones absorbidos": []}, "reps_data": {}}

  config_emision_fuente = config["emision_fuente"]
  config_emision_fuente["mean_angle"] = parse_param(config_emision_fuente["mean_angle"])
  config_emision_fuente["std_angle"] = parse_param(config_emision_fuente["std_angle"])
  
  # Se asume que config_fotones, estructuras, entorno, fuente y d_arbitraria_ampliacion
  # ya están definidos en el contexto.

  # Ejecutamos los experimentos en paralelo
  times = []
  abs_fractions = []
  nabs_fotons = []
  nfotons = []
  nfotones_int = []
  fotones_inactivos = None
  with ProcessPoolExecutor(max_workers=8) as executor:
    futures = [
        executor.submit(
            process_repetition, 
            config_emision_fuente, 
            estructuras, 
            entorno, 
            fuente, 
            config_emision_fuente["d_ampliacion"]
        )
        for _ in range(n_reps)
    ]
    for future in tqdm.tqdm(as_completed(futures), total=len(futures), desc=f"config {i+1}"):
      try:
        future_results = future.result()
      except Exception as e:
        print(f"Error en la ejecución: {e}")
        continue
      times.append(future_results["elapsed"])
      abs_fractions.append(future_results["abs_fraction"])
      nabs_fotons.append(future_results["nfotones_absorbidos"])
      nfotons.append(future_results["N_fotones"])
      nfotones_int.append(future_results["N_fotones_int"])
      fotones_inactivos = future_results["Fotones inactivos"]
  
  if graph:
    graph_path = graphPath + f"/experiment_{i+1}.png"
    # Reducimos el número de fotones a un 10% para visualizar mejor
    fotones_inactivos = fotones_inactivos[:int(len(fotones_inactivos) * 0.1)]
    draw_fotones_hist(fotones_inactivos, estructuras, save_path=graph_path)
    print(f"Gráfico guardado en {graph_path}")
  results_data["mean_data"]["N fotones"] = config_emision_fuente["N_fotones"]
  results_data["mean_data"]["Time"] = float(np.mean(times))
  results_data["mean_data"]["Fraccion fotones absorbidos"] = float(np.mean(abs_fractions))
  results_data["reps_data"]["times"] = times
  results_data["reps_data"]["abs_fractions"] = abs_fractions
  results_data["reps_data"]["nabs_fotons"] = nabs_fotons
  results_data["reps_data"]["nfotons"] = nfotons
  results_data["reps_data"]["nfotones_int"] = nfotones_int
  
  results[f"config_{i+1}"] = results_data
  print(results_data)
  print(f"Experimento {i+1} finalizado")

  
  with open(f'{configOutPath}/{files[i]}', 'w') as file:
    yaml.dump(config, file)
  with open(f'{outputPath}/results_{files[i]}', 'w') as file:
    yaml.dump(results[f"config_{i+1}"], file)
    
  print("Resultados guardados en el directorio de salida")
  print("========================================")
  if test:
    break
  
print("========================================")
print("Proceso finalizado")
print("========================================")
