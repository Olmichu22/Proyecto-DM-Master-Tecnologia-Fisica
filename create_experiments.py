import yaml
import argparse
import os
from copy import deepcopy
import numpy as np
import re

def create_experiments(default_config, category, dict_of_values):
    """
    Crea una lista de experimentos a partir de una configuración por defecto y un diccionario
    de valores a sobrescribir en la configuración.
    
    Permite especificar claves con notación de índice para modificar un solo elemento de una lista.
    Por ejemplo, si la clave es "nr_list[0]", se modificará solo el primer elemento de la lista.
    
    Args:
      default_config (str): Ruta al archivo de configuración por defecto.
      category (list): Lista de claves que indican la ruta en la estructura anidada donde cambiar.
      dict_of_values (dict): Diccionario de valores a sobrescribir.
    
    Returns:
      list: Lista de configuraciones (dictionaries) para cada experimento.
    """
    with open(default_config, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    experiments = []
    
    # Suponemos que se va a modificar una única clave (pero con múltiples valores)
    key_with_index = list(dict_of_values.keys())[0]
    # Detectar si la clave tiene notación de índice, por ejemplo "nr_list[0]"
    m = re.match(r"(.+)\[(\d+)\]$", key_with_index)
    if m:
        base_key = m.group(1)
        idx = int(m.group(2))
    else:
        base_key = key_with_index
        idx = None

    for value in dict_of_values[key_with_index]:
        # Navegar en la configuración usando la lista 'category'
        nested_config = config
        for cat in category[:-1]:
            nested_config = nested_config[cat]
        
        final_key = category[-1]
        
        # Obtenemos el valor actual en la configuración para esa clave
        current_val = nested_config[final_key][base_key]
        type_value = type(current_val)
        
        if idx is not None:
            # Se espera que current_val sea una lista
            if not isinstance(current_val, list):
                raise Exception(f"La clave {base_key} no es una lista, pero se intentó acceder con un índice.")
            # Convertir el valor según el tipo del elemento actual
            if isinstance(current_val[idx], int):
                new_value = int(value)
            elif isinstance(current_val[idx], float):
                new_value = float(value)
            elif isinstance(current_val[idx], str):
                new_value = str(value)
            else:
                new_value = value
            # Modificar solo el elemento en la posición idx
            nested_config[final_key][base_key][idx] = new_value
        else:
            # Si el valor actual es una lista, se reemplaza toda la lista
            if isinstance(current_val, list):
                nested_config[final_key][base_key] = value
            elif isinstance(current_val, dict):
                nested_config[final_key][base_key] = {base_key: value}
            elif isinstance(current_val, str):
                nested_config[final_key][base_key] = value
            elif isinstance(current_val, int):
                nested_config[final_key][base_key] = int(value)
            elif isinstance(current_val, float):
                nested_config[final_key][base_key] = float(value)
            else:
                raise Exception("Tipo no válido para la clave")
        
        experiments.append(deepcopy(config))
    return experiments

# Ejemplo de uso con argumentos de línea de comandos:

parser = argparse.ArgumentParser(description='Generador de archivos de experimentos')
parser.add_argument("-d", '--default_config', default="configs/default_configs", type=str, help='Ruta al archivo de configuración por defecto.')
parser.add_argument("-c", '--category', nargs='+', type=str, help='Categoría superior de variables a cambiar (ruta en la configuración).')
parser.add_argument("-k", '--key', type=str, help='Clave a sobrescribir en la configuración. Se puede usar notación "clave[index]".')
parser.add_argument("-v", '--value', nargs='+', help='Valores a sobrescribir en la configuración.')
parser.add_argument("-s", "--structures", default="single", type=str, help='Tipo de estructuras a usar en la simulación.')
parser.add_argument("-r", "--range", nargs='+', type=float, help='Rango de valores: valor inicial, final y paso.')
args = parser.parse_args()

output_path = "configs/experiments_" + args.key
if not os.path.exists(output_path):
    os.makedirs(output_path)

default_config_path = args.default_config
if args.structures == "nested":
    default_config_path += "/experiment_config_nested.yml"
elif args.structures == "single":
    default_config_path += "/experiment_config_single.yml"
elif args.structures == "inverse_nested":
    default_config_path += "/experiment_config_inverse_nested.yml"
else:
    raise Exception("Tipo de estructura inválido")
  
if args.range:
    dict_of_values = {args.key: list(np.arange(args.range[0], args.range[1], args.range[2]))}
elif args.value:  
    dict_of_values = {args.key: args.value}
else:
    raise Exception("No se proporcionaron valores")

experiments = create_experiments(default_config_path, args.category, dict_of_values)
for i, experiment in enumerate(experiments):
    with open(os.path.join(output_path, f"config_{args.key}{str(i)}.yaml"), 'w') as file:
        yaml.dump(experiment, file)
        print("Experimento", i, "creado con éxito")
