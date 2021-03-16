def test():
    import tkinter as tk
    import tkinter.messagebox as msg
    from boombox import BoomBox
    import os
    import sys
    
    def ch(fichier):
        return os.path.join(sys.path[0], str(fichier))
    
    maitre = tk.Tk()
    maitre.title("Morpion!")

    prin = tk.Frame(master=maitre)
    prin.rowconfigure([0, 1, 2], minsize=100, weight=1)
    prin.columnconfigure([0, 1, 2], minsize=100, weight=1)
    prin.pack()

    X = tk.PhotoImage(file=ch("X.png"))
    X = X.subsample(25,25)
    O = tk.PhotoImage(file=ch("O.gif"))
    O = O.subsample(25,25)

    tour = 1
    victoire = 0
    grille = [[0, 0, 0],
              [0, 0, 0],
              [0, 0, 0]]

    def fin(tour):
        if victoire == 42:
            t = "Egalité !"
        else:
            t = forme(tour, "texte") + " a gagné!"
        BoomBox(os.path.join(sys.path[0],"1_honteux_Rene.wav"), wait=False).play()
        
        msg.showinfo("Fin du jeu", t)
        maitre.destroy()

    def forme(y, type="texte"):
        if y == -1 and type == "image":
            y = X
        elif y == -1 and type == "texte":
            y = "X"
        elif y == 1 and type == "image":
            y = O
        elif y == 1 and type == "texte":
            y = "O"
        elif y == 0:
            y = "-"
        else:
            y = "erreur"
        return y

    def jeu(x, y):
        nonlocal tour
        nonlocal victoire
        nonlocal grille
        nonlocal prin
        if grille[y][x] == 0:
            grille[y][x] = tour

            prin.grid_slaves(y, x)[0].config(image=forme(tour, "image"))

            # test d'une éventuelle égalité
            if (not 0 in grille[2]) == (not 0 in grille[1]) == (not 0 in grille[0]) == True:
                victoire = 42

            # test de victoire par colonne
            for x in range(3):
                if grille[2][x] == grille[1][x] == grille[0][x] != 0:
                    victoire = tour

            # test de victoire par ligne
            for x in range(3):
                if grille[x][0] == grille[x][1] == grille[x][2] != 0:
                    victoire = tour

            # test de victoire par diagonale
            if (grille[2][0] == grille[1][1] == grille[0][2] != 0) or (grille[2][2] == grille[1][1] == grille[0][0] != 0):
                victoire = tour

            if victoire != 0:
                fin(tour)
            tour *= -1

    for i in range(3):
        for j in range(3):
            case = tk.Button(
                master=prin,
                text="-",
                command=lambda i=i, j=j: jeu(i, j),
                width=10,
                height=5,
                image=None,
            )
            case.grid(column=i, row=j, padx=5, pady=5, sticky="nswe")
    maitre.mainloop()


test()
