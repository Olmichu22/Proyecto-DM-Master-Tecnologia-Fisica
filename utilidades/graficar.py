import matplotlib.pyplot as plt

def draw_fotones_hist(fotones, estructuras, expand=True, save_path=None):
  plt.figure(figsize=(50, 50))

  for estructura in estructuras:
    x, y = estructura.getPlotCoords()
    plt.plot(x, y)
  plt.gca().set_aspect('equal', adjustable='box')

  for foton in fotones:
    # Dibuujando camino de los fotones
    pos_hist = [p[0] for p in foton.poshist]
    x = [p[0] for p in pos_hist]
    y = [p[1] for p in pos_hist]
    plt.plot(x, y, c='b', alpha=0.05)

    # Dibujamos el vector de salida en la última posición
    if expand:
      plt.quiver(x[-1], y[-1], foton.dire[0], foton.dire[1], color='r', scale=100)  # Reduce el tamaño de las flechas
      plt.text(x[-1], y[-1], foton.n, fontsize=12, color='black')
  plt.plot()
  if save_path:
    plt.savefig(save_path)
  else:
    plt.show() 
  return 
