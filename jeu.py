# définir les joueurs et ce que veut dire : "tracer un trait"
J1 = 1
J2 = -1
trait = "X"
vide = 0

def cases_dispo(grille):
    # renvoies la liste des cases que l'on peut former
    cases = []
    N = len(grille)
    P = len(grille[0])
    for i in range(1, N, 2):
        for j in range(1, P, 2):
            if grille[i][j] == 0:
                cases.append((i, j))
    return cases

def liste_cases(grille):
    # renvoies toutes les cases de la grille
    cases = []
    N = len(grille)
    P = len(grille[0])
    for i in range(1, N, 2):
        for j in range(1, P, 2):
            cases.append((i, j))
    return cases

def traits_adjacents(grille, case):
    # renvoie les traits qui permettent de former la case
    i, j = case
    return [grille[i-1][j], grille[i+1][j], grille[i][j-1], grille[i][j+1]]

def jouer(grille, case):
    # joue un trait dans la grille
    i, j = case
    grille[i][j] = trait

def nouv_score(grille, joueur, dernier_coup):
    # donne le score en fonction du joueur et du dernier coup
    # modifie la grille
    # renvoies les dernières cases formées

    # donne les cases que l'on peut former en jouant dernier_coup
    i, j = dernier_coup
    if i % 2 :
        cases_potentielles = [(i, j-1), (i, j+1)]
    else:
        cases_potentielles = [(i - 1, j), (i + 1, j)]
    
    # intersecte avec toutes les cases que l'on peut former : cases réelles
    cases_possibles = list(set(cases_dispo(grille)) & set(cases_potentielles))

    # donne un score aux cases formées si le dernier_coup le permet
    cases_formees = []
    for (i, j) in cases_possibles:
        if traits_adjacents(grille, (i, j)) == [trait, trait, trait, trait]:
            grille[i][j] = joueur
            cases_formees.append((i, j))
    return cases_formees

def decompte(grille, joueur=0):
    # renvoies le score de la grille / compte les points du joueur 1 ou du joueur 2 si demandé en mettant joueur = 1 ou -1
    somme = 0
    for (i, j) in liste_cases(grille):
        if joueur == J1 and grille[i][j] > 0:
            somme += grille[i][j]

        elif joueur == J2 and grille[i][j] < 0:
            somme += grille[i][j]*(-1)

        elif joueur == 0:
            somme += grille[i][j]
    return somme

def coups_possibles(grille):
    # prends en parametre la grille et renvoies la listes des coups possibles
    N = len(grille)
    P = len(grille[0])

    liste_coups =[]

    for i in range(1, N, 2):
        for j in range(0, P, 2):
            if grille[i][j] == vide:
                liste_coups.append((i, j))

    for i in range(0, N, 2):
        for j in range(1, P, 2):
            if grille[i][j] == vide:
                liste_coups.append((i, j))
    
    return liste_coups