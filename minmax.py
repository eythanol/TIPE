from copy import deepcopy
from structure import J1, decompte, coups_possibles, jouer, nouv_score

def choix_coups(grille, joueur, niveau=1):
    coups_poss = coups_possibles(grille)

    # Cas d'arret
    if (len(coups_poss) == 0) or (niveau == 0):
        return decompte(grille), []
    
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


    return score, coup_choisi[score]