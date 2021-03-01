# === imports ===
import tkinter as tk
from configparser import ConfigParser
from langue import *
import sys
import os

# === chemins ===
def ch(fichier):
    """indique le chemin du fichier executé"""
    return os.path.join(sys.path[0], str(fichier))

# === lecture paramètres ===
options = ConfigParser()
if os.path.isfile(ch("options.txt")) == False:
    options["DEFAULT"] = {
        "plein_ecran": True,
        "son": True,
        "langue": "fr_FR",
        "langues_dispo": "fr_FR,en_US"
    }
    with open(ch('options.txt'), 'w') as fichier:
        options.write(fichier)
else:
    options.read(ch("options.txt"))
    
# === localisation ===
loc = {}
exec("loc = " + options["DEFAULT"]["langue"])
    
# === initialisation fenêtre ===
maitre = tk.Tk()
maitre.title(loc["titre"])
maitre.resizable(0, 0)
h_ecran = maitre.winfo_screenheight()
l_ecran = maitre.winfo_screenwidth()

# === prise en compte plein écran ===
if options["DEFAULT"].getboolean("plein_ecran"):
    maitre.attributes('-fullscreen', True)

#=== images ===
I = tk.PhotoImage(file=ch("media/fond.png"))

#=== fonctions ===
def efface():
    global maitre
    for enfant in maitre.winfo_children():
        enfant.destroy()

#***====== FENETRE ======***
def acceuil():
    global maitre
    global options
    global I
    
    efface()
    
    acceuil = tk.Frame(master=maitre)
    acceuil.place(relheight=1, relwidth=1)

    acceuil.rowconfigure(list(range(15)), weight=1)
    acceuil.columnconfigure(list(range(7)), weight=1)

    fond = tk.Label(acceuil, image=I)
    fond.place(x=0, y=0, relwidth=1, relheight=1)

    B_quitter = tk.Button(
        text=loc["quitter"],
        bg="grey",
        fg="black",
        master=acceuil,
        command=lambda: maitre.destroy(),
    )
    B_options = tk.Button(
        text=loc["options"],
        bg="grey",
        fg="black",
        master=acceuil,
        command=param,
    )
    B_charger = tk.Button(
        text=loc[">partie"],
        bg="grey",
        fg="black",
        master=acceuil,
        command=charger,
    )
    B_creer = tk.Button(
        text=loc["+partie"],
        bg="grey",
        fg="black",
        master=acceuil,
        command=creer,
    )

    B_quitter.grid(column=3, row=12, sticky="nswe")
    B_options.grid(column=3, row=10, sticky="nswe")
    B_charger.grid(column=3, row=8, sticky="nswe")
    B_creer.grid(column=3, row=6, sticky="nswe")


def creer():
    pass

def param():
    global options
    global maitre
    global I
    
    efface()
    
    param = tk.Frame(master=maitre)
    param.place(relheight=1, relwidth=1)
    param.rowconfigure(list(range(10)), weight=1)
    param.columnconfigure(list(range(10)), weight=1)
    
    def quitter_sans():
        options.read(ch("options.txt"))
        acceuil()
    
    def quitter_avec():
        with open(ch('options.txt'), 'w') as fichier:
            options.write(fichier)
        acceuil()
    
    #temporaire***********
    afond = tk.Label(param, image = I)
    afond.place(x=0, y=0, relwidth=1, relheight=1)
    
    opt = list(options["DEFAULT"]["langues_dispo"].split(","))
    clic = tk.StringVar()
    clic.set(options["DEFAULT"]["langue"])
    B_langue = tk.OptionMenu(param, clic, *opt)
    
    B_quitter_sauv = tk.Button(
        master = param,
        bg = "grey",
        fg = "black",
        text = loc["q+sauv"],
        command=quitter_avec,
    )
    B_quitter_sans = tk.Button(
        master = param,
        bg = "grey",
        fg = "black",
        text = loc["q-sauv"],
        command=quitter_sans,
    )
    
    def change(*args):
        options["DEFAULT"]["langue"] = clic.get()
    clic.trace('w', change)

    B_langue.grid(row=3,column=4,sticky="nswe")
    B_quitter_sauv.grid(row=7,column=4,sticky="nswe")
    B_quitter_sans.grid(row=5,column=4,sticky="nswe")

def charger():
    pass


acceuil()

maitre.mainloop()
