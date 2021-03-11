# ====== IMPORTS ======
import tkinter as tk
import datetime as dt
from configparser import ConfigParser
from fractions import Fraction
from tkinter.messagebox import showinfo
from tkinter import ttk
from langue import lang
from niveaux import niv
import sys
import os

# === déclaration fenêtre ===
maitre = tk.Tk()
maitre.resizable(0, 0)
# maitre.iconbitmap(ch("*.ico"))
H_E = maitre.winfo_screenheight()
L_E = maitre.winfo_screenwidth()

# === styles ===
style = {
    "font": ('Helvetica', 11),
    "background": "grey",
    "foreground": "black",
}
ttkStyle = ttk.Style(maitre)
ttkStyle.configure(
    "TMenubutton",
    **style
)

# === chemins ===
def ch(fichier):
    """
    (fichier)\n
    indique le chemin absolu du fichier executé
    """
    return os.path.join(sys.path[0], str(fichier))

# === changement de taille ===
def dim(L, H, img):
    """
    (Largeur (px), Hauteur (px), image)\n
    redimensionne l'image aux dimensions souhaitées
    """
    H = (Fraction(str(H/img.height()))).limit_denominator(100)
    L = (Fraction(str(L/img.width()))).limit_denominator(100)
    return img.zoom(L.numerator, H.numerator).subsample(L.denominator, H.denominator)

# === tout effacer ===
def efface(parent):
    """
    (parent)\n
    Efface tous les widgets présents dans le parent indiqué
    """
    for enfant in parent.winfo_children():
        enfant.destroy()

# ====== changer langue ======
def localisation():
    """
    ()\n
    Change la langue
    """
    global loc
    global lang
    global options
    global maitre
    loc = lang[options["DEFAULT"]["langue"]]
    maitre.title(loc["titre"])

# === prise en compte plein écran ===
def ecran():
    """
    ()\n
    Redimensionne la taille de l'écran
    """
    global maitre
    global options
    global H_E, L_E
    if options["DEFAULT"].getboolean("plein_ecran"):
        maitre.attributes('-fullscreen', True)
        return L_E, H_E
    else:
        maitre.attributes('-fullscreen', False)
        maitre.geometry(options["DEFAULT"]["taille"])
        return tuple(int(i) for i in options["DEFAULT"]["taille"].split("x"))

# ====== VARIABLES ======
temp = {}
img = {
    "V--": tk.PhotoImage(file=ch("media/V--.png")),
    "I": tk.PhotoImage(file=ch("media/fond.png")),
    "MPC": tk.PhotoImage(file=ch("media/MPC.png")),
    "MPF": tk.PhotoImage(file=ch("media/MPF.png")),
    "MPD": tk.PhotoImage(file=ch("media/MPD.png")),
    "perso": tk.PhotoImage(file=ch("media/MPC--.png")),
}

# === lecture des paramètres ===
options = ConfigParser()
if os.path.isfile(ch("options.txt")) == False:
    options["DEFAULT"] = {
        "plein_ecran": True,
        "taille": "1920x1080",
        "taille_dispo": "1920x1080,1366x768,1440x900,1600x900,1280x800,1280x1024,1024x768",
        "son": True,
        "langue": "fr_FR",
        "langues_dispo": "fr_FR,en_US"
    }
    with open(ch('options.txt'), 'w') as fichier:
        options.write(fichier)
else:
    options.read(ch("options.txt"))

# === lecture des parties sauvegardées ===
parties = ConfigParser()
if os.path.isfile(ch("parties.txt")):
    parties.read(ch("parties.txt"))
else:
    with open(ch('parties.txt'), 'w') as fichier:
        parties.write(fichier)

localisation()
L_F, H_F = ecran()

# ***====== FENETRES ======***
def acceuil():
    global maitre
    global options
    global img

    efface(maitre)

    F_acceuil = tk.Frame(master=maitre)
    F_acceuil.place(relheight=1, relwidth=1)

    F_acceuil.rowconfigure(list(range(15)), weight=1)
    F_acceuil.columnconfigure(list(range(7)), weight=1)

    temp["I"] = dim(L_F, H_F, img["I"])

    fond = tk.Label(F_acceuil, image=temp["I"])
    fond.place(x=0, y=0, relwidth=1, relheight=1)

    B_quitter = tk.Button(
        text=loc["quitter"],
        master=F_acceuil,
        command=maitre.destroy,
        **style,
    )
    B_options = tk.Button(
        text=loc["options"],
        master=F_acceuil,
        command=param,
        **style,
    )
    B_charger = tk.Button(
        text=loc[">partie"],
        master=F_acceuil,
        command=charger,
        **style,
    )
    B_creer = tk.Button(
        text=loc["+partie"],
        master=F_acceuil,
        command=creer,
        **style,
    )

    B_quitter.grid(column=3, row=12, sticky="nswe")
    B_options.grid(column=3, row=10, sticky="nswe")
    B_charger.grid(column=3, row=8, sticky="nswe")
    B_creer.grid(column=3, row=6, sticky="nswe")


def creer():
    global parties
    global maitre
    global img

    efface(maitre)

    F_creer = tk.Frame(maitre)
    F_creer.place(relheight=1, relwidth=1)
    F_creer.rowconfigure([0, 1], weight=1)
    F_creer.columnconfigure([0, 1], weight=1)

    E_creer = tk.Entry(
        master=F_creer,
        **style,
    )

    def creation():
        nonlocal E_creer
        nom = E_creer.get()
        if nom in parties.sections():
            showinfo(loc["err"], loc["déjà"])
        else:
            parties[nom] = {
                "niv": "11",
                "score": 0,
                "inv": "",
                "pos": "",
                "S_niv": "11",
                "S_score": 0,
                "S_inv": "",
                "temps": 0,
            }
            with open(ch("parties.txt"), "w") as fichier:
                parties.write(fichier)
            jeu(nom)

    B_creer = tk.Button(
        master=F_creer,
        text=loc["creer"],
        command=creation,
        **style,
    )
    B_annuler = tk.Button(
        master=F_creer,
        text=loc["annuler"],
        command=acceuil,
        **style,
    )

    E_creer.grid(row=0, column=0, columnspan=2, sticky="nswe")
    B_annuler.grid(row=1, column=0, sticky="nswe")
    B_creer.grid(row=1, column=1, sticky="nswe")


def param():
    global options
    global maitre
    global img

    efface(maitre)

    F_param = tk.Frame(master=maitre)
    F_param.place(relheight=1, relwidth=1)
    F_param.rowconfigure(list(range(10)), weight=1)
    F_param.columnconfigure(list(range(10)), weight=1)

    opt_l = options["DEFAULT"]["langues_dispo"].split(",")
    clic_l = tk.StringVar()

    opt_r = options["DEFAULT"]["taille_dispo"].split(",")
    clic_r = tk.StringVar()

    V_son = tk.StringVar(value=options["DEFAULT"]["son"])

    V_plein = tk.StringVar(value=options["DEFAULT"]["plein_ecran"])

    def sono():
        options["DEFAULT"]["son"] = V_son.get()

    def plein():
        options["DEFAULT"]["plein_ecran"] = V_plein.get()

    def quitter_sans():
        options.read(ch("options.txt"))
        acceuil()

    def quitter_avec():
        global L_F, H_F
        with open(ch('options.txt'), 'w') as fichier:
            options.write(fichier)
        localisation()
        L_F, H_F = ecran()
        acceuil()

    afond = tk.Label(F_param, image=img["I"])
    afond.place(x=0, y=0, relwidth=1, relheight=1)

    B_langue = ttk.OptionMenu(
        F_param,
        clic_l,
        options["DEFAULT"]["langue"],
        *opt_l,
    )
    B_taille = ttk.OptionMenu(
        F_param,
        clic_r,
        options["DEFAULT"]["taille"],
        *opt_r,
    )
    B_son = tk.Checkbutton(
        master=F_param,
        text=loc["son"],
        command=sono,
        onvalue="True",
        offvalue="False",
        variable=V_son,
        **style,
    )
    B_plein = tk.Checkbutton(
        master=F_param,
        text=loc["plein"],
        command=plein,
        onvalue="True",
        offvalue="False",
        variable=V_plein,
        **style,
    )
    B_quitter_sauv = tk.Button(
        master=F_param,
        text=loc["q+sauv"],
        command=quitter_avec,
        **style,
    )
    B_quitter_sans = tk.Button(
        master=F_param,
        text=loc["q-sauv"],
        command=quitter_sans,
        **style,
    )

    def C_langue(*args):
        options["DEFAULT"]["langue"] = clic_l.get()
    clic_l.trace('w', C_langue)

    def C_taille(*args):
        options["DEFAULT"]["taille"] = clic_r.get()
        V_plein.set("False")
        plein()
    clic_r.trace('w', C_taille)

    B_taille.grid(row=5, column=4, sticky="nswe")
    B_langue.grid(row=2, column=4, sticky="nswe")
    B_plein.grid(row=4, column=4, sticky="nswe")
    B_quitter_sauv.grid(row=9, column=4, sticky="nswe")
    B_quitter_sans.grid(row=8, column=4, sticky="nswe")
    B_son.grid(row=4, column=6, sticky="nswe")


def charger():
    global options
    global maitre
    global img
    global parties

    efface(maitre)

    F_charge = tk.Frame(maitre)
    F_charge.place(relheight=1, relwidth=1)

    F_liste = tk.Frame(F_charge)
    F_liste.place(relheight=0.9, relwidth=1)

    F_barre = tk.Frame(F_charge)
    F_barre.place(relheight=0.1, relwidth=1, rely=0.9)
    F_barre.rowconfigure(0, weight=1)
    F_barre.columnconfigure([0, 1, 2], weight=1)

    B_retour = tk.Button(
        master=F_barre,
        text=loc["retour"],
        command=acceuil,
        **style,
    )
    B_charger = tk.Button(
        master=F_barre,
        text=loc["charger"],
        command=lambda: jeu(sauv[B_liste.curselection()[0]]),
        **style,
    )
    B_importer = tk.Button(
        master=F_barre,
        text=loc["import"],
        command=None,
        **style,
    )

    parties.read(ch("parties.txt"))
    sauv = parties.sections()

    if sauv != []:
        roue = tk.Scrollbar(F_liste)
        roue.pack(side="right", fill="y")

        B_liste = tk.Listbox(
            master=F_liste,
            height=len(sauv),
            selectmode="single",
            width=L_F,
            yscrollcommand=roue.set,
            **style,
        )
        for x in sauv:
            B_liste.insert("end", x + "|" + loc["XP"] + " : " + parties[x]["score"] +
                           " | " + loc["niv"] + " : " + parties[x]["niv"] + " | " + parties[x]["temps"])
        B_liste.pack()

    else:
        vide = tk.Label(
            master=F_liste,
            text=loc["-sauv"],
            **style,
        )
        vide.pack(fill="both")
        B_charger.config(state="disabled")

    B_importer.grid(row=0, column=0, sticky="nswe")
    B_retour.grid(row=0, column=1, sticky="nswe")
    B_charger.grid(row=0, column=2, sticky="nswe")


def jeu(nom):
    global maitre
    global options
    global parties
    global img

    efface(maitre)

    def quitter():
        with open(ch("parties.txt"), "w") as fichier:
            parties.write(fichier)
        acceuil()

    F_jeu = tk.Frame(maitre, background=None)
    F_jeu.place(relheight=1, relwidth=1)

    F_carte = tk.Frame(F_jeu, background=None)
    F_carte.place(relheight=1, relwidth=0.8)

    F_barre = tk.Frame(F_jeu, background=None)
    F_barre.place(relheight=1, relwidth=0.2, relx=0.8)

    F_barre.rowconfigure(list(range(10)), weight=1)
    F_barre.columnconfigure([0, 1, 2], weight=1)

    def charge(n):
        global niv
        global img
        global temp
        nonlocal F_carte
        temp = {}
        efface(F_carte)
        li = int(niv[n]["li"])
        col = int(niv[n]["col"])
        x = min((L_F * 0.8) // col, H_F // li)

        F_terrain = tk.Canvas(
            F_carte,
            height=li*x,
            width=col*x,
        )
        F_terrain.place(relx=0.5, rely=0.5, anchor="center")
        F_terrain.create_image(0, 0, image=img["I"], anchor="nw", tag="fond")

        for i in range(li):
            for j in range(col):
                s = niv[n]["grille"][i][j]
                if s in temp:
                    image = temp[s]
                else:
                    image = dim(x, x, img[s])
                    temp[s] = image
                F_terrain.create_image(
                    j*x,
                    i*x,
                    image=image,
                    anchor="nw",
                    tag="case"
                )

        if parties[nom]["pos"] == "":
            parties[nom]["pos"] = str(niv[n]["def_pos"][0] - 1) \
                                    + ";" + str(niv[n]["def_pos"][1] - 1)

        
        image = dim(x, x, img["perso"])
        temp["perso"] = image
        F_terrain.create_image(
            int(parties[nom]["pos"].split(";")[0]) * x,
            int(parties[nom]["pos"].split(";")[1]) * x,
            image=image,
            tag="perso",
            anchor="nw",
        )

    B_quitter = tk.Button(
        master=F_barre,
        text=loc["quitter"],
        command=quitter,
        **style,
    )

    B_quitter.grid(row=9, column=1, sticky="nswe")

    charge(parties[nom]["niv"])


acceuil()

maitre.mainloop()
