import tkinter as tk
fenetre = tk.Tk()
fenetre.title("titre")

cadre = tk.Frame(master=fenetre)
cadre1 = tk.Frame(master=fenetre)

border_effects = {
    "flat": tk.FLAT,
    "sunken": tk.SUNKEN,
    "raised": tk.RAISED,
    "groove": tk.GROOVE,
    "ridge": tk.RIDGE,
}

for relief_name, relief in border_effects.items():
    frame = tk.Frame(master=cadre, relief=relief, borderwidth=5)
    frame.pack(side=tk.LEFT)
    label = tk.Label(master=frame, text=relief_name)
    label.pack()

texte = tk.Label(
    text="slt mon petit",
    fg="white",
    bg="#34A2FE",
    width=10,
    height=10,
    master=cadre,
)
bouton = tk.Button(
    text="Clique moi!",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    master=cadre,
)
entre = tk.Entry(
    fg="yellow",
    bg="blue",
    width=50,
    master=cadre,
)
recup = entre.get()
entre.delete(0, 4)
entre.delete(0, tk.END)
entre.insert(0, "insertion")

Mentre = tk.Text(
    fg="yellow",
    bg="blue",
    width=50,
    height=10,
    master=cadre,
)
recup = Mentre.get("1.0", tk.END)
Mentre.delete("1.0", "1.4")
Mentre.delete("1.0", tk.END)
Mentre.insert("1.0", "insertion")

#texte.pack(fill=tk.X, side=tk.LEFT, expand=True)
#bouton.pack(fill=tk.Y)
#entre.pack(fill=tk.BOTH)
#Mentre.place(x=0, y=0)

cadre.pack()
#cadre1.pack()

for i in range(3):
    fenetre.columnconfigure(i, weight=1, minsize=75)
    fenetre.rowconfigure(i, weight=1, minsize=50)

for i in range(3):
    for j in range(3):
        frame = tk.Frame(
            master=cadre1,
            relief=tk.RAISED,
            borderwidth=1
        )
        frame.grid(row=i, column=j, padx=5, pady=5)
        label = tk.Label(master=frame, text=f"Row {i}\nColumn {j}")
        label.pack(padx=5, pady=5)

label1 = tk.Label(text="A", master=cadre1)
label1.grid(row=0, column=0, sticky="nswe")


def handle_keypress(event):
    print(event.char)


fenetre.bind("<Key>", handle_keypress)


def handle_click(event):
    print("The button was clicked!")


button = tk.Button(text="Click me!")

button.bind("<Button-1>", handle_click)
button = tk.Button(text="aaa", command=())


def increase():
    value = int(lbl_value["text"])
    lbl_value["text"] = f"{value + 1}"


def decrease():
    value = int(lbl_value["text"])
    lbl_value["text"] = f"{value - 1}"


window = tk.Tk()

window.rowconfigure(0, minsize=50, weight=1)
window.columnconfigure([0, 1, 2], minsize=50, weight=1)

btn_decrease = tk.Button(master=window, text="-", command=decrease)
btn_decrease.grid(row=0, column=0, sticky="nsew")

lbl_value = tk.Label(master=window, text="0")
lbl_value.grid(row=0, column=1)

btn_increase = tk.Button(master=window, text="+", command=increase)
btn_increase.grid(row=0, column=2, sticky="nsew")

btn_increase.grid_remove()
btn_increase.grid_forget()

fenetre.mainloop()
"""
https://realpython.com/python-gui-tkinter/
https://tkdocs.com/tutorial/index.html
http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
https://docs.python.org/fr/3/library/tk.html

"""
