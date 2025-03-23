import numpy as np
import yaml
import argparse
import os

def getxvalue(config, category, key):
    nested_config = config
    for cat in category[:-1]:
        nested_config = nested_config[cat]
    x_val = nested_config[category[-1]][key]
    return x_val


parser = argparse.ArgumentParser(description='Pintar resultados experimento')
parser.add_argument("-p", '--resultsPath', type=str, default='results/experiments_espesor', help='Directorio de los resultados de experimentos')
parser.add_argument("-c", '--category', nargs='+', type=str, help='Upper category of variables to change.')
parser.add_argument("-k", '--key', type =str, help='Key to override in the default configuration.')
parser.add_argument("-s", "--save", default = "False", type=str, help='Guardar la imagen')
args = parser.parse_args()

resultsPath = args.resultsPath
category = args.category
final_key = args.key
save = args.save
save = True if save == "True" else False

resultsConfig = resultsPath + "/configurations/"


config_files = {}
result_files = {}

# Listamos todos los archivos de configuración
for file in os.listdir(resultsConfig):
    if file.endswith(".yaml") or file.endswith(".yml"):
        with open(resultsConfig + file) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            config_files[file] = config

for key in config_files.keys():
    for file in os.listdir(resultsPath):
        if key in file:
          with open(resultsPath + "/"+file) as f:
            result = yaml.load(f, Loader=yaml.FullLoader)
          result_files[key]=result
        else:
            continue

print(f"Cargadas {len(config_files)} configuraciones y {len(result_files)} resultados")

# Guardamos dato medio de valor absorbido y su std
x_values = []
y_values = []
y_err = []
for config in config_files.keys():
    x_values.append(getxvalue(config_files[config], category, final_key))
    y_values.append(result_files[config]["mean_data"]["Fraccion fotones absorbidos"])
    y_err.append(np.std(result_files[config]["reps_data"]["abs_fractions"]))

# Pintamos
import matplotlib.pyplot as plt
x_sorted = np.argsort(x_values)
y_err_sorted = np.array(y_err)[x_sorted]
y_values_sorted = np.array(y_values)[x_sorted]
x_values_sorted = np.array(x_values)[x_sorted]

plt.plot(x_values_sorted, y_values_sorted, '-o')
plt.fill_between(x_values_sorted, np.array(y_values_sorted) - np.array(y_err_sorted), np.array(y_values_sorted) + np.array(y_err_sorted), alpha=0.5)
# plt.scatter(x_values, y_values, c='red')
# plt.errorbar(x_values, y_values, yerr=y_err, fmt='o')
# plt.xlabel(final_key.capitalize(), fontsize=14)
plt.xlabel(final_key.capitalize() + " (nm)", fontsize=14)
plt.ylabel("Fracción fotones absorbidos", fontsize=14)
plt.title(f"Fracción fotones absorbidos vs {final_key}", fontsize=16)
plt.grid()
plt.tight_layout()

if save:
    save_path = f"{resultsPath}/plots/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    plt.savefig(f"{resultsPath}/plots/{final_key}_absorbed_fraction.png")
else:
    plt.show()

  