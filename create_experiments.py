import yaml
import argparse
import os
from copy import deepcopy
import numpy as np

def create_experiments(default_config, category, dict_of_values):
  """
  Create a list of experiments from a default configuration and a dictionary of values to override in the default configuration.

  Args:
    default_config (str): Path to the default configuration file.
    category (list): List of keys leading to the nested structure to change.
    dict_of_values (dict): Dictionary of values to override in the default configuration.

  Returns:
    list: List of experiments.
  """
  with open(default_config, 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

  experiments = []
  key = list(dict_of_values.keys())[0]
  for value in dict_of_values[key]:
    # Navigate to the nested structure using the category list
    nested_config = config
    for cat in category[:-1]:
      nested_config = nested_config[cat]
    
    # Access the final nested structure
    final_key = category[-1]
    type_value = type(nested_config[final_key][key])
    if type_value == list:
      nested_config[final_key][key] = value
    elif type_value == dict:
      nested_config[final_key][key] = {key: value}
    elif type_value == str:
      nested_config[final_key][key] = value
    elif type_value == int:
      nested_config[final_key][key] = int(value)
    elif type_value == float:
      nested_config[final_key][key] = float(value)
    else:
      raise Exception("Invalid type")
    experiments.append(deepcopy(config))
  return experiments
        

parser = argparse.ArgumentParser(description='Generador de archivos de experimentos')
parser.add_argument("-d", '--default_config', default ="configs/default_configs", type=str, help='Path to the default configuration file.')
parser.add_argument("-c", '--category', nargs='+', type=str, help='Upper category of variables to change.')
parser.add_argument("-k", '--key', type =str, help='Key to override in the default configuration.')
parser.add_argument("-v", '--value', nargs='+', help='Values to override in the default configuration.')
parser.add_argument("-s", "--structures", default = "single", type=str, help='Type of structures to use in the simulation.')
parser.add_argument("-r", "--range", nargs='+', type=float, help='Range of values to override in the default configuration. Initial value, final value and step.')
args = parser.parse_args()


output_path = "configs/experiments_"+args.structures+"_"+args.key

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
    raise Exception("Invalid structure type")
  
if args.range:
  dict_of_values = {args.key: list(np.arange(args.range[0], args.range[1], args.range[2]))}
elif args.value:  
  dict_of_values = {args.key: args.value}
else:
  raise Exception("No values provided")
experiments = create_experiments(default_config_path, args.category, dict_of_values)
for i, experiment in enumerate(experiments):
    with open(output_path +f"/config_{args.key}{str(i)}"+".yaml", 'w') as file:
        yaml.dump(experiment, file)
        print("Experimento", i, "creado con éxito")