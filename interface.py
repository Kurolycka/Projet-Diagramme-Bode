#Tests interface

#--------------------{Importation des modules}---------------------

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

#--------------------{Préparation des variables globales}---------------------
freq_dep = ""
freq_fin = ""
nb_points = ""
voie_entree = ""
amplitude_entree = ""
voie_sortie = ""

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
    amplitude_entree=entry5.get()
    amplitude_entree=amplitude_entree.replace(",",".")
    try:
        amplitude_entree=float(amplitude_entree)
        if 0 < amplitude_entree:
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
                                              f"Avec ce nombre de points, votre mesure va durer {nb_points * 2} secondes.\n"
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
    
def validate_voie_entree():
    global voie_entree
    global voie_sortie
    voie_entree=entry4.get()
    voie_entree=voie_entree.replace(",",".")
    try :
        voie_entree=int(voie_entree)
        if voie_entree==1 or voie_entree==2:
            if voie_entree==1:
                voie_sortie=2
            else :
                voie_sortie=1
            return True
        else :
            messagebox.showerror("Erreur",f"Vous n'avez pas choisi 1 ou 2 comme voie d'entrée.")
            return False
    except:
        messagebox.showerror("Erreur",f"Vous n'avez pas entré un nombre entier.\n Vous avez entré {voie_entree}.")
        return False 
    

def get_text():
    global freq_dep
    global freq_fin
    global nb_points
    global voie_entree
    global amplitude_entree
    global voie_sortie
    if not validate_freq_dep():
       return
    if not validate_freq_fin():
       return
    if not validate_nb_points():
       return
    if not validate_voie_entree():
        return
    if not validate_amplitude_entree():
       return
    print("Texte saisi (Entrée 1) :", freq_dep)
    print("Texte saisi (Entrée 2) :", freq_fin)
    print("Texte saisi (Entrée 3) :", nb_points)
    print("Texte saisi (Entrée 4) :", voie_entree)
    print("Texte saisi (Entrée 5) :", amplitude_entree)
    print("Voie sortie par défaut :", voie_sortie)
    
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

ttk.Label(frm, text="Fréquence de départ (Hz) : ").grid(column=0, row=1)
entry1 = ttk.Entry(frm)
entry1.grid(column=1, row=1)

ttk.Label(frm, text="Fréquence de fin (Hz) : ").grid(column=0, row=2)
entry2 = ttk.Entry(frm)
entry2.grid(column=1, row=2)

ttk.Label(frm, text="Nombre de points : ").grid(column=0, row=3)
entry3 = ttk.Entry(frm)
entry3.grid(column=1, row=3)

ttk.Label(frm, text="Numéro de voie du signal d'entrée : ").grid(column=0, row=4)
entry4 = ttk.Entry(frm)
entry4.grid(column=1, row=4)

ttk.Label(frm, text="Amplitude du signal d'entrée (V) : ").grid(column=0, row=5)
entry5 = ttk.Entry(frm)
entry5.grid(column=1, row=5)

#Pour ajouter un espace avant les boutons :
ttk.Label(frm, text="").grid(column=0, row=6)

#--------------------{Les boutons au bottom}---------------------

ttk.Button(frm, text="Valider", command=get_text).grid(column=1, row=7)
ttk.Button(frm, text="Aide", command=open_window).grid(column=0, row=7)
ttk.Button(frm, text="Quitter", command=root.destroy).grid(column=2, row=7)


root.mainloop()

#--------------------{Vérification des variables globales}---------------------

print("Valeur de freq_dep en dehors de root.mainloop() :", freq_dep)
print("Valeur de freq_fin en dehors de root.mainloop() :", freq_fin)
print("Valeur de nb_points en dehors de root.mainloop() :", nb_points)
print("Valeur de voie_entree en dehors de root.mainloop() :", voie_entree)
print("Valeur de amplitude_entree en dehors de root.mainloop() :", amplitude_entree)
