import tkinter as tk
from configparser import ConfigParser
import sys
import os

def ch(fichier):
    """indique le chemin du fichier executé"""
    return os.path.join(sys.path[0], str(fichier))

options = ConfigParser()
if os.path.isfile(ch("options.txt")) == False:
    options["DEFAULT"] = {
        "plein_ecran": False,
        "son": True,
    }
else:
    options.read(ch("options.txt"))
print(options["DEFAULT"]["son"])

with open(ch('options.txt'), 'w') as fichier:
    options.write(fichier)

maitre = tk.Tk()
maitre.title("titre")

hauteur_écran = maitre.winfo_screenwidth()
largeur_écran = maitre.winfo_screenheight()

maitre.mainloop()