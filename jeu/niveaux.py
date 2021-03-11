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
    "11" : {
        "li" : 20,
        "col" : 29,
        "def_pos" : [6,19],
        "grille" : [
            ["MPC","MPC","MPC","MPD","MPC","MPC","MPC","MPD","MPF","MPC","MPC","MPF","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MPC","V--","MPC","MPC","MPC","MPC","MPC","MPD","MPF","MPC","MPC","MPC","MPC","MPC","MPC","MPC","MPF","MPF",],
            ["MPD","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MPC","V--","MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MPC",],
            ["MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MPC","V--","MPD","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MPD",],
            ["MPC","MPC","MPC","MPC","MPF","V--","V--","MPC","MPC","MPF","MPC","MPC","V--","MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MPC",],
            ["V--","V--","V--","V--","MPC","V--","V--","MPC","V--","V--","V--","V--","V--","MPF","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MPC",],
            ["MPD","MPD","MPC","MPC","MPC","V--","V--","MPC","MPC","MPC","MPC","MPC","MPC","MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MPC",],
            ["MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MPC",],
            ["MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MPC",],
            ["MPC","MPC","MPC","MPC","MPC","V--","V--","MPC","MPC","MPC","MPC","MPC","MPC","MPF","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MPC",],
            ["V--","V--","V--","V--","MPC","V--","V--","MPF","V--","V--","V--","V--","V--","MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MPD",],
            ["MPC","MPD","MPC","MPD","MPC","V--","V--","MPC","MPC","MPC","MPC","MPD","V--","MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MPC",],
            ["MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MPC","V--","MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MPC",],
            ["MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MPC","V--","MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MPC",],
            ["MPD","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MPC","V--","MPC","MPC","MPF","MPC","MPD","MPC","MPC","MPC","MPC","MPC","MPC","MPF","MPC","MPD","MPC","MPC",],
            ["MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["MPC","MPC","MPC","MPC","MPC","V--","V--","MPF","MPC","MPC","MPC","MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
        ]
    },
    "21" : {
        "li" : 10,
        "col" : 10,
        "grille" : [
            
        ]
    },
}