"""
fonctionement case: #opus :OP1 fantôme : FB1 givine :GI struck boon : SB
    chaque case a un nom en trois lettres, qui signifient:
        première lettre --> type physique: V pour vide, S pour sol, M pour mur, C pour coffre, ...
        deuxième lettre --> variante visuelle: P pour pierre, R pour rouge, S pour sable, F pour feuille, ...
        troisième lettre -> utilité fonctionelle: 1 pour monstre ayant la première clé, a pour indice N°1, ...
    exemples: "SSC", "V--", "MP+"
possibilité d'utiliser n'importe quel caractère valable pour des noms de fichiers (tout sauf "/\*<>?|)
"""
niv = {
    "1" : {
        "li" : 20,
        "col" : 29,
        "def_pos" : [2,1],
        "grille" : [
            ["MP-","MP-","MP-","M9-","MP-","MP-","MP-","M9-","MF-","MP-","MP-","MF-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","CD1","SG-","MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--","MP-","MP-","MP-","MP-","MP-","M9-","MF-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MF-","MF-",],
            ["M9-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-",],
            ["MP-","FB1","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--","M9-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","M9-",],
            ["MP-","MP-","MP-","MP-","MF-","SG-","SG-","MP-","MP-","MF-","MP-","MP-","V--","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-",],
            ["V--","V--","V--","V--","MP-","PG1","PD1","MP-","V--","V--","V--","V--","V--","MF-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-",],
            ["M9-","M9-","MP-","MP-","MP-","SG-","SG-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-",],
            ["MP-","SG-","OP2","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","FB2","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-",],
            ["MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-",],
            ["MP-","MP-","MP-","MP-","MP-","SG-","SG-","MP-","MP-","MP-","MP-","MP-","MP-","MF-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-",],
            ["V--","V--","V--","V--","MP-","SG-","SG-","MF-","V--","V--","V--","V--","V--","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","M9-",],
            ["MP-","M9-","MP-","M9-","MP-","SG-","SG-","MP-","MP-","MP-","MP-","M9-","V--","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-",],
            ["MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-",],
            ["MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","OP1","SG-","SG-","MP-","V--","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-",],
            ["M9-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--","MP-","MP-","MF-","MP-","M9-","MP-","MP-","MP-","MP-","MP-","MP-","MF-","MP-","M9-","MP-","MP-",],
            ["MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["MP-","SG-","SG-","FB3","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["MP-","MP-","MP-","MP-","MP-","PG+","PD+","MF-","MP-","MP-","MP-","MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
        ],
        "def_img" : "SG",
    },
    "2" : {
        "li" : 14,
        "col" : 37,
        "def_pos" : [7,0],
        "grille" : [
            ["V--","V--","V--","V--","V--","V--","MP-","SG-","SG-","MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","V--","V--","V--","MF-","SG-","SG-","M9-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","V--","V--","V--","MP-","SG-","SG-","MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","V--","V--","V--","MP-","SG-","SG-","MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","V--","V--","V--","M9-","SG-","SG-","MF-","MF-","MP-","M9-","M9-","MF-","MP-","M9-","MF-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","MP-","MP-","MF-","MP-","MF-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","OP3","SG-","OP1","MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","MP-","FB1","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","M9-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","MF-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","OP2","MF-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","MP-","MF-","MF-","MP-","MP-","SG-","SG-","MP-","MF-","MP-","M9-","MP-","MF-","MF-","MP-","MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","V--","V--","V--","M9-","SG-","SG-","MF-","V--","V--","V--","V--","V--","V--","V--","V--","V--","M9-","MP-","M9-","MP-","MF-","MF-","MF-","MP-","MP-","V--","V--","MP-","M9-","M9-","MF-","MP-","MF-","MP-",],
            ["M9-","MP-","MF-","MP-","MP-","MF-","MF-","SG-","SG-","MP-","MP-","M9-","MP-","MP-","M9-","M9-","MF-","MP-","MP-","M9-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","CD2","MP-",],
            ["M9-","SG-","SG-","SG-","SG-","SG-","SG-","FB2","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MF-","M9-","MP-","SG-","SG-","SG-","SG-","SG-","MF-",],
            ["MP-","MP-","MF-","MP-","MP-","M9-","MF-","MF-","MP-","M9-","MP-","MP-","MF-","M9-","MP-","MP-","MP-","MF-","MF-","MP-","SG-","SG-","SG-","SG-","SG-","OP5","SG-","OP4","MP-","V--","MP-","SG-","SG-","SG-","SG-","CD1","MP-",],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","M9-","MP-","M9-","M9-","MP-","MF-","MP-","MF-","MP-","V--","MF-","MF-","MP-","MP-","M9-","M9-","MP-",],

        ]
        ,"def_img" : "SG",
    },
    "3" : {
        "li" : 19,
        "col" : 30,
        "def_pos" : [16,7],
        "grille" : [
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","V--",],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--",],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--",],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--",],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--",],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--",],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--",],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--",],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","MP-","MP-","MP-","SG-","SG-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","V--",],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","SG-","SG-","MP-","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","SG-","SG-","MP-","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","V--","V--","V--","V--","MP-","MP-","MP-","V--","MP-","MP-","MP-","V--","V--","V--","V--","MP-","SG-","SG-","MP-","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","V--","MP-","MP-","MP-","MP-","SG-","MP-","MP-","MP-","SG-","MP-","MP-","MP-","MP-","MP-","MP-","SG-","SG-","MP-","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","V--","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","V--","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","V--","MP-","MP-","MP-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","V--","V--","V--","MP-","SG-","SG-","MP-","MP-","MP-","MP-","MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","V--","V--","V--","MP-","MP-","MP-","MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],

        ]
        ,"def_img" : "SG",
    },
    "4" : {
        "li" : 19,
        "col" : 30,
        "def_pos" : [19,21],
        "grille" : [
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","V--","V--","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","MP-","V--","V--","V--",],
            ["MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","MP-","MP-","MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","V--","V--","V--",],
            ["MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","V--","V--","V--",],
            ["MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","MP-","MP-","MP-","V--","V--","MP-","MP-","MP-","MP-",],
            ["MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","MP-","MP-","MP-","V--","V--","V--","V--","V--","MP-","V--","V--","MP-","V--","V--","V--","V--","V--","MP-",],
            ["MP-","MP-","MP-","MP-","MP-","V--","V--","V--","MP-","MP-","MP-","MP-","V--","V--","MP-","V--","V--","V--","V--","V--","MP-","V--","V--","MP-","V--","V--","MP-","MP-","MP-","MP-",],
            ["V--","V--","V--","V--","MP-","V--","V--","V--","MP-","V--","V--","V--","V--","V--","MP-","MP-","MP-","MP-","MP-","MP-","MP-","V--","V--","MP-","V--","V--","MP-","V--","V--","V--",],
            ["V--","V--","V--","V--","MP-","V--","V--","V--","MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","V--","V--","MP-","V--","V--","V--",],
            ["V--","V--","V--","MP-","MP-","V--","V--","V--","MP-","MP-","MP-","V--","MP-","MP-","MP-","MP-","MP-","MP-","V--","V--","V--","V--","V--","MP-","MP-","MP-","MP-","V--","V--","V--",],
            ["V--","V--","V--","MP-","V--","V--","V--","V--","V--","V--","MP-","MP-","MP-","V--","V--","V--","V--","MP-","MP-","MP-","MP-","MP-","MP-","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","MP-","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","MP-","V--","V--","V--","V--","V--","MP-","MP-","MP-","V--","V--","V--","V--","MP-","MP-","MP-","MP-","V--","V--","MP-","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","MP-","V--","V--","V--","V--","MP-","V--","V--","MP-","V--","V--","V--","V--","MP-","V--","V--","MP-","V--","V--","MP-","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","MP-","MP-","MP-","MP-","MP-","MP-","V--","V--","MP-","MP-","MP-","MP-","MP-","MP-","V--","V--","MP-","V--","V--","MP-","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","V--","V--","MP-","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","SG-","SG-","MP-","V--","V--","V--","V--","V--","V--","V--",],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MP-","SG-","SG-","MP-","V--","V--","V--","V--","V--","V--","V--",],

        ]
        ,"def_img" : "SG",
    },
}