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
        "def_pos" : [2,1],
        "grille" : [
            ["MPC","MPC","MPC","MPD","MPC","MPC","MPC","MPD","MPF","MPC","MPC","MPF","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["MPC","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","CD1","SG-","MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["MPC","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["MPC","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MPC","V--","MPC","MPC","MPC","MPC","MPC","MPD","MPF","MPC","MPC","MPC","MPC","MPC","MPC","MPC","MPF","MPF",],
            ["MPD","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MPC","V--","MPC","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MPC",],
            ["MPC","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MPC","V--","MPD","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MPD",],
            ["MPC","MPC","MPC","MPC","MPF","SG-","SG-","MPC","MPC","MPF","MPC","MPC","V--","MPC","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MPC",],
            ["V--","V--","V--","V--","MPC","SG-","SG-","MPC","V--","V--","V--","V--","V--","MPF","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MPC",],
            ["MPD","MPD","MPC","MPC","MPC","SG-","SG-","MPC","MPC","MPC","MPC","MPC","MPC","MPC","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MPC",],
            ["MPC","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MPC",],
            ["MPC","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MPC",],
            ["MPC","MPC","MPC","MPC","MPC","SG-","SG-","MPC","MPC","MPC","MPC","MPC","MPC","MPF","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MPC",],
            ["V--","V--","V--","V--","MPC","SG-","SG-","MPF","V--","V--","V--","V--","V--","MPC","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MPD",],
            ["MPC","MPD","MPC","MPD","MPC","SG-","SG-","MPC","MPC","MPC","MPC","MPD","V--","MPC","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MPC",],
            ["MPC","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MPC","V--","MPC","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MPC",],
            ["MPC","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MPC","V--","MPC","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MPC",],
            ["MPD","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MPC","V--","MPC","MPC","MPF","MPC","MPD","MPC","MPC","MPC","MPC","MPC","MPC","MPF","MPC","MPD","MPC","MPC",],
            ["MPC","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
            ["MPC","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","SG-","MPC","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--","V--",],
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