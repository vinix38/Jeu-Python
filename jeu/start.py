# === imports ===
import tkinter as tk
import datetime as dt
from configparser import ConfigParser, DEFAULTSECT
from fractions import Fraction
from tkinter.messagebox import showinfo
from langue import *
import sys
import os


# === chemins ===
def ch(fichier):
    """
    indique le chemin du fichier executé
    """
    return os.path.join(sys.path[0], str(fichier))

#resize
def dim(L, H, img):
    """
    Largeur (px), Hauteur (px), image
    redimensionne l'image aux dimensions souhaitées
    """
    print(L, H)
    H = (Fraction(str(H/img.height()))).limit_denominator(100)
    L = (Fraction(str(L/img.width()))).limit_denominator(100)
    print(L, H)
    img.subsample(L.denominator, H.denominator)
    img.zoom(L.numerator, H.numerator)

    return img

# === lecture paramètres ===
options = ConfigParser()
if os.path.isfile(ch("options.txt")) == False:
    options["DEFAULT"] = {
        "plein_ecran": True,
        "taille" : "1920x1080",
        "taille_dispo" : "1920x1080,1366x768,1440x900,1600x900,1280x800,1280x1024,1024x768",
        "son": True,
        "langue": "fr_FR",
        "langues_dispo": "fr_FR,en_US"
    }
    with open(ch('options.txt'), 'w') as fichier:
        options.write(fichier)
else:
    options.read(ch("options.txt"))

parties = ConfigParser()
if os.path.isfile(ch("parties.txt")):
    parties.read(ch("parties.txt"))
else:
    with open(ch('parties.txt'), 'w') as fichier:
        parties.write(fichier)


# === localisation ===
loc = {}
exec("loc = " + options["DEFAULT"]["langue"])


# === initialisation fenêtre ===
maitre = tk.Tk()
maitre.title(loc["titre"])
maitre.resizable(0, 0)
H_E = maitre.winfo_screenheight()
L_E = maitre.winfo_screenwidth()


# === prise en compte plein écran ===
if options["DEFAULT"].getboolean("plein_ecran"):
    maitre.attributes('-fullscreen', True)
    H_F, L_F = H_E, L_E
else:
    maitre.geometry(options["DEFAULT"]["taille"])
    L_F, H_F = [int(i) for i in options["DEFAULT"]["taille"].split("x")]
    


# === images ===
img = {
    #"V--" : tk.PhotoImage(file=ch("media/V--.png")),
    "I" : dim(L_F, H_F, tk.PhotoImage(file=ch("media/calibrator.png"))),
}



# === fonctions ===
def efface():
    global maitre
    for enfant in maitre.winfo_children():
        enfant.destroy()


# ***====== FENETRES ======***
def acceuil():
    global maitre
    global options
    global img

    efface()

    F_acceuil = tk.Frame(master=maitre)
    F_acceuil.place(relheight=1, relwidth=1)

    F_acceuil.rowconfigure(list(range(15)), weight=1)
    F_acceuil.columnconfigure(list(range(7)), weight=1)

    fond = tk.Label(F_acceuil, image=img["I"])
    fond.place(x=0, y=0, relwidth=1, relheight=1)

    B_quitter = tk.Button(
        text=loc["quitter"],
        fg="black",
        bg="grey",
        master=F_acceuil,
        command=maitre.destroy,
    )
    B_options = tk.Button(
        text=loc["options"],
        bg="grey",
        fg="black",
        master=F_acceuil,
        command=param,
    )
    B_charger = tk.Button(
        text=loc[">partie"],
        bg="grey",
        fg="black",
        master=F_acceuil,
        command=charger,
    )
    B_creer = tk.Button(
        text=loc["+partie"],
        bg="grey",
        fg="black",
        master=F_acceuil,
        command=creer,
    )

    B_quitter.grid(column=3, row=12, sticky="nswe")
    B_options.grid(column=3, row=10, sticky="nswe")
    B_charger.grid(column=3, row=8, sticky="nswe")
    B_creer.grid(column=3, row=6, sticky="nswe")


def creer():
    global parties
    global maitre
    global img
    
    efface()
    
    F_creer = tk.Frame(maitre)
    F_creer.place(relheight=1,relwidth=1)
    F_creer.rowconfigure([0,1],weight=1)
    F_creer.columnconfigure([0,1],weight=1)
    
    E_creer = tk.Entry(
        master=F_creer,
        bg = "black",
        fg = "white",
    )
    def creation():
        nonlocal E_creer
        nom = E_creer.get()
        if nom in parties.sections():
            showinfo(loc["err"], loc["déjà"])
        else:
            parties[nom] = {
                "niv" : "00",
                "score" : 0,
                "temps" : 0,
                "inv" : "",
                "pos" : "00;00"
            }
            with open(ch("parties.txt")) as fichier:
                parties.write(fichier)
            jeu()
    
    B_creer = tk.Button(
        master=F_creer,
        bg="grey",
        fg="black",
        text=loc["creer"],
        command=creation,
    )
    B_annuler = tk.Button(
        master=F_creer,
        bg="grey",
        fg="black",
        text=loc["annuler"],
        command=acceuil,        
    )
    
    E_creer.grid(row=0,column=0,columnspan=2,sticky="nswe")
    B_annuler.grid(row=1,column=0,sticky="nswe")
    B_creer.grid(row=1,column=1,sticky="nswe")

def param():
    global options
    global maitre
    global img

    efface()

    F_param = tk.Frame(master=maitre)
    F_param.place(relheight=1, relwidth=1)
    F_param.rowconfigure(list(range(10)), weight=1)
    F_param.columnconfigure(list(range(10)), weight=1)

        
    opt = options["DEFAULT"]["langues_dispo"].split(",")
    clic = (tk.StringVar())
    clic.set(options["DEFAULT"]["langue"])
        
    V_son = tk.StringVar()
    V_son.set(options["DEFAULT"]["son"])
    
    V_plein = tk.StringVar()
    V_plein.set(options["DEFAULT"]["plein_ecran"])

    def sono():
        options["DEFAULT"]["son"] = V_son.get()
        
    def plein():
        options["DEFAULT"]["plein_ecran"] = V_plein.get()
        
    def quitter_sans():
        options.read(ch("options.txt"))
        acceuil()

    def quitter_avec():
        with open(ch('options.txt'), 'w') as fichier:
            options.write(fichier)
        acceuil()

    afond = tk.Label(F_param, image=img["I"])
    afond.place(x=0, y=0, relwidth=1, relheight=1)

    B_langue = tk.OptionMenu(
        F_param,
        clic,
        *opt,
    )
    B_son = tk.Checkbutton(
        master=F_param,
        bg="grey",
        fg="black",
        text=loc["son"],
        command=sono,
        onvalue="True", 
        offvalue="False",
        variable = V_son,
    )
    B_plein = tk.Checkbutton(
        master=F_param,
        bg="grey",
        fg="black",
        text=loc["plein"],
        command=plein,
        onvalue="True", 
        offvalue="False",
        variable = V_plein,
    )
    B_quitter_sauv = tk.Button(
        master=F_param,
        bg="grey",
        fg="black",
        text=loc["q+sauv"],
        command=quitter_avec,
    )
    B_quitter_sans = tk.Button(
        master=F_param,
        bg="grey",
        fg="black",
        text=loc["q-sauv"],
        command=quitter_sans,
    )

    def change(*args):
        options["DEFAULT"]["langue"] = clic.get()
    clic.trace('w', change)

    B_langue.grid(row=2, column=4, sticky="nswe")
    B_plein.grid(row=3, column=4, sticky="nswe")
    B_quitter_sauv.grid(row=7, column=4, sticky="nswe")
    B_quitter_sans.grid(row=5, column=4, sticky="nswe")
    B_son.grid(row=4, column=4, sticky="nswe")


def charger():
    global options
    global maitre
    global img
    global parties

    efface()

    F_charge = tk.Frame(maitre)
    F_charge.place(relheight=1, relwidth=1)

    F_liste = tk.Frame(F_charge)
    F_liste.place(relheight=0.9, relwidth=1)

    F_barre = tk.Frame(F_charge)
    F_barre.place(relheight=0.1, relwidth=1, rely=0.9)
    F_barre.rowconfigure(0, weight=1)
    F_barre.columnconfigure([0, 1, 2], weight=1)

    parties.read(ch("parties.txt"))
    sauv = parties.sections()

    if sauv != []:
        roue = tk.Scrollbar(F_liste)
        roue.pack(side="right", fill="Y")

        B_liste = tk.Listbox(
            maitre=F_liste,
            height=len(sauv),
            selectmode="SINGLE",
            width=l_ecran,
            yscrollcommand=roue.set,
        )

        for x in sauv:
            B_liste.insert("END", x.upper() + "\t" + loc["XP"] + " : " + parties[x]["score"] +
                           " | " + loc["niv"] + " : " + parties[x]["niv"] + " | " + parties[x]["temps"])

        def charge():
            a = B_liste.get()
            print(a)
            
        B_liste.pack()

    else:
        vide = tk.Label(
            master=F_liste,
            text=loc["-sauv"]
        )
        vide.pack(fill="both")

        def charge():
            pass

    B_retour = tk.Button(
        master=F_barre,
        text=loc["retour"],
        bg="grey",
        fg="black",
        command=acceuil,
    )
    B_charger = tk.Button(
        master=F_barre,
        text=loc["charger"],
        bg="grey",
        fg="black",
        command=charge,
    )
    B_importer = tk.Button(
        master=F_barre,
        text=loc["import"],
        bg="grey",
        fg="black",
        command=None,
    )

    B_importer.grid(row=0, column=0, sticky="nswe")
    B_retour.grid(row=0, column=1, sticky="nswe")
    B_charger.grid(row=0, column=2, sticky="nswe")

def jeu(sauv):
    global maitre
    global options
    global parties
    global img
    
    def quitter():
        nonlocal sauv
        with open(ch("parties.txt")) as fichier:
            pass
        acceuil()
    
    F_jeu = tk.Frame(maitre)
    F_jeu.place(relheight=1,relwidth=1)
    
    F_carte = tk.Frame(F_jeu)
    F_carte.place(relheight=1,relwidth=0.8)
    
    F_barre = tk.Frame(F_jeu)
    F_barre.place(relheight=1,relwidth=0.2,relx=0.8)
    
    F_barre.rowconfigure(list(range(10)), weight=1)
    F_barre.columnconfigure([0, 1, 2], weight=1)
    
    B_quitter = tk.Button(
        master=F_barre,
        bg = "grey",
        command = quitter,
    )

acceuil()

maitre.mainloop()
