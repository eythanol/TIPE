from copy import deepcopy
from jeu import J1, decompte, coups_possibles, jouer, nouv_score


def conversion(grille:list) -> tuple:
    """
    grille : liste de liste qui constitue la grille de jeu

    convertit la grille sous forme de tuple de tuples
    """
    N = len(grille)
    return tuple(tuple(grille[i]) for i in range(N))


graphe_partie = {} # stocke les coups déjà calculés

def choix_coups(grille, joueur, niveau=1):
    coups_poss = coups_possibles(grille)

    # Cas d'arret
    if (len(coups_poss) == 0) or (niveau == 0):
        return decompte(grille), []

    grille_tuple = conversion(grille)

    # Cas où le calcul est déjà fait, position connue
    if grille_tuple in graphe_partie:
        return graphe_partie[grille_tuple]
        
    coup_choisi = {}
    for (i, j) in coups_poss:
        copie = deepcopy(grille)

        # teste un coup
        score_precedant = decompte(copie) # score avant de jouer le coup

        jouer(copie, (i, j))
        nouv_score(copie, joueur, (i, j))

        score_suivant = decompte(copie) # score après avoir joué le coup
        # affiche_grille(copie, tour, joueur, score_suivant)
        print()

        # on appelle l'algorithme selon si le coup joué permet de rejouer ou non (car changement de joueur)
        if score_precedant == score_suivant:
            score, choix = choix_coups(copie, joueur*(-1), niveau-1) 
        else:
            score, choix = choix_coups(copie, joueur, niveau-1)

        if score in coup_choisi:
            coup_choisi[score].append((i, j))
        else:
            coup_choisi[score] = [(i, j)]
    
    if joueur == J1:
        score = max(coup_choisi.keys())
    else:
        score = min(coup_choisi.keys())

    graphe_partie[grille_tuple] = (score, coup_choisi[score]) # une fois le calcul réalisé, on le stocke dans le graphe et on le réutilise en cas de besoin

    return score, coup_choisi[score]
