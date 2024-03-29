from numpy import *
import matplotlib.pyplot as plt

# On calcule le gain avec des array numpy
Tension_entree = linspace(5, 0.01, 100)
Tension_sortie = 1 / Tension_entree**2
Freq_entree_oscillo = linspace(0, 10E6, 100)
Phase = rad2deg(arctan(Freq_entree_oscillo/5E5))
Err_freq_entree_oscillo = 0.00001 * Freq_entree_oscillo
Err_tension_entree = 0.001 * Tension_entree
Err_tension_sortie = 0.001 * Tension_sortie
Err_phase = zeros(100) + 3

Gain = 20 * log(abs(Tension_sortie / Tension_entree))
Err_gain = (20 / log(10)) * ( (Err_tension_sortie / Tension_sortie) + (Err_tension_entree / Tension_entree))

print(Err_gain)

# On trace le gain et le déphasage avec les incertitudes
fig, ax = plt.subplots(2, 1, figsize=(13, 9))
fig.suptitle("Diagramme de Bode")

ax[0].plot(Freq_entree_oscillo, Gain, color="purple")
ax[0].fill_between(Freq_entree_oscillo, Gain - Err_gain, Gain + Err_gain, color="purple", alpha=0.2)
ax[0].grid(which="major", color="gainsboro")
ax[0].grid(which="minor", color="gainsboro", ls=":")
ax[0].minorticks_on()
ax[0].set_xlabel("Fréquence (Hz)")
ax[0].set_ylabel("Gain (dB)")

ax[1].plot(Freq_entree_oscillo, Phase, color="orange")
ax[1].fill_between(Freq_entree_oscillo, Phase - Err_phase, Phase + Err_phase, color="orange", alpha=0.2)
ax[1].grid(which="major", color="gainsboro")
ax[1].grid(which="minor", color="gainsboro", ls=":")
ax[1].minorticks_on()
ax[1].set_xlabel("Fréquence (Hz)")
ax[1].set_ylabel("Phase (°)")

ax[0].axhline(y=-3, ls="--", color="m")

plt.show()