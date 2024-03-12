import pyvisa
import time
from numpy import *
import matplotlib.pyplot as plt
import sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

#--------------------{Objectifs}---------------------

# Mettre dans le readme quelles références de machines utiliser.
# logarithmique faire gaffe à Vsortie=Ventrée Incertitudes ?
# Afficher les incertitudes
# Se mettre en couplage AC : mesure et trigger et donc mettre le trigger à 0
# remplacer pk2pk par amplitude 
# faire attention si tension trop basse (en-dessous de 10 mV) arrêter les mesures car n'importe quoi
# comparer avec la valeur théorique de la fréquence de coupure 

#Précision 3% en vertical


#--------------------{Préparation des variables globales}---------------------
freq_dep = ""
freq_fin = ""
nb_points = ""
voie_entree = ""
amplitude_entree = ""
voie_sortie = ""
voie_GBF= ""
moyenne_echantillon= ""
amplitude_max=""

#--------------------{Fonctions pour les widgets}---------------------

def validate_freq_dep():
    global freq_dep
    freq_dep = entry1.get()
    freq_dep = freq_dep.replace(",",".")
    try:
        freq_dep = float(freq_dep)
        if 1E-6 < freq_dep < 3E7:
            return True 
        else:
            messagebox.showerror("Erreur", f"Votre fréquence de départ doit être un réel compris entre 1µHz et 30 MHz.\n"
                  f"Vous avez entré {freq_dep} Hz.")
            return False  
    except:
        messagebox.showerror("Erreur", f"Votre fréquence de départ doit être un réel compris entre 1µHz et 30 MHz.\n"
              f"Vous avez entré {freq_dep} Hz.")
        return False
    
def validate_freq_fin():
    global freq_fin
    freq_fin=entry2.get()
    freq_fin=freq_fin.replace(",",".")
    try:
        freq_fin=float(freq_fin)
        if freq_dep < freq_fin < 3E7 :
            return True 
        else :
            messagebox.showerror("Erreur",f"Votre fréquence de fin doit être un réel compris entre {freq_dep} Hz et 30 MHz.\n"
                  f"Vous avez entré {freq_fin} Hz.")
            return False
    except:
        messagebox.showerror("Erreur",f"Vous n'avez pas entré un nombre réel pour la fréquence de fin.\n"
              f"Vous avez entré {freq_fin} Hz.")
        return False
    
def validate_amplitude_entree():
    global amplitude_entree
    global amplitude_max
    amplitude_entree=entry5.get()
    amplitude_entree=amplitude_entree.replace(",",".")
    try:
        amplitude_entree=float(amplitude_entree)
        if 2.5E-3 <= amplitude_entree <= amplitude_max:
            return True
        else :
            messagebox.showerror("Erreur",f"Votre amplitude de signal d'entrée doit être positive.\n"
                  f"Vous avez entré {amplitude_entree} V.")
            return False  
    except:
        messagebox.showerror("Erreur",f"Vous n'avez pas entré un nombre réel.\n"
              f"Vous avez entré {amplitude_entree}.")
        return False
        
def validate_nb_points():
    global nb_points
    nb_points=entry3.get()
    nb_points=nb_points.replace(",",".")
    try:
        nb_points=int(nb_points)
        if nb_points >=1:
            response = messagebox.askquestion("Confirmation",
                                              f"Avec ce nombre de points, votre mesure va durer entre {2+nb_points*1} et {2+nb_points*3} secondes.\n"
                                              "Êtes-vous sûr de vouloir procéder ?")
            if response == 'yes':
                return True
            else:
                return False
            return True 
        else :
            return False  
    except:
        messagebox.showerror("Erreur",f"Vous n'avez pas entré un nombre entier.\n Vous avez entré {nb_points}.")
        return False
    

def get_text():
    global freq_dep
    global freq_fin
    global nb_points
    global amplitude_entree
    global voie_GBF
    global amplitude_max
    if not validate_freq_dep():
       return False
    if not validate_freq_fin():
       return False
    else :
        amplitude_max = None
        if freq_fin < 1E+7:
            amplitude_max = 10
        elif 1E+7 <= freq_fin < 3E+7:
            amplitude_max = 5 
        elif 3E+7 <= freq_fin < 6E+7:
            amplitude_max = 2.5
    print(amplitude_max)
    if not validate_amplitude_entree():
       return False
    if not validate_nb_points():
       return False
    return True 
    print("Texte saisi (Entrée 1) :", freq_dep)
    print("Texte saisi (Entrée 2) :", freq_fin)
    print("Texte saisi (Entrée 3) :", nb_points)
    print("Texte saisi (Entrée 5) :", amplitude_entree)
    
def open_window():
    # Créer une nouvelle fenêtre
    new_window = Toplevel(root)
    new_window.title("Aide")

    # Ajouter du texte à la nouvelle fenêtre
    label = ttk.Label(new_window, text="Gros texte d'aide à insérer plus tard.")
    label.pack(padx=20, pady=20)
    
#--------------------{Définition de la fenêtre principale}---------------------
    
root = Tk()
root.title("Diagramme de Bode")

style = ttk.Style()
style.theme_use('alt')  
style.configure('TButton', background='pink', foreground='black', borderradius=50, padding=10) 
root.configure(bg='green')

frm = ttk.Frame(root, padding=10)
frm.grid()

#--------------------{Les widgets}---------------------

ttk.Label(frm, text="Numéro de voie du signal d'entrée (Oscilloscope): ").grid(column=0, row=1)
voie_entree = IntVar()  # Variable pour stocker la valeur sélectionnée
rdio1 = ttk.Radiobutton(frm, text="1", variable=voie_entree, value=1)
rdio2 = ttk.Radiobutton(frm, text="2", variable=voie_entree, value=2)
rdio1.grid(column=1, row=1)
rdio2.grid(column=2, row=1)

ttk.Label(frm, text="Numéro de voie du générateur : ").grid(column=0, row=2)
voie_GBF = IntVar()  # Variable pour stocker la valeur sélectionnée
rdio3 = ttk.Radiobutton(frm, text="1", variable=voie_GBF, value=1)
rdio4 = ttk.Radiobutton(frm, text="2", variable=voie_GBF, value=2)
rdio3.grid(column=1, row=2)
rdio4.grid(column=2, row=2)

ttk.Label(frm, text="Fréquence de départ (Hz) : ").grid(column=0, row=3)
entry1 = ttk.Entry(frm)
entry1.grid(column=1, row=3, columnspan=2)

ttk.Label(frm, text="Fréquence de fin (Hz) : ").grid(column=0, row=4)
entry2 = ttk.Entry(frm)
entry2.grid(column=1, row=4, columnspan=3)

ttk.Label(frm, text="Nombre de points : ").grid(column=0, row=5)
entry3 = ttk.Entry(frm)
entry3.grid(column=1, row=5, columnspan=2)

ttk.Label(frm, text="Amplitude du signal d'entrée (V) : ").grid(column=0, row=6)
entry5 = ttk.Entry(frm)
entry5.grid(column=1, row=6, columnspan=2)

ttk.Label(frm,text="Nombre d'échantillons utilisés pour le tracé : ").grid(column=0, row=7)
options_moyenne = ["2", "4","8","16","32","64","128","256"]
moyenne_echantillon = StringVar()
moyenne_echantillon_combobox=ttk.Combobox(frm, values=options_moyenne, textvariable=moyenne_echantillon)
moyenne_echantillon_combobox.grid(column=1, row=7, columnspan=2)
moyenne_echantillon_combobox.current(0)

#Pour ajouter un espace avant les boutons :
ttk.Label(frm, text="").grid(column=0, row=8)


#--------------------{fonctions pour les boutons}---------------------

def get_text_and_destroy():
    if get_text():
        root.destroy() # si get_text() on continue en tuant la fenêtre

        
    
def quit_program():
    root.destroy()
    sys.exit()

#--------------------{Les boutons au bottom}---------------------


ttk.Button(frm, text="Valider", command=get_text_and_destroy).grid(column=1, row=9)
ttk.Button(frm, text="Aide", command=open_window).grid(column=0, row=9)
ttk.Button(frm, text="Quitter", command=quit_program).grid(column=2, row=9)


root.mainloop()

#--------------------{Vérification des variables globales}---------------------

print("Valeur de freq_dep en dehors de root.mainloop() :", freq_dep)
print("Valeur de freq_fin en dehors de root.mainloop() :", freq_fin)
print("Valeur de nb_points en dehors de root.mainloop() :", nb_points)
voie_entree=voie_entree.get() #Je récupère la valeur de voie_entree

#Pour avoir voie_sortie :
if voie_entree==1:
    voie_sortie=2
else :
    voie_sortie=1
    
print("Valeur de voie_entree en dehors de root.mainloop() :", voie_entree)
print("Valeur de voie_sortie en dehors de root.mainloop() :", voie_sortie)
print("Valeur de amplitude_entree en dehors de root.mainloop() :", amplitude_entree)
voie_GBF=voie_GBF.get()
print("Valeur de voie_GBF en dehors de root.mainloop() :", voie_GBF)
moyenne_echantillon=moyenne_echantillon.get()
print("Valeur de moyenne_echantillon en dehors de root.mainloop() :", voie_GBF)



#--------------------{Récupération des ports}---------------------

gestionnaire = pyvisa.ResourceManager()

listePorts = gestionnaire.list_resources('?*')

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
        
#--------------------{Définition du signal d'entrée}---------------------


GBF.write(f":Source{voie_entree}:APPLy:sin")
GBF.write(f":Source{voie_entree}:VOLT {amplitude_entree}")
GBF.write(f":Source{voie_entree}:frequence {freq_dep}")
GBF.write(f":output{voie_GBF} ON") 

#--------------------{Réglages oscilloscope}---------------------

oscillo.write(f":ACQuire:MODe AVERage")
oscillo.write(f":ACQuire:AVERage {moyenne_echantillon}")
oscillo.write(f":TRIGger:COUPle AC")

#pour le coupling AC voir page 44


#--------------------{Balayage des fréquences}---------------------

plage_freq = list(logspace(log10(freq_dep), log10(freq_fin), nb_points))
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

oscillo.write(":AUTOSet")
time.sleep(2)

for freq in plage_freq:
    
    GBF.write(f":Source{voie_entree}:FREQ {freq}")
    time.sleep(1)
    
    oscillo.write(f":MEASure:SOURce1 CH{voie_sortie}")
    ampli = float(oscillo.query(":MEASure:PK2Pk?"))
    
    echelle_hori = float(oscillo.query(":timebase:scale?"))
    echelle_vert = float(oscillo.query(f":channel{voie_sortie}:scale?"))
    
    if not (2/freq <= echelle_hori*10 <= 10/freq) or not(echelle_vert*2 <= ampli <= echelle_vert*3):
        oscillo.write(":AUTOSet")
        time.sleep(2)

    oscillo.write(f":MEASure:SOURce1 CH{voie_entree}")
    tension_entree.append(float(oscillo.query(":MEASure:PK2Pk?")))
    freq_entree_oscillo.append(float(oscillo.query(":MEASure:FREQuency?")))

    oscillo.write(f":MEASure:SOURce1 CH{voie_sortie}")
    tension_sortie.append(float(oscillo.query(":MEASure:PK2Pk?")))
    
    oscillo.write(f":MEASure:SOURce1 CH{voie_entree}")
    oscillo.write(f":MEASure:SOURce2 CH{voie_sortie}")
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