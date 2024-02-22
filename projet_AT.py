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
"""
Pour la vérification des pramaètres on procède de la manière suivante : 
1. on pose le nombre d'essais à 0 et le paramètre demandé à None pour être sur et certain qu'il soit définit
2. on demande le paramètre à l'utilisateur en lui donnant les conditions sur celui ci
3. on essaie de convertir la valeur donné, si ça ne marche pas on prévient l'utilisateur que la variable qu'il a entré
n'est pas valide et on le laisse repartir de l'éape 2
4. si la valeur donné est valide mais ne respecte pas les conditions données on le prévient que les conditions n'ont
pas été respecté et on le laisse repartir de l'étape 2
5. si toutes les conditions sont réunie en 3 essais ou moins on poursuit le code
"""

# ----------{Demande et Test de la fréquence de départ}---------- #
freq_depart = None
essais = 0  # le nombre de chances
var_test = False

while essais < 3 and var_test == False:
    freq_depart = input("Entrez votre fréquence de départ en Hz : ")
    # Le float n'acceptant pas les "," on les remplace par des "."
    freq_depart = freq_depart.replace(",", ".")
    try:
        freq_depart = float(freq_depart)
        if 1E-6 < freq_depart < 3E7:
            var_test = True
        else:
            print(f"Erreur : Votre fréquence de départ doit être un réel compris strictement entre 1µHz et 30 MHz.\n"
                  f"Vous avez entré {freq_depart}")

    except:
        print(f"Erreur : Vous n'avez pas entré un nombre réel.\n"
              f"Vous avez entré {freq_depart}")
    essais += 1

if essais == 3 and var_test == False:
    print("Erreur : Trop de mauvaises tentatives. Retournez voir l'help si besoin.")
    sys.exit()

# ----------{Test de la fréquence de fin}---------- #
freq_fin = None
essais = 0  # le nombre de chances
var_test = False

while essais < 3 and var_test == False:
    freq_fin = input("Entrez votre fréquence de fin en Hz : ")
    # Le float n'acceptant pas les "," on les remplace par des "."
    freq_fin = freq_fin.replace(",", ".")
    try:
        freq_fin = float(freq_fin)
        if freq_depart < freq_fin < 3E7:
            var_test = True
        else:
            print(f"Erreur : Votre fréquence de fin doit être un réel compris entre freq_depart et 30 MHz.\n"
                  f"Vous avez entré {freq_fin}")

    except:
        print(f"Erreur : Vous n'avez pas entré un nombre réel.\n"
              f"Vous avez entré {freq_fin}")
    essais += 1

if essais == 3 and var_test == False:
    print("Erreur : Trop de mauvaises tentatives. Retournez voir l'help si besoin.")
    sys.exit()

# ----------{Test du nombre de points}---------- #
essais = 0  # le nombre de chances
var_test = False
nb_points = None

while essais < 3 and var_test == False:
    nb_points = input("Entrez le nombre de mesure à effectuer dans la plage de fréquence choisie ci-dessus : ")
    try:
        nb_points = int(nb_points)
        if nb_points >= 1:
            verif = input(f"Avertissement : Avec ce nombre de point, votre mesure va durer {nb_points * 2} secondes.\n"
                          f"Êtes vous sur de vouloir procéder? (o ou n) : ")
            if verif == "o":
                var_test = True

        else:
            print(f"Erreur : Le nombre de mesure à effectuer est inférieur à 1.\n"
                  f"Vous avez entré {nb_points}")

    except:
        print(f"Erreur : Vous n'avez pas entré un nombre entier.\n"
              f"Vous avez entré {nb_points}")
    essais += 1

if essais == 3 and var_test == False:
    print("Erreur : Trop de mauvaises tentatives. Retournez voir l'help si besoin.")
    sys.exit()

# ----------{Test du nombre de la voie d'entrée}---------- #
essais = 0  # le nombre de chances
var_test = False
voie_entree = None
voie_sortie = None
Voies = [1, 2]

while essais < 3 and var_test == False:
    voie_entree = input("Entrez le numéro de voie de votre signal d'entrée (1 ou 2) : ")
    try:
        voie_entree = int(voie_entree)
        if voie_entree in Voies:
            Voies.remove(voie_entree)
            voie_sortie = Voies[0]
            print(f"Avertissement : La voie de votre signal d'entrée étant la voie N°{voie_entree} "
                  f"la voie de sortie est la voie N°{voie_sortie}.")
        else:
            print(f"Erreur : La voie que vous avez entré n'est ni la 1 ni la 2.\n"
                  f"Vous avez entré{voie_entree}")
    except:
        print(f"Erreur : Vous n'avez pas entré un nombre entier entre 1 et 2.\n"
              f"Vous avez entré {voie_entree}")
    essais += 1

if essais == 3 and var_test == False:
    print("Erreur : Trop de mauvaises tentatives. Retournez voir l'help si besoin.")
    sys.exit()

# ----------{Test de l'amplitude du signal d'entrée}---------- #

# Regarder l'amplitude max ? Ai du mal à trouver l'info sur le manuel. Et elle est obligée d'être positive ?
var_test = False
essais = 0  # le nombre de chances
amplitude = None

while essais < 3 and var_test == False:
    amplitude = input("Entrez l'amplitude du signal d'entrée en volt : ")
    # Le float n'acceptant pas les "," on les remplace par des "."
    amplitude = amplitude.replace(",", ".")
    try:
        amplitude = float(amplitude)
        if 0 < amplitude:
            var_test = True
        else:
            print(f"Erreur : Votre amplitude de signal d'entrée doit être strictement positive.\n"
                  f"Vous avez entré {amplitude}")
    except:
        print(f"Erreur : Vous n'avez pas entré un nombre réel.\n"
              f"Vous avez entré {amplitude}")
    essais += 1

if essais == 3 and var_test == False:
    print("Erreur : Trop de mauvaises tentatives. Retournez voir l'help si besoin.")
    sys.exit()

# ----------{Test de l'échelle}---------- #
essais = 0
var_test = False
echelleLog = None

while essais < 3 and var_test == False:
    echelleLog = input("Entrez le type d'echelle souhaitée (lin/log) : ")
    echelleLog.lower()
    if echelleLog == "log":
        echelleLog = True
    elif echelleLog == "lin":
        echelleLog = False
    else:
        print(f"Erreur : vous n'avez pas entré lin ou log."
              f"Vous avez entré {echelleLog}")
    essais += 1

if essais == 3 and var_test == False:
    print("Erreur. Trop de mauvaises tentatives. Retournez voir l'help si besoin.")
    sys.exit()

# ----------{Ouverture de l'oscillo et du GBF}---------- #

"""
Pour ouvrir le GBF et l'oscillo on utilise la commande "list_resources" du ressource manager de pyvisa. Elle renvoie 
la liste de tout les périphériques qui sont connecté à un appareil. On identifie chaque périphériques en leurs 
demandant de s'identifier avec "*IDN?". 
Si le périphérique est allumé il renvoie son identification. Si l'identification contient : 
- "Rigol Technologies,DG1032Z" : alors on a le GBF, on l'ouvre
- "GW,GDS-1072B" : alors on a l'oscillo, on l'ouvre
"""

gestionnaire = pyvisa.ResourceManager()

listePorts = gestionnaire.list_resources('?*')

GBF = None
oscillo = None

for port in listePorts:
    try:
        instrument = gestionnaire.open_resource(port)
        if "Rigol Technologies,DG1032Z" in instrument.query("*IDN?"):
            GBF = gestionnaire.open_resource(port)
        elif "GW,GDS-1072B" in instrument.query("*IDN?"):
            oscillo = gestionnaire.open_resource(port)
        instrument.close()
    except:
        print(port + " pas connecté")

oscillo.read_termination = "\n"

# ----------{Définition du signal d'entrée}---------- #

"""
On définit le signal avec les paramètres fournit par l'utilisateur
"""

GBF.write(":Source" + voie_entree + ":APPLy:sin")
GBF.write(":Source" + voie_entree + ":VOLT " + amplitude)

# ----------{Définition de la plage de fréquence}---------- #

"""
Pour définir la fréquence il y a deux situations, soit l'utilisateur veut une échelle logarithmique soit il veut
une échelle linéaire : 
- pour l'écgelle log : on utilise le logspace de numpy. mais il faut penser à convertir les limites de la plage
de fréquence en leurs équivalent en puissance de 10.
- pour l'échelle lin : on utilise le linspace de numpy sans conversions cette fois-ci.
"""

if echelleLog:
    plage_freq = list(logspace(log10(freq_depart), log10(freq_fin), nb_points))
    plage_freq = [round(i, 4) for i in plage_freq]
    print(plage_freq)
else:
    plage_freq = list(linspace(freq_depart, freq_fin, nb_points))
    plage_freq = [round(i, 4) for i in plage_freq]
    print(plage_freq)

# ----------{Définition des listes de stockage et constantes}---------- #
tension_entree = []
tension_sortie = []
freq_entree_oscillo = []
phase = []

# echelles_possibles=[1.e-08, 2.e-08, 5.e-08, 1.e-07, 2.e-07, 5.e-07, 1.e-06, 2.e-06, 5.e-06, 1.e-05,
# 2.e-05, 5.e-05, 1.e-04, 2.e-04, 5.e-04, 1.e-03, 2.e-03, 5.e-03, 1.e-02, 2.e-02,
# 5.e-02, 1.e-01, 2.e-01, 5.e-01, 1.e+00, 2.e+00, 5.e+00, 1.e+01, 2.e+01, 5.e+01,
# 1.e+02, 2.e+02, 5.e+02]

# ----------{Balayage de la plage de fréquences et mesures}---------- #
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

# ----------{calcul du gain}---------- #
tension_entree = array(tension_entree)
tension_sortie = array(tension_sortie)

gain = 20 * log(abs(tension_sortie / tension_entree))
print(gain)

# ----------{Tracé du diagramme de bode}---------- #
fig, ax = plt.subplots(2, 1)
fig.suptitle("Diagramme de Bode")

ax[0].plot(freq_entree_oscillo, gain, color="purple")
# ax[0].set_title("Gain en fonction de la fréquence")
ax[0].set_xlabel("Fréquence (Hz)")
ax[0].set_ylabel("Gain (dB)")
if echelleLog:
    ax[0].set_xscale("log")
ax[1].plot(freq_entree_oscillo, phase, color="orange")
# ax[1].set_title("Phase en fonction de la fréquence")
ax[1].set_xlabel("Fréquence (Hz)")
ax[1].set_ylabel("Phase (°)")
if echelleLog:
    ax[1].set_xscale("log")

plt.show()

gestionnaire.close()