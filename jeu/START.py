# ====== IMPORTS ======
try:
    import tkinter as tk                    #librairie graphique
except ImportError:
    print("sudo apt-get install python-tk") #pour installer tkinter sur les distributions debian
    raise
import datetime as dt                       #infos de temps
import platform as pf                       #detection de l'OS
from boombox import BoomBox                 #gestion du son
from configparser import ConfigParser       #gestion des fichiers persistants
from fractions import Fraction              #calcul des ratios d'images
from tkinter.messagebox import showinfo     #message d'erreur
from tkinter import ttk                     #tkinter en plus beau
from niveaux import niv                     #infos de niveaux
import time                                 #retarder l'execution du programe
import sys                                  #gestion des chemins de fichiers
import os                                   # ^^idem^^

# fonction de log
def log(*arg):
    print("[LOG", str(dt.datetime.now())[11:23],"]" , *arg)


# === déclaration fenêtre ===
log("=== INITIALISATION ===")
maitre = tk.Tk()                            #déclaration de fenetre
maitre.resizable(0, 0)                      #empecher le changement de taille
H_E = maitre.winfo_screenheight()           #hauteur d'écran
L_E = maitre.winfo_screenwidth()            #largeur d'écran
log("taille d'écran =", H_E, "x", L_E)


# === styles ===
style = {   #style par défaut pour tk
    "font": ('Fixedsys', 24),
    "background": "grey",
    "foreground": "black",
}
ttkStyle = ttk.Style(maitre) #styles par défaut pour ttk
ttkStyle.theme_use('clam')
ttkStyle.configure(
    "TMenubutton",
    **style
)
ttkStyle.configure("TProgressbar", foreground="black", background="black", troughcolor="black") #temporaire
ttkStyle.configure("Treeview", highlightthickness=0, bd=0, font=('Fixedsys', 20), rowheight=40) # style des cases
ttkStyle.configure("Treeview.Heading", font=('Fixedsys', 20,'bold')) # style de l'en-tête

# === chemins ===
def ch(fichier):
    """
    (fichier)\n
    indique le chemin absolu du fichier executé
    """
    return os.path.join(sys.path[0], str(fichier))

# === changement de taille ===
def img(L, H, nom):
    """
    (Largeur (px), Hauteur (px), nom de l'image)\n
    redimensionne l'image aux dimensions souhaitées
    """
    global temp
    if nom not in temp:
        img = tk.PhotoImage(file=ch("media/"+nom+".png")) #ressource image
        H = (Fraction(str(H/img.height()))).limit_denominator(30) #ratio de hauteur
        L = (Fraction(str(L/img.width()))).limit_denominator(30)  #ratio de largeur
        log("image", nom,"=",H,"par",L)
        img = img.zoom(L.numerator, H.numerator).subsample(L.denominator, H.denominator)
        temp[nom] = img
    return temp[nom]

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
    from langue import langue #fichier de localisation
    global loc
    global options
    global maitre
    loc = langue[options["DEFAULT"]["langue"]] #changement de la localisation par défaut
    temp["BG"] = img(L_F, H_F, "BG_"+options["DEFAULT"]["langue"][0:2]) #changement du fond d'écran
    maitre.title(loc["titre"]) #changement du titre
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
            maitre.iconify()
            maitre.deiconify()
            maitre.geometry(str(L_E)+"x"+str(H_E)+"+0+0")
        return L_E, H_E
    else:
        if pf.system() == ("Windows" or "Darwin"):
            maitre.wm_attributes("-fullscreen", False)
        else:
            maitre.iconify()
            maitre.deiconify()
        maitre.geometry(options["DEFAULT"]["taille"])
        return tuple(int(i) for i in options["DEFAULT"]["taille"].split("x"))


# ====== VARIABLES ======
temp = {}       #empêche que les images soient effacées par le garbage collector
maitre.iconphoto(True, img(200, 200, "icone")) #icone de fenetre

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

def son(nom):
    if options["DEFAULT"].getboolean("son"):
        BoomBox(ch("media/"+nom+".wav"), False).play()

L_F, H_F = ecran()
localisation()

# ***====== FENETRES ======***
def acceuil():
    global maitre
    global options
    global temp

    efface(maitre)

    log("=== accueil ===")

    # fenetre
    F_acceuil = tk.Frame(master=maitre)
    F_acceuil.place(relheight=1, relwidth=1)
    F_acceuil.rowconfigure(list(range(15)), weight=1)
    F_acceuil.columnconfigure(list(range(7)), weight=1)

    # fond
    temp={}
    fond = tk.Label(F_acceuil, image=img(L_F, H_F, "BG_"+options["DEFAULT"]["langue"][0:2]))
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
                "vie": 5,
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
        L_F, H_F = ecran()
        localisation()
        acceuil()

    # fond
    afond = tk.Label(F_param, image=temp["BG_"+options["DEFAULT"]["langue"][0:2]])
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
        command=lambda: C_touche("haut"),
        **style,
    )
    B_bas = tk.Button(
        master=F_param,
        textvariable=V_dir["bas"],
        command=lambda: C_touche("bas"),
        **style,
    )
    B_gauche = tk.Button(
        master=F_param,
        textvariable=V_dir["gauche"],
        command=lambda: C_touche("gauche"),
        **style,
    )
    B_droite = tk.Button(
        master=F_param,
        textvariable=V_dir["droite"],
        command=lambda: C_touche("droite"),
        **style,
    )
    B_action = tk.Button(
        master=F_param,
        textvariable=V_dir["action"],
        command=lambda: C_touche("action"),
        **style,
    )
    #texte associé aux bouton
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
    def charge(B_liste):
        sel = B_liste.focus()
        log(sel)
        if sel:
            jeu(B_liste.item(sel)["values"][0])
            
    B_charger = tk.Button(
        master=F_barre,
        text=loc["charger"],
        command=lambda: charge(B_liste),
        **style,
    )
    def supprimer(B_liste):
        sel = B_liste.focus()
        if sel:
            parties.remove_section(B_liste.item(sel)["values"][0])
            with open(ch('parties.txt'), 'w') as fichier:
                parties.write(fichier)
            charger()

    B_supprimer = tk.Button(
        master=F_barre,
        text=loc["suppr"],
        command=lambda: supprimer(B_liste),
        **style,
    )

    parties.read(ch("parties.txt"))
    sauv = parties.sections()
    log("parties existantes -", sauv)

    if sauv != []:
        roue = tk.Scrollbar(F_liste)
        roue.pack(side="right", fill="y")

        colonnes = (loc["nom"], loc["niv"], loc["XP"], loc["temps"])
        B_liste = ttk.Treeview(
            master=F_liste,
            show="headings",
            column=colonnes,
            height=len(sauv),
            selectmode="browse",
            yscrollcommand=roue.set,

        )
        for c in colonnes:
            B_liste.column(c, anchor="center")
            B_liste.heading(c, text=c.title(), anchor="center")            
            
        for x in sauv:
            B_liste.insert(
                parent='',
                index='end',
                values=(x, parties[x]["niv"][0], parties[x]["score"], parties[x]["temps"])
            )
        B_liste.pack(fill="both")

    else:
        vide = tk.Label(
            master=F_liste,
            text=loc["-sauv"],
            **style,
        )
        vide.pack(fill="both")
        B_charger.config(state="disabled")
        log("pas de parties disponibles")

    B_supprimer.grid(row=0, column=0, sticky="nswe")
    B_retour.grid(row=0, column=1, sticky="nswe")
    B_charger.grid(row=0, column=2, sticky="nswe")


def jeu(nom):
    global maitre
    global options
    global parties

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
    F_barre.rowconfigure(list(range(15)), weight=1,minsize=H_F/15)
    F_barre.columnconfigure([0, 1, 2, 3], weight=1, minsize=L_F/20)

    # \_(°-°)_/
    mvt = x = 0

    F_terrain = tk.Canvas(F_carte, background="black")

    # chargement des niveaux
    def charge(n):
        """
        (n)\n
        charge le niveau (n) spécifié
        """
        global niv
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
            #highlightthickness=0,
        )
        F_terrain.place(relx=0.5, rely=0.5, anchor="center")
        
        log("image par défaut -", niv[n]["def_img"])
        temp["def_img"] = img(x, x, niv[n]["def_img"]) #image par défaut en cas de transparence

        for i in range(li):
            for j in range(col):
                s = niv[n]["grille"][i][j][0:2] #récupération du nom de la texture
                
                if s[0] != "V": #pas d'image à afficher si la case est vide
                    #gestion transparence
                    if s[0] not in "SMV":
                        F_terrain.create_image(
                            j*x,
                            i*x,
                            image=temp["def_img"],
                            anchor="nw",
                            tag="case",
                        )       
                    
                    #affichage de la case
                    F_terrain.create_image(
                        j*x,
                        i*x,
                        image=img(x, x, s),
                        anchor="nw",
                        tag="case"
                    )
        # ---=== fin charge() ===---

        if parties[nom]["pos"] == "": #si il n'y a pas encore de position enregistrée
            parties[nom]["pos"] = str(
                niv[n]["def_pos"][0]) + ";" + str(niv[n]["def_pos"][1])
         
        F_terrain.create_image(
            int(parties[nom]["pos"].split(";")[0]) * x,
            int(parties[nom]["pos"].split(";")[1]) * x,
            image=img(x, x, "perso"),
            tag="perso",
            anchor="nw",
        )
        mvt = 0

    def mouv(mov, coords):
        """
        déplace le personnage si possible
        """
        nonlocal x
        nonlocal mvt
        nonlocal F_terrain
        
        cible = [int(coords[i] + mov[i]) for i in range(2)]
        log("coordonnés cibles -", cible)
        if niv[parties[nom]["niv"]]["grille"][cible[1]][cible[0]][0] == "S":
            log("mouvement accepté")
            son("pas")
            parties[nom]["pos"] = ";".join([str(i) for i in cible])
            mov = [i*x for i in mov]
            F_terrain.move("perso", *mov)
        else:
            log("mouvement refusé")
        mvt = 0

    def action(case):
        global parties
        log("interaction avec", case)
        nonlocal mvt
        ca = case[0:2]
        if ca == "FB":
            showinfo("", loc[parties[nom]["niv"][0] + "_fantome" + case[2]])
        elif ca == "OP":
            pass
        elif ca == "EP":
            charge(case[2])
            
        mvt = 0
        

    def inter(coords):
        """
        cherche si il y a un objet avec lequel interagir
        """
        tr = False
        for i in range(-1,2):
            for j in range(-1,2):
                if niv[parties[nom]["niv"]]["grille"][coords[1]+i][coords[0]+j][0] not in "MSV":
                    log("objet trouvé")
                    tr = True
                    break
            if tr:
                break
        if tr:
            action(niv[parties[nom]["niv"]]["grille"][coords[1]+i][coords[0]+j])
        else:
            nonlocal mvt
            mvt = 0

    def clavier(e):
        """
        intercepte toutes les touches tapées et décide l'action appropriée
        """
        nonlocal mvt
        e = e.keysym
        log("touche pressée -", e)
        if mvt == 0:
            coords = [int(i / x) for i in F_terrain.coords("perso")]
            log("coords", coords)
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
                log("tentative d'interaction")
                mvt = 1
                inter(coords)
            if mov != [0, 0]:
                log("tentative de mouvement")
                mvt = 1
                mouv(mov, coords)

    maitre.bind_all("<Key>", clavier)

    #=== barre latérale ===
    B_quitter = tk.Button(
        master=F_barre,
        text=loc["quitter"],
        command=quitter,
        **style,
    )
    T_niveau = tk.Label(
        master=F_barre,
        text=loc["niv"],
        **style,
    )
    V_niv = tk.StringVar(value="/!\\")
    A_niveau = tk.Label(
        master=F_barre,
        textvariable=V_niv,
        **style,
    )
    T_xp = tk.Label(
        master=F_barre,
        text=loc["XP"],
        **style,
    )
    V_xp = tk.IntVar(value=parties[nom].getint("score"))
    A_xp = tk.Label(
        master=F_barre,
        textvariable=V_xp,
        **style,
    )
    A_vie = ttk.Progressbar(
        master=F_barre,
        orient = "horizontal", 
        mode = 'determinate',
        maximum = 20,
        value=parties[nom].getint("vie"),
    )
    
    def retour():
        """
        retour au dernier checkpoint
        """
        nonlocal mvt
        global parties
        parties[nom]["inv"] = parties[nom]["S_inv"]
        parties[nom]["niv"] = parties[nom]["S_niv"]
        parties[nom]["score"] = parties[nom]["S_score"]
        parties[nom]["pos"] = ""
        parties[nom]["vie"] = 5
        charge(parties[nom]["niv"])
        
    def vie(delta):
        """
        effectue les changements de niveau de vie
        """
        global parties
        valeur = A_vie["value"]
        valeur += delta
        if valeur <= 0:
            retour()
        else:
            A_vie["value"] = valeur
            parties[nom]["vie"] = str(valeur)
            if valeur < 5:
                couleur = "red"
            elif 5 <= valeur < 10:
                couleur = "orange"
            elif 10 <= valeur < 15:
                couleur = "green"
            else:
                 couleur = "blue"
            ttkStyle.configure("TProgressbar", foreground=couleur, background=couleur)
            
    def xp(delta):
        """
        effectue les changements de score
        """
        global parties
        valeur = V_xp.get()
        valeur += delta
        V_xp.set(valeur)
        parties[nom]["score"] = str(valeur)
    
    
    #placement
    A_vie.grid(row=2, column=0, sticky="nswe", columnspan=4)
    T_niveau.grid(row=8, column=0, sticky="nswe", columnspan=2)
    A_niveau.grid(row=8, column=2, sticky="nswe", columnspan=2)
    T_xp.grid(row=6, column=0, sticky="nswe", columnspan=2)
    A_xp.grid(row=6, column=2, sticky="nswe", columnspan=2)
    B_quitter.grid(row=14, column=1, sticky="nswe", columnspan=2)

    vie(0)
    xp(0)
    charge(parties[nom]["niv"])


log("début de l'execution")

acceuil()

maitre.mainloop() #fin du script !
