from copy import deepcopy

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

    # donne les cases que l'on peut former en jouant dernier_coup
    i, j = dernier_coup
    if i % 2 :
        cases_potentielles = [(i, j-1), (i, j+1)]
    else:
        cases_potentielles = [(i - 1, j), (i + 1, j)]
    
    # intersecte avec toutes les cases que l'on peut former : cases réelles
    cases_possibles = list(set(cases_dispo(grille)) & set(cases_potentielles))

    # donne un score aux cases formées si le dernier_coup le permet
    for (i, j) in cases_possibles:
        if traits_adjacents(grille, (i, j)) == [trait, trait, trait, trait]:
            grille[i][j] = joueur

def decompte(grille):
    # renvoies le score de la grille
    somme = 0
    for (i, j) in liste_cases(grille):
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

def affiche_grille(grille):
    # affiche la grille comme une matrice de taille N x P
    prompt = f"[ {grille[0]} \n"
    for i in range(1, len(grille)-1):
        prompt += f"  {grille[i]} \n"
    prompt += f"  {grille[-1]} ]"
    print(prompt)



# minmax
    
def choix_coups(grille, joueur, n):
    coups_poss = coups_possibles(grille)

    # Cas d'arret
    if len(coups_poss) == 0 or n == 0:
        return decompte(grille), []
    
    coup_choisi = {}
    for (i, j) in coups_poss:
        copie = deepcopy(grille)

        # teste un coup
        score_precedant = decompte(copie) # score avant de jouer le coup


        jouer(copie, (i, j))
        nouv_score(copie, joueur, (i, j))

        score_suivant = decompte(copie) # score après avoir joué le coup


        # on appelle l'algorithme selon si le coup joué permet de rejouer ou non (car changement de joueur)
        if score_precedant == score_suivant:
            score, choix = choix_coups(copie, joueur*(-1), n-1) 
        else:
            score, choix = choix_coups(copie, joueur, n-1)

        if score in coup_choisi:
            coup_choisi[score].append((i, j))
        else:
            coup_choisi[score] = [(i, j)]
    
    if joueur == J1:
        score = max(coup_choisi.keys())
    else:
        score = min(coup_choisi.keys())

    return score, coup_choisi[score]

N = 2
P = 2

grille = [[0 for j in range(2*P - 1)] for i in range(2*N - 1)]

affiche_grille(grille)
print(choix_coups(grille, J1, n=6))