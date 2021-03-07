"""
fonctionement texture:
    chaque texture a un nom en trois lettres, qui signifient:
        première lettre --> type: V pour vide, S pour sol, M pour mur, C pour coffre, ...
        deuxième lettre --> matériau/couleur: P pour pierre, R pour rouge, S pour sable, ...
        troisième lettre -> variante: C pour craquelé, F pour feuille, B pour brillante, ...
    exemples: "SSC", "V--", "MP+"
possibilité d'utiliser n'importe quel caractère valable pour des noms de fichiers (tout sauf "/\*<>?|)
"""
niv = {
    11 : {
        "li" : 10,
        "col" : 10,
        "def_pos" : "05,05",
        "grille" : [
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--"],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--"],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--"],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--"],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--"],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--"],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--"],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--"],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--"],
            ["V--","V--","V--","V--","V--","V--","V--","V--","V--","V--"],
        ]
    },
    12 : {
        "li" : 10,
        "col" : 10,
        "grille" : [
            
        ]
    },
}