# %matplotlib qt
import pyvisa
import time
from numpy import *
import matplotlib.pyplot as plt
import sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# --------------------{Objectifs}---------------------

# Mettre dans le readme quelles références de machines utiliser.
# Afficher les incertitudes 
# comparer avec la valeur théorique de la fréquence de coupure 
# sert à rien qu'on règle le trigger car l'autoset le fait
# essais marque le nombre d'essais pour un point, si il échoue 3 fois sur le même point il passe au point suivant
# cela permet sur des mesures de point à problème de lui laisser l'occasion de réessayer pour si possible être plus
# précis sur la courbe

# Précision 3% en vertical
# problème car à certains moments il arrivait pas à mesurer l'amplitude mettre dans cr


# --------------------{Préparation des variables globales}---------------------
"""
On commence par déclarer les variables globales sous forme de string vide car le input va nous donner des strings
"""
# La fréquence de départ
freq_dep = ""
# La fréquence de fin
freq_fin = ""
# Le nombre de points voulu
nb_points = ""
# La voie de l'oscilloscope qui va mesurer la tension d'entrée
voie_entree = ""
# L'amplitude désirée
amplitude_entree = ""
# La voie de l'oscilloscope qui va mesurer la tension de sortie
voie_sortie = ""
# La voie du GBF qui fournit le signal
voie_GBF = ""
# Le nombre d'échantillons voulu pour mesurer le signal
moyenne_echantillon = ""
# Amplitude maximale que le GBF peut produire (imposé)
amplitude_max = ""
# type d'échelle des fréquences pour le tracé
echelle = ""
# fréquence de coupure approximative ou non 
frequence_coupure_case = ""

# --------------------{Fonctions pour les widgets}---------------------

"""
Les fonctions ci-dessous sont les fonctions appellée par les boutons de l'interface graphique; les fonctions validate
fonctionne d'une manière similaire: 
1. La valeur entrée dans l'interface graphique est récupérée en tant que paramètre et passe par leur fonction 
de validation respective.
2. La valeur passe par plusieurs test et soit : 
    a. Il y a une erreur, auquel cas un message est affiché dans une nouvelle fenêtre
    b. Il n'y a pas d'erreur, auquel cas la fonction renvoie vrai pour signaler à validate_all que cette variable est ok

Pour les fonctions
"""


def validate_freq_dep():
    """
    Critères de validité :
    1. La valeur freq_dep doit être un réel à virgule ou à point. Dans le cas contraire la fonction float échoue
    2. La valeur freq_dep doit être compris dans l'intervale [1E-6; 3E7] en accord avec les limitations du GBF
    """
    global freq_dep  # On modifie la variable globale
    freq_dep = entry1.get()  # On récupère la variable
    freq_dep = freq_dep.replace(",", ".")
    try:  # on essaie de la transformer en float
        freq_dep = float(freq_dep)
        if 1E-6 < freq_dep < 3E7:  # On regarde si la valeur respecte l'intervalle
            return True
        else:  # Si la valeur n'est pas dans l'intervalle, on affiche un message d'erreur
            messagebox.showerror("Erreur",
                                 f"Votre fréquence de départ doit être un réel compris entre 1µHz et 30 MHz.\n"
                                 f"Vous avez entré {freq_dep} Hz.")
            return False
    except:  # Si la transformation en float à échouer on affiche ce message
        messagebox.showerror("Erreur", f"Votre fréquence de départ doit être un réel compris entre 1µHz et 30 MHz.\n"
                                       f"Vous avez entré {freq_dep} Hz.")
        return False


def validate_freq_fin():
    """
    Critères de validité :
    1. La valeur freq_fin doit être un réel à virgule ou à point. Dans le cas contraire la fonction float échoue
    2. La valeur freq_fin doit être compris dans l'intervale [freq_dep; 3E7] en accord avec les limitations du GBF
    """
    global freq_fin
    freq_fin = entry2.get()
    freq_fin = freq_fin.replace(",", ".")
    try:
        freq_fin = float(freq_fin)
        if freq_dep < freq_fin < 3E7:
            return True
        else:
            messagebox.showerror("Erreur",
                                 f"Votre fréquence de fin doit être un réel compris entre {freq_dep} Hz et 30 MHz.\n"
                                 f"Vous avez entré {freq_fin} Hz.")
            return False
    except:
        messagebox.showerror("Erreur", f"Vous n'avez pas entré un nombre réel pour la fréquence de fin.\n"
                                       f"Vous avez entré {freq_fin} Hz.")
        return False


def validate_amplitude_entree():
    """
    Critères de validité :
    1. La valeur amplitude_entree doit être un réel à virgule ou à point. Dans le cas contraire la fonction float échoue
    2. La valeur amplitude_entree doit être compris dans l'intervale [2.5E-3; amplitude_max]
    amplitude max étant imposé juste avant l'appel de cette fonction et en accord avec les limitations du GBF
    """
    global amplitude_entree
    global amplitude_max
    amplitude_entree = entry5.get()
    amplitude_entree = amplitude_entree.replace(",", ".")
    try:
        amplitude_entree = float(amplitude_entree)
        if 2.5E-3 <= amplitude_entree <= amplitude_max:
            return True
        else:
            messagebox.showerror("Erreur", f"Votre amplitude de signal d'entrée doit être positive.\n"
                                           f"Vous avez entré {amplitude_entree} V.")
            return False
    except:
        messagebox.showerror("Erreur", f"Vous n'avez pas entré un nombre réel.\n"
                                       f"Vous avez entré {amplitude_entree}.")
        return False


def validate_nb_points():
    """
    Critères de validité :
    1. La valeur nb_points doit être un entier. Dans le cas contraire la fonction int échoue
    2. La valeur nb_points doit être positive
    3. L'utilisateur sera informé de la durée de l'acquisition, s'il souhaite poursuivre il doit valider.
    """
    global nb_points
    nb_points = entry3.get()
    nb_points = nb_points.replace(",", ".")
    try:
        nb_points = int(nb_points)
        if nb_points >= 1:
            response = messagebox.askquestion("Confirmation",
                                              f"Avec ce nombre de points, votre mesure va durer entre {2 + nb_points * 1} et {2 + nb_points * 3} secondes.\n"
                                              "Êtes-vous sûr de vouloir procéder ?")
            if response == 'yes':
                return True
            else:
                return False
        else:
            return False
    except:
        messagebox.showerror("Erreur", f"Vous n'avez pas entré un nombre entier.\n Vous avez entré {nb_points}.")
        return False


def validate_all():
    """
    Cette fonction permet d'apeller toutes les fonctions de validation précédentes. Si l'une d'entre elle renvoie un
    False, l'éxécution du programme ne se produira pas.
    """
    global freq_dep
    global freq_fin
    global nb_points
    global amplitude_entree
    global amplitude_max
    if not validate_freq_dep():
        return False
    if not validate_freq_fin():
        return False
    else:
        amplitude_max = None
        if freq_fin < 1E+7:
            amplitude_max = 10
        elif 1E+7 <= freq_fin < 3E+7:
            amplitude_max = 5
        elif 3E+7 <= freq_fin < 6E+7:
            amplitude_max = 2.5

    if not validate_amplitude_entree():
        return False
    if not validate_nb_points():
        return False
    return True


def help_window():
    """
    Cette fonction permet d'afficher la fenêtre d'aide.
    """
    # Créer une nouvelle fenêtre
    new_window = Toplevel(root)
    new_window.title("Aide")

    # Ajouter du texte à la nouvelle fenêtre
    label = ttk.Label(new_window, text="Gros texte d'aide à insérer plus tard.")
    label.pack(padx=20, pady=20)


# --------------------{Définition de la fenêtre principale}---------------------

root = Tk()  # Base de l'interface
root.title("Diagramme de Bode")  # Titre de la fenêtre

# On choisit ensuite le style, les couleurs et les espacement
style = ttk.Style()
style.theme_use('alt')

color_rgb_darkp = (25, 12, 24)
color_html_darkp = "#%02x%02x%02x" % color_rgb_darkp

color_rgb_purple = (247, 65, 143)
color_html_purple = "#%02x%02x%02x" % color_rgb_purple

# style.configure('TButton', background=color_html_purple, foreground='black')

style.configure('Titi.TButton', background=color_html_purple, foreground='black', relief='raised', borderwidth=4)

ttk.Style().configure('Custom.TLabel', foreground=color_html_darkp, font=("Times New Roman", 12))

# On créer un cadre dans la fenêtre
frm = ttk.Frame(root, padding=10)

# On crée une grille dans le cadre pour placer les éléments correctement
frm.grid()

# --------------------{Les widgets}---------------------


# Pour ajouter un espace avant les boutons :
ttk.Label(frm, text="", style='Custom.TLabel').grid(column=0, row=1)

"""
La structure des widget est très similaire les unes des autres :
1. On met un label pour savoir ce que ce widget va définir
2. on place les widgets
3. on crée une variable spéciale de tkinter qui permet de récupérer les valeurs entrée dans les saisie de texte/listes
(pour les boutons radio on fait cette valeur directement dans le bouton)
"""
# -----{Choix de voie pour la mesure de Ve
ttk.Label(frm, text="Numéro de voie du signal d'entrée (Oscilloscope): ", style='Custom.TLabel').grid(column=0, row=2)
voie_entree = IntVar()  # Variable pour stocker la valeur sélectionnée
rdio1 = ttk.Radiobutton(frm, text="1", variable=voie_entree, value=1)
rdio2 = ttk.Radiobutton(frm, text="2", variable=voie_entree, value=2)
rdio1.grid(column=1, row=2)
rdio2.grid(column=2, row=2)

# -----{Choix de voie pour la production de Ve
ttk.Label(frm, text="Numéro de voie du générateur : ", style='Custom.TLabel').grid(column=0, row=3)
voie_GBF = IntVar()  # Variable pour stocker la valeur sélectionnée
rdio3 = ttk.Radiobutton(frm, text="1", variable=voie_GBF, value=1)
rdio4 = ttk.Radiobutton(frm, text="2", variable=voie_GBF, value=2)
rdio3.grid(column=1, row=3)
rdio4.grid(column=2, row=3)

# -----{Choix entre log et lin
ttk.Label(frm, text="Type d'échelle pour le balayage en fréquence: ", style='Custom.TLabel').grid(column=0, row=4)
echelle = IntVar()  # Variable pour stocker la valeur sélectionnée
rdio5 = ttk.Radiobutton(frm, text="lin", variable=echelle, value=1)
rdio6 = ttk.Radiobutton(frm, text="log", variable=echelle, value=2)
rdio5.grid(column=1, row=4)
rdio6.grid(column=2, row=4)

# -----{Saisie de la fréquence initiale
ttk.Label(frm, text="Fréquence de départ (Hz) : ", style='Custom.TLabel').grid(column=0, row=5)
entry1 = ttk.Entry(frm)
entry1.grid(column=1, row=5, columnspan=2)

# -----{Saisie de la fréquence finale
ttk.Label(frm, text="Fréquence de fin (Hz) : ", style='Custom.TLabel').grid(column=0, row=6)
entry2 = ttk.Entry(frm)
entry2.grid(column=1, row=6, columnspan=3)

# -----{Saisie du nombre de points
ttk.Label(frm, text="Nombre de points : ", style='Custom.TLabel').grid(column=0, row=7)
entry3 = ttk.Entry(frm)
entry3.grid(column=1, row=7, columnspan=2)

# -----{Saisie de l'amplitude souhaitée
ttk.Label(frm, text="Amplitude du signal d'entrée (V) : ", style='Custom.TLabel').grid(column=0, row=8)
entry5 = ttk.Entry(frm)
entry5.grid(column=1, row=8, columnspan=2)

# -----{Saisie du nombre d'échantillons de mesure
ttk.Label(frm, text="Nombre d'échantillons utilisés pour le tracé : ", style='Custom.TLabel').grid(column=0, row=9)
options_moyenne = ["2", "4", "8", "16", "32", "64", "128", "256"]
moyenne_echantillon = StringVar()
moyenne_echantillon_combobox = ttk.Combobox(frm, values=options_moyenne, textvariable=moyenne_echantillon)
moyenne_echantillon_combobox.grid(column=1, row=9, columnspan=2)
moyenne_echantillon_combobox.current(0)

# Pour ajouter un espace avant les boutons :
ttk.Label(frm, text="", style='Custom.TLabel').grid(column=0, row=10)

# La case à cocher pour l'approximation de la fréquence de coupure :
frequence_coupure_case = IntVar()
checkbox = Checkbutton(frm, text="Affichage de l'approximation de la fréquence de coupure",
                       variable=frequence_coupure_case, onvalue=True, offvalue=False, font=("Times New Roman", 12))
checkbox.grid(column=0, row=11, columnspan=3)

# Pour ajouter un espace avant les boutons :
ttk.Label(frm, text="", style='Custom.TLabel').grid(column=0, row=12)


# --------------------{fonctions pour les boutons}---------------------

def get_text_and_destroy():
    """
    Cette fonction sera apellée une fois que l'utilisateur aura cliqué sur le bouton "Valider". La fenêtre se fermera
    et le programme se poursuit.
    """
    if validate_all():
        root.destroy()  # si get_text() on continue en tuant la fenêtre


def quit_program():
    """
    Cette fonction sera apellée une fois que l'utilisateur aura cliqué sur le bouton "Quitter". La fenêtre se fermera
    et le programme s'arrête.
    """
    root.destroy()
    sys.exit()


# --------------------{Les boutons au bottom}---------------------

# -----{Bouton valider
ttk.Button(frm, text="Valider", command=get_text_and_destroy, style='Titi.TButton').grid(column=1, row=13)
# -----{Bouton aide
ttk.Button(frm, text="Aide", command=help_window, style='Titi.TButton').grid(column=0, row=13)
# -----{Bouton quitter
ttk.Button(frm, text="Quitter", command=quit_program, style='Titi.TButton').grid(column=2, row=13)

root.mainloop()

# --------------------{Vérification des variables globales}---------------------

print("Voici les paramètres sélectionné :")
print(" - Valeur de freq_dep :", freq_dep)
print(" - Valeur de freq_fin :", freq_fin)
print(" - Valeur de nb_points :", nb_points)

voie_entree = voie_entree.get()  # Je récupère la valeur de voie_entree

# Pour avoir voie_sortie :
if voie_entree == 1:
    voie_sortie = 2
else:
    voie_sortie = 1
print(" - Valeur de voie_entree :", voie_entree)
print(" - Valeur de voie_sortie :", voie_sortie)

print(" - Valeur de amplitude_entree  :", amplitude_entree)

voie_GBF = voie_GBF.get()
print(" - Valeur de voie_GBF :", voie_GBF)

moyenne_echantillon = moyenne_echantillon.get()
print(" - Valeur de moyenne_echantillon :", voie_GBF)

echelle = echelle.get()
if echelle == 1:
    echelle = "lin"
else:
    echelle = "log"
print(" - Valeur de echelle :", echelle)

frequence_coupure_case = frequence_coupure_case.get()
print(" - Affichage de la fréquence de coupure ? :", frequence_coupure_case)

# --------------------{Récupération des ports}---------------------

# On ouvre le ressource manage de pyvisa
gestionnaire = pyvisa.ResourceManager()

# on ouvre la liste des ports connectée à l'ordinateur avec le ressource manager
listePorts = gestionnaire.list_resources('?*')

# pour chaque élément de cette liste
for port in listePorts:
    try:  # on essaie d'ouvrir le port
        instrument = gestionnaire.open_resource(port)
        if "Rigol Technologies,DG1032Z" in instrument.query("*IDN?"):
            GBF = gestionnaire.open_resource(port)
        elif "GW,GDS-1072B" in instrument.query("*IDN?"):
            oscillo = gestionnaire.open_resource(port)
        instrument.close()
    except:  # Si le port n'est pas ouvert, c'est qu'il n'est pas allumé
        print(port + " pas allumé")

# --------------------{Définition du signal d'entrée}---------------------

# On définit le premier signal et on allume la sortie du GBF
GBF.write(f":Source{voie_entree}:APPLy:sin")
GBF.write(f":Source{voie_entree}:VOLT {amplitude_entree}")
GBF.write(f":Source{voie_entree}:frequence {freq_dep}")
GBF.write(f":output{voie_GBF} ON")

# --------------------{Réglages oscilloscope}---------------------

# Permet de faire une moyenne de plusieurs mesures
oscillo.write(f":ACQuire:MODe AVERage")
oscillo.write(f":ACQuire:AVERage {moyenne_echantillon}")

# On met le couplage des chaîne en AC, ce qui permet à l'utilisateur de mettre un offset sans conséquence sur les calculs
oscillo.write(f":CHANnel1:COUPling AC")
oscillo.write(f":CHANnel2:COUPling AC")

# pour le coupling AC voir page 44


# --------------------{Balayage des fréquences}---------------------

# On crée la plage de fréquence à balayer en fonction de l'échelle voulue
if echelle == "log":
    # logspace fait une echelle linéaire des puissances, il faut donc récupérer la puissance de 10 correspondante à la
    # freq de départ et de fin
    plage_freq = list(logspace(log10(freq_dep), log10(freq_fin), nb_points))
elif echelle == "lin":
    plage_freq = list(linspace(freq_dep, freq_fin, nb_points))

# on arrondit pour que les valeurs soient acceptées par le GBF
plage_freq = [round(i, 4) for i in plage_freq]

# on crée les listes qui vont stocker nos mesures
Freq_entree_oscillo = []
Err_freq_entree_oscillo = []
Tension_entree = []
Err_tension_entree = []
Tension_sortie = []
Err_tension_sortie = []
Phase = []
Err_phase = []

oscillo.read_termination = "\n"

# On fait un premier autoset
oscillo.write(":AUTOSet")
time.sleep(2)

for freq in plage_freq:
    essais = 0
    # on modifie la frequence produite par le GBF en partant de freq_dep
    GBF.write(f":Source{voie_entree}:FREQ {freq}")
    # on attend un peu avant de faire les mesures
    time.sleep(1)
    while essais < 3:
        try:
            # on récupère l'échelle horizontale de l'oscillo (commune aux deux channels)
            echelle_hori = float(oscillo.query(":timebase:scale?"))

            # on met la source de mesure sur le channel qui mesure la tension d'entrée et on récupère
            # nos mesures et les échelles
            oscillo.write(f":MEASure:SOURce1 CH{voie_entree}")
            freq_entree_oscillo = oscillo.query(":MEASure:FREQuency?")
            ampli_entree = oscillo.query(":MEASure:AMPlitude?")
            echelle_vert_entree = float(oscillo.query(f":channel{voie_entree}:scale?"))

            # on met la source de mesure sur le channel qui mesure la tension de sortie et on récupère
            # nos mesures et les échelles
            oscillo.write(f":MEASure:SOURce1 CH{voie_sortie}")
            ampli_sortie = oscillo.query(":MEASure:AMPlitude?")
            echelle_vert_sortie = float(oscillo.query(f":channel{voie_sortie}:scale?"))

            # on met la source de mesure 1 sur le channel qui mesure la tension d'entrée et la deuxième sur le
            # channel qui mesure la tension de sortie et on mesure le déphasage de la source 2 par rapport à la 1
            oscillo.write(f":MEASure:SOURce1 CH{voie_entree}")
            oscillo.write(f":MEASure:SOURce2 CH{voie_sortie}")
            phase = oscillo.query(":MEASure:PHAse?")

            freq_entree_oscillo = float(freq_entree_oscillo)
            ampli_entree = float(ampli_entree)
            ampli_sortie = float(ampli_sortie)
            phase = float(phase)
        except:
            oscillo.write(":AUTOSet")
            time.sleep(2)
            essais = essais + 1
            continue

        break

    if ampli_sortie <= 50E-3 or essais == 3:
        print(f"La mesure de la fréquence {freq} à trop échoué, passage à la fréquence suivante.")
        continue

    # Si le signal n'est pas entre 2 et 10 périodes de longueur ou s'il n'est pas contenu entre 2 et 2.5 fois l'échelle
    # verticale de la chaine de sortie
    if not (2 / freq <= echelle_hori * 10 <= 10 / freq) or not (
            echelle_vert_sortie * 1.5 <= ampli_sortie <= echelle_vert_sortie * 2.5):
        # on fait un autoset et on attend
        oscillo.write(":AUTOSet")
        time.sleep(2)

    # On ajoute les valeurs aux listes et on calcule leurs incertitudes
    Tension_entree.append(ampli_entree)
    Err_tension_entree.append(ampli_entree * 0.03 + 0.1 * echelle_vert_entree + 1E-3)

    Tension_sortie.append(ampli_sortie)
    Err_tension_sortie.append(ampli_sortie * 0.03 + 0.1 * echelle_vert_sortie + 1E-3)

    Freq_entree_oscillo.append(freq_entree_oscillo)
    Err_freq_entree_oscillo.append(freq_entree_oscillo * 0.00001)

    Phase.append(phase)
    Err_phase.append(3)

# --------------------{Calculs et tracé}---------------------

# On calcule le gain avec des array numpy
Freq_entree_oscillo = array(Freq_entree_oscillo)
Tension_entree = array(Tension_entree)
Tension_sortie = array(Tension_sortie)
Phase = array(Phase)

Err_freq_entree_oscillo = array(Err_freq_entree_oscillo)
Err_tension_entree = array(Err_tension_entree)
Err_tension_sortie = array(Err_tension_sortie)
Err_phase = array(Err_phase)

Gain = 20 * log(abs(Tension_sortie / Tension_entree))
print(Gain)
Err_gain = (20 / log(10)) * ((Err_tension_sortie / Tension_sortie) + (Err_tension_entree / Tension_entree))

# On trace le gain et le déphasage avec les incertitudes
fig, ax = plt.subplots(2, 1, figsize=(12, 10))
fig.suptitle("Diagramme de Bode")

ax[0].plot(Freq_entree_oscillo, Gain, color="purple")
ax[0].fill_between(Freq_entree_oscillo, Gain - Err_gain, Gain + Err_gain, color="purple", alpha=0.2)
ax[0].grid(which="major", color="gainsboro")
ax[0].grid(which="minor", color="gainsboro", ls=":")
ax[0].minorticks_on()
ax[0].set_xlabel("Fréquence (Hz)")
if echelle == "log":
    ax[0].set_xscale("log")
ax[0].set_ylabel("Gain (dB)")

ax[1].plot(Freq_entree_oscillo, Phase, color="orange")
ax[1].fill_between(Freq_entree_oscillo, Phase - Err_phase, Phase + Err_phase, color="orange", alpha=0.2)
ax[1].grid(which="major", color="gainsboro")
ax[1].grid(which="minor", color="gainsboro", ls=":")
ax[1].minorticks_on()
ax[1].set_xlabel("Fréquence (Hz)")
if echelle == "log":
    ax[1].set_xscale("log")
ax[1].set_ylabel("Phase (°)")

if frequence_coupure_case:
    ax[0].axhline(y=-3, ls="--", color="m")



# Tracé des asymptotes :
# Problème avec le fait que les asymptotes ne sont pas droites quand je passe en échelle semi-logarithmique et
# que je peux pas passer en log log pour les asymptotes vu que les gains sont négatifs

# if frequence_coupure_case==True:
# Asymptote du haut :
#   y1_haut=gain[0]
#   y2_haut=gain[1]
#   x1_haut=Freq_entree_oscillo[0]
#   x2_haut=Freq_entree_oscillo[1]
#   coeff_directeur_haut=(y1_haut-y2_haut)/(x1_haut-x2_haut)
#   ordonnee_origine_haut=y1_haut-coeff_directeur_haut*x1_haut
#   asymptote_haut=[coeff_directeur_haut*i+ordonnee_origine_haut for i in Freq_entree_oscillo]
#   asymptote_haut=asymptote_haut
#   ax[0].plot(plage_freq, asymptote_haut,"--",color="gray")
#   ax[0].set_ylim(min(gain)-2, max(gain)+1)

# Asymptote du bas :
#   y1_bas=gain[len(gain)-2]
#   y2_bas=gain[len(gain)-1]
#   x1_bas=Freq_entree_oscillo[len(gain)-2]
#   x2_bas=Freq_entree_oscillo[len(gain)-1]
#   coeff_directeur_bas=(y1_bas-y2_bas)/(x1_bas-x2_bas)
#   ordonnee_origine_bas=y1_bas-coeff_directeur_bas*x1_bas
#   asymptote_bas=[coeff_directeur_bas*i+ordonnee_origine_bas for i in Freq_entree_oscillo]
#   asymptote_bas=asymptote_bas
#   ax[0].plot(plage_freq, asymptote_bas,"--",color="gray")

#   freq_coup=(ordonnee_origine_bas-ordonnee_origine_haut)/(coeff_directeur_haut-coeff_directeur_bas)
#   gain_coup=coeff_directeur_bas*freq_coup+ordonnee_origine_bas
#   ax[0].scatter(freq_coup,gain_coup,color="red", label="fréquence de coupure")

#   ax[0].text(freq_coup, gain_coup, f'({round(freq_coup,2)}, {round(gain_coup,2)})', fontsize=12, ha='right')
#   ax[0].legend()

plt.show()

gestionnaire.close()
