import numpy as np
import matplotlib.pyplot as plt


# Cálculo del ángulo crítico
teta_critico = np.arcsin(ni/ nt)
print(np.degrees(teta_critico))
print(teta_critico)
# Definición de la función de Snell
def snell(ni, nt, teta_i):
    """Calcula el ángulo de refracción usando la ley de Snell."""
    try:
        teta_t = np.arcsin(ni * np.sin(teta_i) / nt)
        return teta_t
    except ValueError:
        # Si el seno es mayor a 1, hay reflexión interna total
        return None  # Indica que no hay transmisión

# Llamada a la función Snell
teta_t = snell(ni, nt, teta_i)

# Salida
if teta_t is None:
    print("Ocurre reflexión interna total")
else:
    print(f"El ángulo de transmisión es {teta_t:.2f} rad")

Rs=0
Rp=0
Ru=0
Tu=0
def fresnel(ni,nt,teta_t,teta_i):
     # Si hay reflexión interna total
    if teta_t is None:
        return 1
    Rs=((ni*np.cos(teta_i)-nt*np.cos(teta_t))/(ni*np.cos(teta_i)+nt*np.cos(teta_t)))**2
    Rp=((ni*np.cos(teta_t)-nt*np.cos(teta_i))/(ni*np.cos(teta_t)+nt*np.cos(teta_i)))**2
    Ru=(Rs+Rp)/2
    return (Ru)


x=fresnel(ni,nt,teta_t,teta_i)
print(x)

