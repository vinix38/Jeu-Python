import tkinter as tk

fenetre = tk.Tk()
fenetre.title("Ceci est un jeu")

maitre = tk.Frame()
maitre.grid(
    sticky="nswe",
)

maitre.columnconfigure(0, minsize=500, weight=1)
maitre.rowconfigure(0, minsize=500, weight=1)
maitre.rowconfigure(1, minsize=50, weight=1)

emplacement1 = tk.Label(
    fg="black",
    bg=None,
    text="numero1",
    master=maitre,
    relief="sunken"
)
emplacement2 = tk.Label(
    fg="white",
    bg="black",
    text="numero2",
    master=maitre,
)

emplacement1.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=5,
    pady=5,
)
emplacement2.grid(
    row=1,
    column=0,
    sticky="nsew",
    padx=5,
    pady=5,
)


maitre.mainloop()
