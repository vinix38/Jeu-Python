# === imports ===
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

temp = {}


# === chemins ===
def ch(fichier):
    """
    indique le chemin absolu du fichier executé
    """
    return os.path.join(sys.path[0], str(fichier))

# resize
def dim(L, H, img):
    """
    Largeur (px), Hauteur (px), image
    redimensionne l'image aux dimensions souhaitées
    """
    H = (Fraction(str(H/img.height()))).limit_denominator(10)
    L = (Fraction(str(L/img.width()))).limit_denominator(10)
    return img.zoom(L.numerator, H.numerator).subsample(L.denominator, H.denominator)


# === lecture paramètres ===
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

parties = ConfigParser()
if os.path.isfile(ch("parties.txt")):
    parties.read(ch("parties.txt"))
else:
    with open(ch('parties.txt'), 'w') as fichier:
        parties.write(fichier)


# === localisation ===
loc = lang[options["DEFAULT"]["langue"]]


# === initialisation fenêtre ===
maitre = tk.Tk()
maitre.title(loc["titre"])
maitre.resizable(0, 0)
# maitre.iconbitmap(ch("*.ico"))
H_E = maitre.winfo_screenheight()
L_E = maitre.winfo_screenwidth()

style = {
    "font" : ('Helvetica', 11),
    "background" : "grey",
    "foreground" : "black",
}
ttkStyle = ttk.Style(maitre)
ttkStyle.configure(
    "TMenubutton",
    **style
)

# === prise en compte plein écran ===
if options["DEFAULT"].getboolean("plein_ecran"):
    maitre.attributes('-fullscreen', True)
    H_F, L_F = H_E, L_E
else:
    maitre.geometry(options["DEFAULT"]["taille"])
    L_F, H_F = [int(i) for i in options["DEFAULT"]["taille"].split("x")]


# === images ===
img = {
    "V--": tk.PhotoImage(file=ch("media/V--.png")),
    "I": dim(L_F, H_F, tk.PhotoImage(file=ch("media/fond.png"))),
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

    efface()

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
                "temps": 0,
                "inv": "",
                "pos": "00;00"
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

    efface()

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
        with open(ch('options.txt'), 'w') as fichier:
            options.write(fichier)
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

    efface()

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
        command=lambda : jeu(B_liste.get(B_liste.curselection()).split("|")[0]),
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

    def quitter():
        with open(ch("parties.txt"), "w") as fichier:
            parties.write(fichier)
        acceuil()

    F_jeu = tk.Frame(maitre)
    F_jeu.place(relheight=1, relwidth=1)

    F_carte = tk.Frame(F_jeu)
    F_carte.place(relheight=1, relwidth=0.8)

    F_barre = tk.Frame(F_jeu)
    F_barre.place(relheight=1, relwidth=0.2, relx=0.8)

    F_barre.rowconfigure(list(range(10)), weight=1)
    F_barre.columnconfigure([0, 1, 2], weight=1)
    
    def charge(n):
        global niv
        global img
        global temp
        nonlocal F_carte
        temp = {}
        for enfant in F_carte.winfo_children():
            enfant.destroy()
        li = int(niv[n]["li"])
        col = int(niv[n]["col"])
        x = int(min([L_F * 0.8 / col, H_F / li]))
        F_carte.rowconfigure(list(range(li+1)), weight=1, minsize=x)
        F_carte.columnconfigure(list(range(col+1)), weight=1, minsize=x)
        for i in range(li):
            for j in range(col):
                s = niv[n]["grille"][i][j]
                if s in temp:
                    image = temp[s]
                else:
                    image = dim(x, x, img[s])
                    temp[s] = image
                    
                gen_img = tk.Label(
                    master=F_carte,
                    image=image,
                    height=x,
                    width=x,
                )
                gen_img.grid(row=i, column=j, sticky="nswe")
        tk.Label(F_carte, bg="pink", text=None, height=int(H_F % li), width=int((L_F * 0.8) % col)).grid(row=li+1,column=col+1)

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
