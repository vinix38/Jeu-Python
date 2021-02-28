#=== imports ===
import tkinter as tk
from configparser import ConfigParser
from langue import *
import sys
import os

#=== fonctions ===
def ch(fichier):
    """indique le chemin du fichier executé"""
    return os.path.join(sys.path[0], str(fichier))

#=== lecture paramètres ===
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
    
#localisation
loc = {}
exec("loc = "+ options["DEFAULT"]["langue"])

#=== initialisation fenêtre ===
maitre = tk.Tk()
maitre.title(loc["titre1"])
maitre.resizable(0, 0)

h_ecran = maitre.winfo_screenheight()
l_ecran = maitre.winfo_screenwidth()

if options["DEFAULT"].getboolean("plein_ecran"):
    maitre.attributes('-fullscreen',True)

acceuil = tk.Frame(master=maitre)
acceuil.rowconfigure([0, 1, 2], minsize=100, weight=1)
acceuil.columnconfigure([0, 1, 2], minsize=100, weight=1)
acceuil.grid()

I = tk.PhotoImage(file = ch("media/fond.png"))

fond = tk.Canvas(
    master=acceuil,
    height=h_ecran,
    width=l_ecran,
    bg="#ff0"
)
fond.grid()
fond.create_image(0, 0, image=I,anchor = "nw")

quitter = tk.Button(
    text=loc["quitter"],
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    master=acceuil,
)

maitre.mainloop()