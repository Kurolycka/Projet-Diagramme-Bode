import pyvisa
import time
from numpy import *
import matplotlib.pyplot as plt
import sys

# penser à dire que le séparateur décimal c'est le point unité de base c'est le volt Demander pour l'échelle
# logarithmique faire gaffe à Vsortie=Ventrée Incertitudes ? vérification des paramètres limitations GBF : 1 microHz
# à 30MHz Faire gaffe à mettre le trigger sur l'entrée autoset car scale : pleins de sleep partout donc au final plus
# long (un sleep au changement de freq, un sleep au changement de base (au moins 2s)) faire un help et prévenir qu'il
# faut 2s entre chaque mesure.


# Je lui demande tous mes paramètres + vérification des paramètres :

# ----------{Demande et Test de la fréquence de départ}---------- #
somme_dep = 0  # le nombre de chances
var_dep = False  # ne respecte pas mes conditions

while somme_dep < 3 and var_dep == False:
    freq_depart = float(input("Entrez votre fréquence de départ en Hz :"))
    # Pas besoin de tester le type vu qu'on force le type comme étant un float
    if 1E-6 < freq_depart < 3E7:
        var_dep = True
    else:
        print(f"Erreur. Votre fréquence de départ doit être un réel compris entre 6µHz et 30 MHz.\n"
              f"Vous avez entré {freq_depart}")

    somme_dep += 1

if somme_dep == 3 and var_dep == False:
    print("Erreur. Trop de mauvaises tentatives. Retournez voir l'help si besoin.")
    sys.exit()

# ----------{Test de la fréquence de fin}---------- #
somme_fin = 0  # le nombre de chances
var_fin = False  # ne respecte pas mes conditions

while somme_fin < 3 and var_fin == False:
    freq_fin = float(input("Entrez votre fréquence de fin en Hz :"))
    if freq_depart < freq_fin < 3E7:
        var_fin = True
    else:
        print(f"Erreur. Votre fréquence de fin doit être un réel compris entre freq_depart et 30 MHz.\n"
              f"Vous avez entré {freq_fin}")

    somme_fin += 1

if somme_fin == 3 and var_fin == False:
    print("Erreur. Trop de mauvaises tentatives. Retournez voir l'help si besoin.")
    sys.exit()

####Reste pas encore fait la vérification de paramètres.

nb_points = int(input("Entrez le nombre de points que vous souhaitez :"))

voie_entree = input("Entrez le channel de votre signal d'entrée (1 ou 2) :")
voie_sortie = input("Entrez le channel de votre signal de sortie (1 ou 2) :")

amplitude_tension = input("Entrez l'amplitude souhaitée pour votre signal d'entrée en V :")

# Je cherche sur quels ports sont l'oscillo et le GBF

gestionnaire = pyvisa.ResourceManager()

listePorts = gestionnaire.list_resources('?*')

for port in listePorts:
    try:
        instrument = gestionnaire.open_resource(port)
        if "Rigol Technologies,DG1032Z" in instrument.query("*IDN?"):
            GBF = gestionnaire.open_resource(port)
        elif "GW,GDS-1072B" in instrument.query("*IDN?"):
            oscillo = gestionnaire.open_resource(port)
    except:
        print(port + " pas connecté")
    instrument.close()

# On définit le signal d'entrée :

GBF.write(":Source" + voie_entree + ":APPLy:sin")
GBF.write(":Source" + voie_entree + ":VOLT " + amplitude_tension)

# Balayer les fréquences :

plage_freq = list(logspace(log10(freq_depart), log10(freq_fin), nb_points))
plage_freq = [round(i, 4) for i in plage_freq]
print(plage_freq)
tension_entree = []
tension_sortie = []
freq_entree_oscillo = []
phase = []

oscillo.read_termination = "\n"

# echelles_possibles=[1.e-08, 2.e-08, 5.e-08, 1.e-07, 2.e-07, 5.e-07, 1.e-06, 2.e-06, 5.e-06, 1.e-05,
# 2.e-05, 5.e-05, 1.e-04, 2.e-04, 5.e-04, 1.e-03, 2.e-03, 5.e-03, 1.e-02, 2.e-02,
# 5.e-02, 1.e-01, 2.e-01, 5.e-01, 1.e+00, 2.e+00, 5.e+00, 1.e+01, 2.e+01, 5.e+01,
# 1.e+02, 2.e+02, 5.e+02]


for freq in plage_freq:
    GBF.write(":Source" + voie_entree + ":FREQ " + str(freq))
    oscillo.write(":AUTOSet")
    time.sleep(2)

    oscillo.write(":MEASure:SOURce2 CH" + voie_entree)
    tension_entree.append(float(oscillo.query(":MEASure:PK2Pk?")))
    freq_entree_oscillo.append(float(oscillo.query(":MEASure:FREQuency?")))

    oscillo.write(":MEASure:SOURce1 CH" + voie_sortie)
    tension_sortie.append(float(oscillo.query(":MEASure:PK2Pk?")))

    phase.append(float(oscillo.query(":MEASure:PHAse?")))


print(freq_entree_oscillo)
print(tension_entree)
print(tension_sortie)
print(phase)

tension_entree = array(tension_entree)
tension_sortie = array(tension_sortie)

gain = 20 * log(abs(tension_sortie / tension_entree))
print(gain)

fig, ax = plt.subplots(2, 1)
fig.suptitle("Diagramme de Bode")

ax[0].plot(freq_entree_oscillo, gain, color="purple")
# ax[0].set_title("Gain en fonction de la fréquence")
ax[0].set_xlabel("Fréquence (Hz, échelle log)")
ax[0].set_xscale("log")
ax[0].set_ylabel("Gain (dB)")
ax[1].plot(freq_entree_oscillo, phase, color="orange")
# ax[1].set_title("Phase en fonction de la fréquence")
ax[1].set_xlabel("Fréquence (Hz, échelle log)")
ax[1].set_ylabel("Phase (°)")
ax[1].set_xscale("log")

plt.show()

gestionnaire.close()
