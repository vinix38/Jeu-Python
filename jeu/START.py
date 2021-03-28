# ====== IMPORTS ======
try:
    from tkinter import Tk                  #librairie graphique
except ImportError:
    print("sudo apt install python-tk")     #pour installer tkinter sur les distributions debian
    raise
from datetime import datetime               #infos de temps
from platform import system                 #detection de l'OS
from boombox import BoomBox                 #gestion du son
from configparser import ConfigParser       #gestion des fichiers persistants
from fractions import Fraction              #calcul des ratios d'images
from tkinter import Label, Frame, Toplevel, Button, StringVar, IntVar, Canvas, PhotoImage, Entry, Checkbutton, Scrollbar
from tkinter.messagebox import showinfo     #message d'erreur
from tkinter.ttk import Style, Treeview, OptionMenu, Progressbar
from niveaux import niv                     #infos de niveaux
import sys                                  #gestion des chemins de fichiers
import os                                   # ^^idem^^pytho

# fonction de log
def log(*arg):
    """
    enregistre les infos données
    """
    print("[LOG", str(datetime.now())[11:23]+"]" , *arg)

# === chemins ===
def ch(fichier):
    """
    (fichier)\n
    indique le chemin absolu du fichier executé
    """
    return os.path.join(sys.path[0], str(fichier))

# === tout effacer ===
def efface(parent):
    """
    (parent)\n
    Efface tous les widgets présents dans le parent indiqué
    """
    for enfant in parent.winfo_children():
        enfant.destroy()

class maitre(Tk): #objet de notre fenetre
    """
    classe de fenetre
    """
    # ====== VARIABLES ======
    temp = {} #empêche que les images soient effacées par le garbage collector
    temp8 = {} #niveau de résilience plus haut
    
    def __init__(self):
        """
        initialisation
        """
        super().__init__() #fenetre tkinter de base
        # === déclaration fenêtre ===
        log("=== INITIALISATION ===")
        self.resizable(0, 0)                      #empecher le changement de taille
        self.H_E = self.winfo_screenheight()           #hauteur d'écran
        self.L_E = self.winfo_screenwidth()            #largeur d'écran
        log("taille d'écran =", self.H_E, "x", self.L_E)

        # === styles ===
        self.style = {   #style par défaut pour tk
            "font": ('Fixedsys', 24),
            "background": "black",
            "foreground": "white",
        }
        self.ttkStyle = Style(self) #styles par défaut pour ttk
        self.ttkStyle.theme_use('clam')
        self.ttkStyle.configure(
            "TMenubutton",
            **self.style
        )
        self.ttkStyle.configure("TProgressbar",
                            foreground="black",
                            background="black",
                            troughcolor="black"
                        ) #temporaire
        self.ttkStyle.configure("Treeview.Heading",
                            font=('Fixedsys', 20,'bold'),
                            foreground="white",
                            background="black",
                            fieldbackground="black",
                        ) # style de l'en-tête
        self.ttkStyle.configure("Treeview",
                            background="pink",
                            foreground="green",
                            fieldbackground="black",
                            rowheight=40,
                            highlightthickness=0,
                            bd=0,
                            font=('Fixedsys', 20),
                        ) # style des cases
        
        self.iconphoto(True, self.img(200, 200, "icone")) #icone de fenetre
        self.res = None
        self.att = 0
        self.x = -1
        self.n = -1
        
        # === lecture des paramètres ===
        self.options = ConfigParser(allow_no_value=True) 
        if os.path.isfile(ch("options.txt")) == False:
            self.options["DEFAULT"] = {
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
                self.options.write(fichier)
        else:
            self.options.read(ch("options.txt"))

        # === lecture des parties sauvegardées ===
        self.parties = ConfigParser(allow_no_value=True)
        if os.path.isfile(ch("parties.txt")):
            self.parties.read(ch("parties.txt"))
        else:
            with open(ch('parties.txt'), 'w') as fichier:
                self.parties.write(fichier)
                
        self.L_F, self.H_F = self.ecran()
        self.localisation()

    # === changement de taille ===
    def img(self, L, H, nom, important=0):
        """
        (Largeur (px), Hauteur (px), nom de l'image, importance)\n
        redimensionne l'image aux dimensions souhaitées
        """
        if nom not in self.temp:
            img = PhotoImage(file=ch("media/"+nom+".png")) #ressource image
            H = (Fraction(str(H/img.height()))).limit_denominator(30) #ratio de hauteur
            L = (Fraction(str(L/img.width()))).limit_denominator(30)  #ratio de largeur
            log("image", nom,"=",H,"par",L)
            img = img.zoom(L.numerator, H.numerator).subsample(L.denominator, H.denominator)
            if important:
                self.temp8[nom] = img
            self.temp[nom] = img
        return self.temp[nom]

    # ====== changer langue ======
    def localisation(self):
        """
        ()\n
        Change la langue
        """
        from langue import langue #fichier de localisation
        self.loc = langue[self.options["DEFAULT"]["langue"]] #changement de la localisation par défaut
        self.temp["BG"] = self.img(self.L_F, self.H_F, "BG_"+self.options["DEFAULT"]["langue"][0:2]) #changement du fond d'écran
        self.title(self.loc["titre"]) #changement du titre
        log("changement de langue -", self.loc["lang"])

    # === prise en compte plein écran ===
    def ecran(self):
        """
        ()\n
        Redimensionne la taille de l'écran
        """
        log("actualisation taille d'écran")
        log("système d'exploitation =", system())
        if self.options["DEFAULT"].getboolean("plein_ecran"):
            if system() == ("Windows" or "Darwin"):
                self.wm_attributes("-fullscreen", True)
            else:
                self.iconify()
                self.deiconify()
                self.geometry(str(self.L_E)+"x"+str(self.H_E)+"+0+0")
            return self.L_E, self.H_E
        else:
            if system() == ("Windows" or "Darwin"):
                self.wm_attributes("-fullscreen", False)
            else:
                self.iconify()
                self.deiconify()
            self.geometry(self.options["DEFAULT"]["taille"])
            return tuple(int(i) for i in self.options["DEFAULT"]["taille"].split("x"))

    def son(self, nom):
        """
        joue le son demandé
        """
        if self.options["DEFAULT"].getboolean("son"):
            BoomBox(ch("media/"+nom+".wav"), False).play()

    # ***====== FENETRES ======***
    def acceuil(self):
        """
        fenetre d'acceuil du jeu
        """
        efface(self)
        self.unbind_all("<Key>")

        log("=== accueil ===")

        # fenetre
        F_acceuil = Frame(master=self)
        F_acceuil.place(relheight=1, relwidth=1)
        F_acceuil.rowconfigure([i for i in range(15)], weight=1)
        F_acceuil.columnconfigure([i for i in range(7)], weight=1)

        # fond
        self.temp={}
        fond = Label(F_acceuil, image=self.img(self.L_F, self.H_F, "BG_"+self.options["DEFAULT"]["langue"][0:2]))
        fond.place(x=0, y=0, relwidth=1, relheight=1)

        # boutons
        B_quitter = Button(
            text=self.loc["quitter"],
            master=F_acceuil,
            command=self.destroy,
            **self.style,
        )
        B_options = Button(
            text=self.loc["options"],
            master=F_acceuil,
            command=self.param,
            **self.style,
        )
        B_charger = Button(
            text=self.loc[">partie"],
            master=F_acceuil,
            command=self.charger,
            **self.style,
        )
        B_creer = Button(
            text=self.loc["+partie"],
            master=F_acceuil,
            command=self.creer,
            **self.style,
        )
        # placement
        B_quitter.grid(column=3, row=12, sticky="nswe")
        B_options.grid(column=3, row=10, sticky="nswe")
        B_charger.grid(column=3, row=8, sticky="nswe")
        B_creer.grid(column=3, row=6, sticky="nswe")

    def creer(self):
        """
        création d'une nouvelle partie
        """
        efface(self)

        log("=== nouvelle partie ===")

        # fenetre
        F_creer = Frame(self)
        F_creer.place(relheight=1, relwidth=1)
        F_creer.rowconfigure([i for i in range(15)], minsize=self.H_F/15)
        F_creer.columnconfigure([i for i in range(15)], minsize=self.L_F/15)

        E_creer = Entry(
            master=F_creer,
            **self.style,
        )

        def creation(nom):
            """
            crée une nouvelle partie si possible
            """
            if nom in self.parties.sections():
                showinfo(self.loc["err"], self.loc["déjà"])
                log("erreur, cette partie existe déjà")
            elif nom == "":
                showinfo(self.loc["err"], self.loc["vide"] )
            else:
                self.parties[nom] = {
                    "niv": "1",
                    "score": 0,
                    "inv": "",
                    "pos": "",
                    "vie": 5,
                    "S_niv": "1",
                    "S_score": 0,
                    "S_inv": "",
                    "temps": 0,
                }
                log("nouvelle partie -", nom)
                with open(ch("parties.txt"), "w") as fichier:
                    self.parties.write(fichier)
                self.jeu(nom)

        # boutons
        B_creer = Button(
            master=F_creer,
            text=self.loc["creer"],
            command=lambda: creation(E_creer.get()),
            **self.style,
        )
        B_annuler = Button(
            master=F_creer,
            text=self.loc["annuler"],
            command=self.acceuil,
            **self.style,
        )
        # placement
        E_creer.grid(row=7, column=6, columnspan=2, sticky="nswe")
        B_annuler.grid(row=9, column=7, sticky="nswe")
        B_creer.grid(row=9, column=6, sticky="nswe")

    def param(self):
        """
        fentre des paramètres du jeu
        """
        efface(self)

        log("=== paramètres ===")

        # fenetre
        F_param = Frame(master=self)
        F_param.place(relheight=1, relwidth=1)
        F_param.rowconfigure([i for i in range(10)], weight=1)
        F_param.columnconfigure([i for i in range(10)], weight=1)

        # variables menus déroulants
        opt_l = self.options["DEFAULT"]["langues_dispo"].split(",")
        clic_l = StringVar()
        opt_r = self.options["DEFAULT"]["taille_dispo"].split(",")
        clic_r = StringVar()

        # variables cases à cocher
        V_son = StringVar(value=self.options["DEFAULT"]["son"])

        def sono():
            self.options["DEFAULT"]["son"] = V_son.get()
        V_plein = StringVar(value=self.options["DEFAULT"]["plein_ecran"])

        def plein():
            self.options["DEFAULT"]["plein_ecran"] = V_plein.get()

        # variables touches de clavier
        V_dir = {
            "haut": StringVar(value=self.options["DEFAULT"]["haut"]),
            "bas": StringVar(value=self.options["DEFAULT"]["bas"]),
            "gauche": StringVar(value=self.options["DEFAULT"]["gauche"]),
            "droite": StringVar(value=self.options["DEFAULT"]["droite"]),
            "action": StringVar(value=self.options["DEFAULT"]["action"]),
        }

        # fonctions de sortie
        def quitter_sans():
            """
            quitter sans sauvegarder
            """
            self.options.read(ch("options.txt"))
            self.acceuil()

        def quitter_avec():
            """
            quitter en sauvegardant
            """
            with open(ch('options.txt'), 'w') as fichier:
                self.options.write(fichier)
            self.L_F, self.H_F = self.ecran()
            self.localisation()
            self.acceuil()

        # fond
        fond = Label(F_param, image=self.temp["BG_"+self.options["DEFAULT"]["langue"][0:2]])
        fond.place(x=0, y=0, relwidth=1, relheight=1)

        # boutons
        B_langue = OptionMenu(
            F_param,
            clic_l,
            self.options["DEFAULT"]["langue"],
            *opt_l,
        )
        B_taille = OptionMenu(
            F_param,
            clic_r,
            self.options["DEFAULT"]["taille"],
            *opt_r,
        )
        B_son = Checkbutton(
            master=F_param,
            text=self.loc["son"],
            command=sono,
            onvalue="True",
            offvalue="False",
            variable=V_son,
            **self.style,
        )
        B_plein = Checkbutton(
            master=F_param,
            text=self.loc["plein"],
            command=plein,
            onvalue="True",
            offvalue="False",
            variable=V_plein,
            **self.style,
        )
        B_quitter_sauv = Button(
            master=F_param,
            text=self.loc["q+sauv"],
            command=quitter_avec,
            **self.style,
        )
        B_quitter_sans = Button(
            master=F_param,
            text=self.loc["q-sauv"],
            command=quitter_sans,
            **self.style,
        )

        # suivi des interactions
        def C_langue(*args):
            self.options["DEFAULT"]["langue"] = clic_l.get()
        clic_l.trace('w', C_langue)

        def C_taille(*args):
            self.options["DEFAULT"]["taille"] = clic_r.get()
            V_plein.set("False")
            plein()
        clic_r.trace('w', C_taille)

        # assignement des touches
        def C_touche(touche):
            nonlocal B_quitter_sauv
            if self.att == 0:
                V_dir[touche].set("")
                B_quitter_sauv["state"] = "disabled"
                self.att = touche

        # boutons des touches
        B_haut = Button(
            master=F_param,
            textvariable=V_dir["haut"],
            command=lambda: C_touche("haut"),
            **self.style,
        )
        B_bas = Button(
            master=F_param,
            textvariable=V_dir["bas"],
            command=lambda: C_touche("bas"),
            **self.style,
        )
        B_gauche = Button(
            master=F_param,
            textvariable=V_dir["gauche"],
            command=lambda: C_touche("gauche"),
            **self.style,
        )
        B_droite = Button(
            master=F_param,
            textvariable=V_dir["droite"],
            command=lambda: C_touche("droite"),
            **self.style,
        )
        B_action = Button(
            master=F_param,
            textvariable=V_dir["action"],
            command=lambda: C_touche("action"),
            **self.style,
        )
        #texte associé aux bouton
        T_haut = Label(
            F_param,
            text=self.loc["haut"],
            **self.style,
        )
        T_bas = Label(
            F_param,
            text=self.loc["bas"],
            **self.style,
        )
        T_gauche = Label(
            F_param,
            text=self.loc["gauche"],
            **self.style,
        )
        T_droite = Label(
            F_param,
            text=self.loc["droite"],
            **self.style,
        )
        T_action = Label(
            F_param,
            text=self.loc["action"],
            **self.style,
        )

        # écoute du clavier
        def capture(e):
            if self.att != 0:
                e = e.keysym
                V_dir[self.att].set(e)
                self.options["DEFAULT"][self.att] = e
                self.att = 0
                B_quitter_sauv["state"] = "normal"
        self.bind("<Key>", capture)

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

    def charger(self):
        """
        fentre de chargement des parties
        """
        efface(self)

        log("=== charger une partie ===")

        F_charge = Frame(self, bg="black")
        F_charge.place(relheight=1, relwidth=1)

        F_liste = Frame(F_charge, bg="black")
        F_liste.place(relheight=0.9, relwidth=1)

        F_barre = Frame(F_charge, bg="black")
        F_barre.place(relheight=0.1, relwidth=1, rely=0.9)
        F_barre.rowconfigure(0, weight=1)
        F_barre.columnconfigure([0, 1, 2], weight=1)

        B_retour = Button(
            master=F_barre,
            text=self.loc["retour"],
            command=self.acceuil,
            **self.style,
        )
        def charge(B_liste):
            """
            lancement du chargement de la partie sélectionnée
            """
            sel = B_liste.focus()
            log(sel)
            if sel:
                self.jeu(B_liste.item(sel)["values"][0])
                
        B_charger = Button(
            master=F_barre,
            text=self.loc["charger"],
            command=lambda: charge(B_liste),
            **self.style,
        )
        def supprimer(B_liste):
            """
            suppression de la partie sélectionnée
            """
            sel = B_liste.focus()
            if sel:
                self.parties.remove_section(B_liste.item(sel)["values"][0])
                with open(ch('parties.txt'), 'w') as fichier:
                    self.parties.write(fichier)
                self.charger()

        B_supprimer = Button(
            master=F_barre,
            text=self.loc["suppr"],
            command=lambda: supprimer(B_liste),
            **self.style,
        )

        self.parties.read(ch("parties.txt"))
        sauv = self.parties.sections()
        log("parties existantes -", sauv)

        if sauv != []:
            roue = Scrollbar(F_liste)
            roue.pack(side="right", fill="y")

            colonnes = (self.loc["nom"], self.loc["niv"], self.loc["XP"], self.loc["temps"])
            B_liste = Treeview(
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
                
            for i in sauv:
                B_liste.insert(
                    parent='',
                    index='end',
                    values=(
                        i,
                        self.parties[i]["niv"][0],
                        self.parties[i]["score"],
                        self.parties[i]["temps"]
                    ),
                    tags=("all",)
                )
            B_liste.tag_configure("all", background="black", foreground="white")
            B_liste.pack(fill="both")

        else:
            vide = Label(
                master=F_liste,
                text=self.loc["-sauv"],
                **self.style,
            )
            vide.pack(fill="both")
            B_charger.config(state="disabled")
            log("pas de parties disponibles")

        B_supprimer.grid(row=0, column=0, sticky="nswe")
        B_retour.grid(row=0, column=1, sticky="nswe")
        B_charger.grid(row=0, column=2, sticky="nswe")
        self.att = 0

    def jeu(self, nom):
        """
        fenetre principale de jeu
        """
        efface(self)

        log("=== chargement du jeu ===")

        # fonction de sortie
        def quitter():
            """
            quitter la partie en sauvegardant
            """
            with open(ch("parties.txt"), "w") as fichier:
                self.parties.write(fichier)
            self.acceuil()

        # fenetre
        F_jeu = Frame(self, background="black")
        F_jeu.place(relheight=1, relwidth=1)

        F_carte = Frame(F_jeu, background="black")
        F_carte.place(relheight=1, relwidth=0.8)

        F_barre = Frame(F_jeu, background="black")
        F_barre.place(relheight=1, relwidth=0.2, relx=0.8)
        F_barre.rowconfigure([i for i in range(15)], minsize=self.H_F/15)
        F_barre.columnconfigure([0, 1, 2, 3], minsize=self.L_F/20)

        F_terrain = Canvas(F_carte, background="black")

        # chargement des niveaux
        def charge(n=self.n):
            """
            (n)\n
            charge le niveau (n) spécifié
            """
            nonlocal F_terrain
            nonlocal F_carte
            self.att = 1
            self.n = n
            log("chargement du niveau",n)
            V_niv.set(n)
            self.parties[nom]["niv"] = n
            self.temp = {}
            efface(F_carte)
            li = int(niv[n]["li"])
            col = int(niv[n]["col"])
            self.x = x = int(min((self.L_F * 0.8) / col, self.H_F / li))
            log("lignes:", li, "| colonnes:", col, "| coté de case (px):", x)

            F_terrain = Canvas(
                F_carte,
                height=li*x,
                width=col*x,
                background="black",
                #highlightthickness=0,
            )
            F_terrain.place(relx=0.5, rely=0.5, anchor="center")
            log("image par défaut -", niv[n]["def_img"])
            self.temp["def_img"] = self.img(x, x, niv[n]["def_img"]) #image par défaut en cas de transparence

            for i in range(li):
                for j in range(col):
                    s = niv[n]["grille"][i][j][0:2] #récupération du nom de la texture
                    
                    if s[0] != "V": #pas d'image à afficher si la case est vide
                        #gestion transparence
                        if s[0] not in "SMV":
                            F_terrain.create_image(
                                j*x,
                                i*x,
                                image=self.temp["def_img"],
                                anchor="nw",
                                tag="case",
                            )       
                        
                        #affichage de la case
                        F_terrain.create_image(
                            j*x,
                            i*x,
                            image=self.img(x, x, s),
                            anchor="nw",
                            tag="case"
                        )
            # ---=== fin charge() ===---

            if self.parties[nom]["pos"] == "": #si il n'y a pas encore de position enregistrée
                self.parties[nom]["pos"] = str(niv[n]["def_pos"][0]) \
                    + ";" + str(niv[n]["def_pos"][1])
            
            F_terrain.create_image(
                int(self.parties[nom]["pos"].split(";")[0]) * x,
                int(self.parties[nom]["pos"].split(";")[1]) * x,
                image=self.img(x, x, "perso01"),
                tag="perso",
                anchor="nw",
            )
            self.att = 0

        #=== barre latérale ===
        B_quitter = Button(
            master=F_barre,
            text=self.loc["quitter"],
            command=quitter,
            **self.style,
        )
        T_niveau = Label(
            master=F_barre,
            text=self.loc["niv"],
            **self.style,
        )
        V_niv = StringVar(value="/!\\")
        A_niveau = Label(
            master=F_barre,
            textvariable=V_niv,
            **self.style,
        )
        T_xp = Label(
            master=F_barre,
            text=self.loc["XP"],
            **self.style,
        )
        V_xp = IntVar(value=self.parties[nom].getint("score"))
        A_xp = Label(
            master=F_barre,
            textvariable=V_xp,
            **self.style,
        )
        A_vie = Progressbar(
            master=F_barre,
            orient = "horizontal", 
            mode = 'determinate',
            maximum = 20,
            value=self.parties[nom].getint("vie"),
        )
        T_vie = Label(
            master=F_barre,
            bg="black",
            image=self.img(self.H_F/15,self.H_F/15, "coeur", 1),
            anchor="n",
        )
        A_inv = Treeview(
            master = F_barre,
            show="headings",
            columns=["inv"],
            selectmode="none",
            #yscrollcommand=roue.set,
            height = len(self.parties[nom]["inv"].split(",")),
        )
        A_inv.column("inv", anchor="center")
        A_inv.heading("inv", text=self.loc["inv"], anchor="center")  
        
        if self.parties[nom]["inv"] != "":
            for i in self.parties[nom]["inv"].split(","):
                A_inv.insert(
                    parent="",
                    index="end",
                    values=(self.loc[i],),
                    )
        
        def sauvegarde():
            self.parties[nom]["S_inv"] = self.parties[nom]["inv"]
            self.parties[nom]["S_niv"] = self.parties[nom]["niv"]
            self.parties[nom]["S_score"] = self.parties[nom]["score"]
        
        def mouv(mov, coords):
            """
            déplace le personnage si possible
            """
            nonlocal F_terrain
            cible = [int(coords[i] + mov[i]) for i in range(2)]
            log("coordonnés cibles -", cible)
            s = niv[self.parties[nom]["niv"]]["grille"][cible[1]][cible[0]]
            log(s)
            if s[0] == "S":
                self.son("pas")
                s = True
            elif (s[0] == "P") and ((self.n + "_D" + s[2]) in self.parties[nom]["inv"].split(",")):
                self.son("porte")
                if s[2] == "+":
                    self.parties[nom]["pos"] = ""
                    charge(str(int(self.n) + 1))
                elif s[2] == "-":
                    self.parties[nom]["pos"] = ""
                    charge(str(int(self.n) + 1))
                else:
                    s = True
            if s == True:
                log("mouvement accepté")
                self.parties[nom]["pos"] = ";".join([str(i) for i in cible])
                F_terrain.delete("perso")
                F_terrain.create_image(
                    *[i*self.x for i in cible],
                    anchor="nw", tag="perso",
                    image=self.img(
                        self.x,
                        self.x,
                        "perso"+"".join([str(i) for i in mov])
                    )
                )
                def apres():
                    self.att = 0
                F_terrain.after(100, apres)
            else:
                log("mouvement refusé")
                self.att = 0

        def action(case):
            """
            interagis avec l'objet si possible
            """
            log("interaction avec", case)
            ca = case[0:2]
            if ca == "FB":
                dialogue().animation(self.n + "_" + case)
            elif ca == "OP":
                f = dialogue()
                f.question(self.n + "_" + case)
                def actu(*args):
                    f.unbind("<Destroy>")
                    log(self.res)
                    res = self.res
                    xp(res[1])
                    inv(res[2])
                    vie(res[0])
                    if res[0] >= 0:
                        sauvegarde()
                f.bind("<Destroy>", actu)
                log(self.res)
            elif ca == "EP":
                self.son("escalier")
                charge(case[2])
            elif ca == "CD":
                inv(self.n + "_" + case[1:])
                self.son("coffre")
                dialogue().animation(str(self.n)+ "_" + case[1:], "coffre_10fps.gif", 5)
            else:
                self.att = 0
            
        def inter(coords):
            """
            cherche si il y a un objet avec lequel interagir
            """
            tr = False
            for i in range(-1,2):
                for j in range(-1,2):
                    if niv[self.parties[nom]["niv"]]["grille"][coords[1]+i][coords[0]+j][0] not in "MSV":
                        log("objet trouvé")
                        tr = True
                        break
                if tr:
                    break
            if tr:
                action(niv[self.parties[nom]["niv"]]["grille"][coords[1]+i][coords[0]+j])
            else:
                self.att = 0

        def clavier(e):
            """
            intercepte toutes les touches tapées et décide l'action appropriée
            """
            e = e.keysym
            log("touche pressée -", e)
            if not self.att:
                coords = [int(i / self.x) for i in F_terrain.coords("perso")]
                mov = [0, 0]
                if e == self.options["DEFAULT"]["haut"]:
                    mov[1] = -1
                elif e == self.options["DEFAULT"]["bas"]:
                    mov[1] = 1
                elif e == self.options["DEFAULT"]["gauche"]:
                    mov[0] = -1
                elif e == self.options["DEFAULT"]["droite"]:
                    mov[0] = 1
                elif e == self.options["DEFAULT"]["action"]:
                    log("tentative d'interaction")
                    self.att = 1
                    inter(coords)
                if mov != [0, 0]:
                    log("coords", coords)
                    log("tentative de mouvement")
                    self.att = 1
                    mouv(mov, coords)

        self.bind_all("<Key>", clavier)
        
        def retour():
            """
            retour au dernier checkpoint
            """
            log("défaite")
            self.son("gameover")
            self.parties[nom]["inv"] = self.parties[nom]["S_inv"]
            self.parties[nom]["niv"] = self.parties[nom]["S_niv"]
            self.parties[nom]["score"] = self.parties[nom]["S_score"]
            V_xp.set(self.parties[nom]["score"])
            self.parties[nom]["pos"] = ""
            self.parties[nom]["vie"] = "5"
            A_vie["value"] = 5
            charge(self.parties[nom]["niv"])
            
        def vie(delta):
            """
            effectue les changements de niveau de vie
            """
            log("changement de vie =", delta)
            valeur = A_vie["value"]
            valeur += delta
            if valeur <= 0:
                retour()
            else:
                A_vie["value"] = valeur
                self.parties[nom]["vie"] = str(valeur)
                if valeur < 5:
                    couleur = "red"
                elif 5 <= valeur < 10:
                    couleur = "orange"
                elif 10 <= valeur < 15:
                    couleur = "green"
                else:
                    couleur = "blue"
                self.ttkStyle.configure("TProgressbar", foreground=couleur, background=couleur)
                
        def xp(delta):
            """
            effectue les changements de score
            """
            log("changement d'expérience =", delta)
            valeur = V_xp.get()
            valeur += delta
            V_xp.set(valeur)
            self.parties[nom]["score"] = str(valeur)
            
        def inv(obj):
            """
            rajoute les objets récoltés
            """
            log("changement d'inventaire =", obj)
            liste = self.parties[nom]["inv"].split(",") if self.parties[nom]["inv"] != "" else []
            if obj not in liste and obj !="":
                liste.append(obj)
                A_inv.insert(
                parent="",
                index="end",
                values=(self.loc[obj],)
                )
                self.parties[nom]["inv"] = ",".join(liste)
                
        def ambiance():
            """
            son de fond
            """
            self.son("ambiance")
            F_jeu.after(22680, ambiance)
            

        class dialogue(Toplevel):
            """
            ouvre une fenetre de dialogue
            """
            def __init__(self):
                """
                initialisation du dialogue
                """
                super().__init__(
                    master=fenetre,
                    bg="black",
                    bd = 10,
                    relief="raised"
                )
                self.res = None
                self.L_F = fenetre.L_F
                self.H_F = fenetre.H_F
                self.loc = fenetre.loc
                self.style = fenetre.style
                self.resizable(0, 0)
                self.minsize(width=int(self.L_F/2), height=int(self.H_F/2))
                self.geometry("{0}x{1}+{2}+{3}".format(int(self.L_F/2), int(self.H_F/2), int(self.L_F/4), int(self.H_F/4)))
                #self.overrideredirect(True)
                
            def animation(self, texte, anim=None, ips=None):
                """
                lance une animation
                """
                T_texte = Label(
                    master=self,
                    text=fenetre.loc[texte],
                    font=fenetre.style["font"],
                    justify="left",
                    wraplength=int(self.L_F/2)-10,
                    fg="white",
                    bg="black",
                )
                T_texte.place(relx=0.5, rely=0.5, anchor="center")
                if anim != None:
                    images = [PhotoImage(file=ch('media/'+anim), format='gif -index %i' %(i), width=int(self.L_F/2), height=int(self.H_F/2),) for i in range(ips)]
                    def maj(ind):
                        """
                        passe à l'image suivante de l'animation
                        """
                        if ind < ips:
                            image = images[ind]
                            ind += 1
                            T_texte.configure(image=image)
                            self.after(130, maj, ind)
                        else:
                            T_texte.configure(image="")
                    maj(0)
                self.bind_all("<ButtonRelease>", self.destruc)
                self.bind_all("<Return>", self.destruc)
                self.bind_all("<{0}>".format(fenetre.options["DEFAULT"]["action"]), self.destruc)
            
            def question(self, case):
                """
                pose une question au joueur
                """
                bonne = int(self.loc[case+"_q"][0]) - 1
                nb = int(self.loc[case+"_q"][1])
                self.columnconfigure([i for i in range(nb)], minsize=self.L_F/(2*nb))
                self.rowconfigure([i for i in range(4)], minsize=self.H_F/8)
                T_question = Label(
                    master=self,
                    text=self.loc[case+"_q"][2:],
                    **self.style,
                )
                T_question.grid(row=0, column=0, rowspan=4, columnspan=nb, sticky="nswe")
                def rep(i):
                    if i == bonne:
                        res = self.loc[case+"_+"]
                        fenetre.son("monstre_dying")
                    else:
                        res = self.loc[case+"_-"]
                    fenetre.res = res
                    self.destruc()
                
                for i in range(nb):
                    Button(
                        master=self,
                        text=self.loc[case+"_"+str(i)],
                        command=lambda i=i: rep(i),
                        **self.style,
                    ).grid(row=3, column=i, sticky="nswe")
            
            def mastermind(self, case):
                pass
            
            def destruc(self, *args):
                """
                retourne à la fentre de jeu principale
                """
                log("destruction")
                fenetre.att = 0
                self.unbind_all("<ButtonRelease>")
                self.unbind_all("<Return>")
                self.unbind_all("<{0}>".format(fenetre.options["DEFAULT"]["action"]))
                self.destroy()
            
        #placement
        A_inv.grid(row=7, column=0, sticky="nswe", columnspan=4, rowspan=6)
        T_vie.grid(row=1, column=0, sticky="nswe")
        A_vie.grid(row=1, column=1, sticky="nswe", columnspan=3)
        T_niveau.grid(row=3, column=0, sticky="nswe", columnspan=2)
        A_niveau.grid(row=3, column=2, sticky="nswe", columnspan=2)
        T_xp.grid(row=5, column=0, sticky="nswe", columnspan=2)
        A_xp.grid(row=5, column=2, sticky="nswe", columnspan=2)
        B_quitter.grid(row=14, column=1, sticky="nswe", columnspan=2)

        if self.options["DEFAULT"].getboolean("son"):
            ambiance()
        vie(0)
        xp(0)
        charge(self.parties[nom]["niv"])
          
log("début de l'execution")
fenetre = maitre()
fenetre.acceuil()
fenetre.mainloop() #fin du script !
