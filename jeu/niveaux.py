"""
fonctionement case:
    chaque case a un nom en trois lettres, qui signifient:
        première lettre --> type physique: V pour vide, S pour sol, M pour mur, C pour coffre, ...
        deuxième lettre --> variante visuelle: P pour pierre, R pour rouge, S pour sable, F pour feuille, ...
        troisième lettre -> utilité fonctionelle: 1 pour monstre ayant la première clé, a pour indice N°1, ...
    exemples: "SSC", "V--", "MP+"
possibilité d'utiliser n'importe quel caractère valable pour des noms de fichiers (tout sauf "/\*<>?|)
"""
niv = {
    "11" : {
        "li" : 20,
        "col" : 29,
        "def_pos" : [2,1],
        "grille" : [
            ["MP-","MP-","MP-","Mp-","MP-","MP-","MP-","Mp-","MF-","MP-","MP-","MF-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","CD1","SG-","MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--","MP-","MP-","MP-","MP-","MP-","Mp-","MF-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MF-","MF-",],
            ["Mp-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-",],
            ["MP-","FB1","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--","Mp-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","Mp-",],
            ["MP-","MP-","MP-","MP-","MF-","SG-","SG-","MP-","MP-","MF-","MP-","MP-","V--","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-",],
            ["V--","V--","V--","V--","MP-","SG-","SG-","MP-","V--","V--","V--","V--","V--","MF-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-",],
            ["Mp-","Mp-","MP-","MP-","MP-","SG-","SG-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-",],
            ["MP-","SG-","OP1","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","FB1","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-",],
            ["MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-",],
            ["MP-","MP-","MP-","MP-","MP-","SG-","SG-","MP-","MP-","MP-","MP-","MP-","MP-","MF-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-",],
            ["V--","V--","V--","V--","MP-","SG-","SG-","MF-","V--","V--","V--","V--","V--","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","Mp-",],
            ["MP-","Mp-","MP-","Mp-","MP-","SG-","SG-","MP-","MP-","MP-","MP-","Mp-","V--","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-",],
            ["MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-",],
            ["MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","OP1","SG-","SG-","MP-","V--","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-",],
            ["Mp-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--","MP-","MP-","MF-","MP-","Mp-","MP-","MP-","MP-","MP-","MP-","MP-","MF-","MP-","Mp-","MP-","MP-",],
            ["MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["MP-","SG-","SG-","FB1","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["MP-","MP-","MP-","MP-","MP-","V--","V--","MF-","MP-","MP-","MP-","MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
        ],
        "def_img" : "SG",
    },
    "21" : {
        "li" : 15,
        "col" : 37,
        "grille" : [
            ["V--","V--","V--",
            ["V--","V--","V--",
            ["V--","V--","V--",
            ["V--","V--","V--",
            ["V--","V--","V--",
            ["V--","V--","MP-",
            ["V--","V--","MP-",
            ["V--","V--","MP-",
            ["V--","V--","MP-","MP-","MP-","MP-","MP-",
            ["V--","V--","V--","V--","V--","V--","MP-",
            ["MP-","MP-","MP-","MP-","MP-","MP-","MP-",
            ["MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",
            ["MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-",
            ["V--","V--",

        ]   
    },
}
"V--","MP-",