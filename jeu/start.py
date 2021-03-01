# === imports ===
import tkinter as tk
from configparser import ConfigParser
from langue import *
import sys
import os


# === fonctions ===
def ch(fichier):
    """indique le chemin du fichier executé"""
    return os.path.join(sys.path[0], str(fichier))

def creer():
    pass

def param():
    pass

def charger():
    pass

# === lecture paramètres ===
options = ConfigParser()
if os.path.isfile(ch("options.txt")) == False:
    options["DEFAULT"] = {
        "plein_ecran": False,
        "son": True,
        "langue": "fr_FR",
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

# === initialisation écran d'acceuil ===
acceuil = tk.Frame(master=maitre,)
acceuil.place(relheight=1, relwidth=1)

acceuil.rowconfigure(list(range(15)), weight=1)
acceuil.columnconfigure(list(range(7)), weight=1)

I = tk.PhotoImage(file=ch("media/fond.png"))
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

maitre.mainloop()
