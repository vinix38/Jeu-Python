# ====== IMPORTS ======
import tkinter as tk
import datetime as dt
import platform as pf
from configparser import ConfigParser
from fractions import Fraction
from tkinter.messagebox import showinfo
from tkinter import ttk
from niveaux import niv
import time
import sys
import os

# fonction de log
def log(*arg):
    print("[LOG", str(dt.datetime.now())[11:23],"]" , *arg)


# === déclaration fenêtre ===
log("=== INITIALISATION ===")
maitre = tk.Tk()
maitre.resizable(0, 0)
H_E = maitre.winfo_screenheight()
L_E = maitre.winfo_screenwidth()
log("taille d'écran =", H_E, "x", L_E)


# === styles ===
style = {
    "font": ('Fixedsys', 24),
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
def dim(L, H, img, nom="?"):
    """
    (Largeur (px), Hauteur (px), image)\n
    redimensionne l'image aux dimensions souhaitées
    """
    H = (Fraction(str(H/img.height()))).limit_denominator(30)
    L = (Fraction(str(L/img.width()))).limit_denominator(30)
    log("image", nom,"=",H,"par",L)
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
    from langue import langue
    global loc
    global options
    global maitre
    loc = langue[options["DEFAULT"]["langue"]]
    maitre.title(loc["titre"])
    log("changement de langue -", loc["lang"])

# === prise en compte plein écran ===
def ecran():
    """
    ()\n
    Redimensionne la taille de l'écran
    """
    global maitre
    global options
    global H_E, L_E
    log("actualisation taille d'écran")
    log("système d'exploitation =", pf.system())
    if options["DEFAULT"].getboolean("plein_ecran"):
        if pf.system() == ("Windows" or "Darwin"):
            maitre.wm_attributes("-fullscreen", True)
        else:
            #maitre.attributes("-zoomed", True)
            maitre.geometry(str(L_E)+"x"+str(H_E)+"+0+0")
        return L_E, H_E
    else:
        if pf.system() == ("Windows" or "Darwin"):
            maitre.wm_attributes("-fullscreen", False)
            #maitre.attributes("-zoomed", False)
        maitre.geometry(options["DEFAULT"]["taille"])
        return tuple(int(i) for i in options["DEFAULT"]["taille"].split("x"))


# ====== VARIABLES ======
temp = {}
img = {
    "V-": tk.PhotoImage(file=ch("media/V--.png")),
    "I": tk.PhotoImage(file=ch("media/fond.png")),
    "MP": tk.PhotoImage(file=ch("media/MPC.png")),
    "MF": tk.PhotoImage(file=ch("media/MPF.png")),
    "Mp": tk.PhotoImage(file=ch("media/MPD.png")),
    "perso": tk.PhotoImage(file=ch("media/icone.png")),
    "SG": tk.PhotoImage(file=ch("media/SG-.png")),
    "CD": tk.PhotoImage(file=ch("media/CD1.png")),
    "FB": tk.PhotoImage(file=ch("media/CD1.png")),
    "OP" : tk.PhotoImage(file=ch("media/OP1.png")),
    "icone" : tk.PhotoImage(file=ch("media/icone.png")),
}
maitre.iconphoto(True, img["icone"])

# === lecture des paramètres ===
options = ConfigParser(allow_no_value=True)
if os.path.isfile(ch("options.txt")) == False:
    options["DEFAULT"] = {
        "plein_ecran": True,
        "taille": "1920x1080",
        "taille_dispo": "1920x1080,1366x768,1440x900,1600x900,1280x800,1280x1024,1024x768",
        "son": True,
        "langue": "fr_FR",
        "langues_dispo": "fr_FR,en_US",
        "haut": "z",
        "gauche": "a",
        "bas": "s",
        "droite": "e",
        "action": "Tab",
    }
    with open(ch('options.txt'), 'w') as fichier:
        options.write(fichier)
else:
    options.read(ch("options.txt"))

# === lecture des parties sauvegardées ===
parties = ConfigParser(allow_no_value=True)
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

    log("=== accueil ===")

    # fenetre
    F_acceuil = tk.Frame(master=maitre)
    F_acceuil.place(relheight=1, relwidth=1)
    F_acceuil.rowconfigure(list(range(15)), weight=1)
    F_acceuil.columnconfigure(list(range(7)), weight=1)

    # fond
    temp["I"] = dim(L_F, H_F, img["I"], "fond")
    fond = tk.Label(F_acceuil, image=temp["I"])
    fond.place(x=0, y=0, relwidth=1, relheight=1)

    # boutons
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
    # placement
    B_quitter.grid(column=3, row=12, sticky="nswe")
    B_options.grid(column=3, row=10, sticky="nswe")
    B_charger.grid(column=3, row=8, sticky="nswe")
    B_creer.grid(column=3, row=6, sticky="nswe")


def creer():
    global parties
    global maitre
    global img

    efface(maitre)

    log("=== nouvelle partie ===")

    # fenetre
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
        if nom in parties.sections() or nom == "":
            showinfo(loc["err"], loc["déjà"])
            log("erreur, cette partie existe déjà")
        else:
            parties[nom] = {
                "niv": "11",
                "score": 0,
                "inv": "",
                "pos": "",
                "vie": 10,
                "S_niv": "11",
                "S_score": 0,
                "S_inv": "",
                "temps": 0,
            }
            log("nouvelle partie -", nom)
            with open(ch("parties.txt"), "w") as fichier:
                parties.write(fichier)
            jeu(nom)

    # boutons
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
    # placement
    E_creer.grid(row=0, column=0, columnspan=2, sticky="nswe")
    B_annuler.grid(row=1, column=0, sticky="nswe")
    B_creer.grid(row=1, column=1, sticky="nswe")


def param():
    global options
    global maitre
    global img

    efface(maitre)

    log("=== paramètres ===")

    # statut écoute du clavier
    cap = False

    # fenetre
    F_param = tk.Frame(master=maitre)
    F_param.place(relheight=1, relwidth=1)
    F_param.rowconfigure(list(range(10)), weight=1)
    F_param.columnconfigure(list(range(10)), weight=1)

    # variables menus déroulants
    opt_l = options["DEFAULT"]["langues_dispo"].split(",")
    clic_l = tk.StringVar()
    opt_r = options["DEFAULT"]["taille_dispo"].split(",")
    clic_r = tk.StringVar()

    # variables cases à cocher
    V_son = tk.StringVar(value=options["DEFAULT"]["son"])

    def sono():
        options["DEFAULT"]["son"] = V_son.get()
    V_plein = tk.StringVar(value=options["DEFAULT"]["plein_ecran"])

    def plein():
        options["DEFAULT"]["plein_ecran"] = V_plein.get()

    # variables touches de clavier
    V_dir = {
        "haut": tk.StringVar(value=options["DEFAULT"]["haut"]),
        "bas": tk.StringVar(value=options["DEFAULT"]["bas"]),
        "gauche": tk.StringVar(value=options["DEFAULT"]["gauche"]),
        "droite": tk.StringVar(value=options["DEFAULT"]["droite"]),
        "action": tk.StringVar(value=options["DEFAULT"]["action"]),
    }

    # fonctions de sortie
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

    # fond
    afond = tk.Label(F_param, image=img["I"])
    afond.place(x=0, y=0, relwidth=1, relheight=1)

    # boutons
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

    # suivi des interactions
    def C_langue(*args):
        options["DEFAULT"]["langue"] = clic_l.get()
    clic_l.trace('w', C_langue)

    def C_taille(*args):
        options["DEFAULT"]["taille"] = clic_r.get()
        V_plein.set("False")
        plein()
    clic_r.trace('w', C_taille)

    # assignement des touches
    def C_touche(touche):
        nonlocal cap
        nonlocal B_quitter_sauv
        if cap == False:
            V_dir[touche].set("")
            B_quitter_sauv["state"] = "disabled"
            cap = touche

    # boutons des touches
    B_haut = tk.Button(
        master=F_param,
        textvariable=V_dir["haut"],
        command=lambda x="haut": C_touche(x),
        **style,
    )
    B_bas = tk.Button(
        master=F_param,
        textvariable=V_dir["bas"],
        command=lambda x="bas": C_touche(x),
        **style,
    )
    B_gauche = tk.Button(
        master=F_param,
        textvariable=V_dir["gauche"],
        command=lambda x="gauche": C_touche(x),
        **style,
    )
    B_droite = tk.Button(
        master=F_param,
        textvariable=V_dir["droite"],
        command=lambda x="droite": C_touche(x),
        **style,
    )
    B_action = tk.Button(
        master=F_param,
        textvariable=V_dir["action"],
        command=lambda x="action": C_touche(x),
        **style,
    )
    T_haut = tk.Label(
        F_param,
        text=loc["haut"],
        **style,
    )
    T_bas = tk.Label(
        F_param,
        text=loc["bas"],
        **style,
    )
    T_gauche = tk.Label(
        F_param,
        text=loc["gauche"],
        **style,
    )
    T_droite = tk.Label(
        F_param,
        text=loc["droite"],
        **style,
    )
    T_action = tk.Label(
        F_param,
        text=loc["action"],
        **style,
    )

    # écoute du clavier
    def capture(e):
        nonlocal cap
        if cap != False:
            e = e.keysym
            V_dir[cap].set(e)
            options["DEFAULT"][cap] = e
            cap = False
            B_quitter_sauv["state"] = "normal"
    maitre.bind("<KeyPress>", capture)

    # placement
    B_taille.grid(row=5, column=4, sticky="nswe")
    B_langue.grid(row=2, column=4, sticky="nswe")
    B_plein.grid(row=4, column=4, sticky="nswe")
    B_quitter_sauv.grid(row=9, column=4, sticky="nswe")
    B_quitter_sans.grid(row=8, column=4, sticky="nswe")
    B_son.grid(row=4, column=2, sticky="nswe")
    B_haut.grid(row=2, column=8, sticky="nswe")
    B_bas.grid(row=3, column=8, sticky="nswe")
    B_gauche.grid(row=4, column=8, sticky="nswe")
    B_droite.grid(row=5, column=8, sticky="nswe")
    B_action.grid(row=6, column=8, sticky="nswe")
    T_haut.grid(row=2, column=7, sticky="nswe")
    T_bas.grid(row=3, column=7, sticky="nswe")
    T_gauche.grid(row=4, column=7, sticky="nswe")
    T_droite.grid(row=5, column=7, sticky="nswe")
    T_action.grid(row=6, column=7, sticky="nswe")


def charger():
    global options
    global maitre
    global img
    global parties

    efface(maitre)

    log("=== charger une partie ===")

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
    log("parties existantes -", sauv)

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
                           " | " + loc["niv"] + " : " + parties[x]["niv"][0] + " | " + parties[x]["temps"])
        B_liste.pack()

    else:
        vide = tk.Label(
            master=F_liste,
            text=loc["-sauv"],
            **style,
        )
        vide.pack(fill="both")
        B_charger.config(state="disabled")
        log("pas de parties disponibles")

    B_importer.grid(row=0, column=0, sticky="nswe")
    B_retour.grid(row=0, column=1, sticky="nswe")
    B_charger.grid(row=0, column=2, sticky="nswe")


def jeu(nom):
    global maitre
    global options
    global parties
    global img

    efface(maitre)

    log("=== chargement du jeu ===")

    # fonction de sortie
    def quitter():
        with open(ch("parties.txt"), "w") as fichier:
            parties.write(fichier)
        acceuil()

    # fenetre
    F_jeu = tk.Frame(maitre, background="black")
    F_jeu.place(relheight=1, relwidth=1)

    F_carte = tk.Frame(F_jeu, background="black")
    F_carte.place(relheight=1, relwidth=0.8)

    F_barre = tk.Frame(F_jeu, background="black")
    F_barre.place(relheight=1, relwidth=0.2, relx=0.8)
    F_barre.rowconfigure(list(range(15)), weight=1,minsize=H_F/10)
    F_barre.columnconfigure([0, 1, 2], weight=1, minsize=L_F/15)

    # \_(°-°)_/
    mvt = x = 0

    F_terrain = tk.Canvas(F_carte, background="black")

    # chargement des niveaux
    def charge(n):
        global niv
        global img
        global temp
        nonlocal x
        nonlocal F_terrain
        nonlocal F_carte
        nonlocal mvt
        mvt = 1
        log("chargement du niveau",n)
        V_niv.set(n[0])
        temp = {}
        efface(F_carte)
        li = int(niv[n]["li"])
        col = int(niv[n]["col"])
        x = int(min((L_F * 0.8) / col, H_F / li))
        log("lignes:", li, "| colonnes:", col, "| coté de case (px):", x)

        F_terrain = tk.Canvas(
            F_carte,
            height=li*x,
            width=col*x,
            background="black",
        )
        F_terrain.place(relx=0.5, rely=0.5, anchor="center")
        #F_terrain.create_image(0, 0, image=img["I"], anchor="nw", tag="fond")
        
        log("image par défaut -", niv[n]["def_img"])
        temp["def_img"] = dim(x, x, img[niv[n]["def_img"]], "def")

        for i in range(li):
            for j in range(col):
                s = niv[n]["grille"][i][j][0:2]
                
                #gestion transparence
                if s[0] not in "SMV":
                    F_terrain.create_image(
                        j*x,
                        i*x,
                        image=temp["def_img"],
                        anchor="nw",
                        tag="case",
                    )
                
                #enregistrement de la case
                if s in temp:
                    image = temp[s]
                else:
                    image = dim(x, x, img[s], s)
                    temp[s] = image
                #affichage de la case
                F_terrain.create_image(
                    j*x,
                    i*x,
                    image=image,
                    anchor="nw",
                    tag="case"
                )

        if parties[nom]["pos"] == "":
            parties[nom]["pos"] = str(
                niv[n]["def_pos"][0]) + ";" + str(niv[n]["def_pos"][1])

        image = dim(x, x, img["perso"])
        temp["perso"] = image
        F_terrain.create_image(
            int(parties[nom]["pos"].split(";")[0]) * x,
            int(parties[nom]["pos"].split(";")[1]) * x,
            image=image,
            tag="perso",
            anchor="nw",
        )
        mvt = 0

    def mouv(mov):
        nonlocal x
        nonlocal mvt
        nonlocal F_terrain
        log("coordonnés de déplacement -", mov)
        coords = [i / x for i in F_terrain.coords("perso")]
        log("coordonnés actuels -", coords)
        cible = [int(coords[i] + mov[i]) for i in range(2)]
        log("coordonnés cibles -", cible)
        if niv[parties[nom]["niv"]]["grille"][cible[1]][cible[0]][0] == "S":
            log("mouvement accepté")
            parties[nom]["pos"] = ";".join([str(i) for i in cible])
            mov = [i*x for i in mov]
            F_terrain.move("perso", *mov)
        else:
            log("mouvement refusé")
        mvt = 0

    def inter():
        pass

    def clavier(e):
        nonlocal mvt
        e = e.keysym
        log("touche pressée -", e)
        if mvt == 0:
            log("mouvement possible")
            mov = [0, 0]
            if e == options["DEFAULT"]["haut"]:
                mov[1] = -1
            elif e == options["DEFAULT"]["bas"]:
                mov[1] = 1
            elif e == options["DEFAULT"]["gauche"]:
                mov[0] = -1
            elif e == options["DEFAULT"]["droite"]:
                mov[0] = 1
            elif e == options["DEFAULT"]["action"]:
                log("essai d'interaction")
                inter()
            if mov != [0, 0]:
                log("tentative de mouvement")
                mvt = 1
                mouv(mov)

    maitre.bind_all("<Key>", clavier)

    B_quitter = tk.Button(
        master=F_barre,
        text=loc["quitter"],
        command=quitter,
        **style,
    )
    T_niveau = tk.Label(
        master=F_barre,
        text=loc["niv"]+" :",
        **style,
    )
    V_niv = tk.StringVar(value="/!\\")
    A_niveau = tk.Label(
        master=F_barre,
        textvariable=V_niv,
        **style,
    )
    A_vie = ttk.Progressbar(
        master=F_barre,
        orient = "horizontal", 
        length = 100,
        mode = 'determinate',
        maximum = 20,
        value=5,
    )
    
    def vie(delta):
        pass
    
    A_vie.grid(row=2, column=0, sticky="nswe", columnspan=3)
    T_niveau.grid(row=5, column=0, sticky="nswe")
    A_niveau.grid(row=5, column=1, sticky="nswe")
    B_quitter.grid(row=9, column=1, sticky="nswe")

    charge(parties[nom]["niv"])


log("début de l'execution")

acceuil()

maitre.mainloop()
