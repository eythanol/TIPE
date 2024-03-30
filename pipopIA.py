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
    cases_formées = []
    for (i, j) in cases_possibles:
        if traits_adjacents(grille, (i, j)) == [trait, trait, trait, trait]:
            grille[i][j] = joueur
            cases_formées.append((i, j))
    return cases_formées

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

def p(x):
    print(x, end="")

def affiche_grille(grille, tour=0, joueur=0, score=0):
    # affiche la grille comme une matrice de taille N x P
    N = len(grille)
    P = len(grille[0])
    
    dec = " "*(N*(tour-1))
    if tour!=0:
        print(dec, "Tour", tour)
    
    for i in range(N):
        p(dec)
        for j in range(P):
            v = grille[i][j]
            if v == J1:     p("1")
            if v == J2:     p("2")
            if v == vide:   p(" ")
            if v == trait and i%2==0:  p("-")
            if v == trait and i%2==1:  p("|")
        if i==N-1:
            if joueur!=0:
                p( "  => joué par " + ("J1 score=" if joueur==1 else "J2 score=") + str(score))
        print()
    
    #prompt = f"[ {grille[0]} \n"
    #for i in range(1, len(grille)-1):
    #    prompt += f"  {grille[i]} \n"
    #prompt += f"  {grille[-1]} ]"
    #print(prompt)



# minmax
    
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

# grille = [[0 for j in range(2*P - 1)] for i in range(2*N - 1)]
# affiche_grille(grille)
# print(choix_coups(grille, J1))

###------------------------------| parties |--------------------------###
import tkinter as tk

class App(tk.Frame):
    def __init__(self, master, N=2, P=2, L=600, l=600, tour_IA=-1):
        super().__init__(master)

        # intégration du jeu à la fenêtre
        self.grille = [[0 for j in range(2*P - 1)] for i in range(2*N - 1)]

        self.tour = J1 # qui doit jouer : (1 => Joueur 1) , (-1 => Joueur 2)
        self.tour_IA = tour_IA

        # affiche le nom du joueur qui doit jouer
        self.txt = tk.StringVar()
        self.text = tk.Label(bd = 0, textvariable=self.txt, height=2, font=("Comic sans MS", 25))
        self.txt.set("Pipopipette")
        self.text.pack()

        # bouton réinitialiser
        #self.btn = tk.Button(text='Restart', font=('Comic sans MS', 23), command=self.restart)

        # tableau des scores
        self.tabscore = tk.Label(bd = 0, text='Score :', height=2, font=("Arial", 18, 'underline'))
        self.scor1 = tk.StringVar()
        self.scor2 = tk.StringVar()
        self.scor1.set('joueur 1 : 0')
        self.scor2.set('joueur 2 : 0')
        self.score1 = tk.Label(bd = 0, textvariable=self.scor1, height=2, font=("Arial", 18))
        self.score2 = tk.Label(bd = 0, textvariable=self.scor2, height=2, font=("Arial", 18))

        # comptage des traits
        self.nb_trait = 0
        self.nombre = tk.StringVar()
        self.nombre.set(f'nombre de traits : {self.nb_trait}')
        self.compte = tk.Label(bd = 0, textvariable=self.nombre, height=2, font=("Arial", 18, 'underline'))

        # terrain de jeu
        self.canv = tk.Canvas(bg="white", height=L, width=l)
        
        # paramètres pour placer les points/cases/traits
        cote = min(l, L)

        r = 45/N

        dx = cote/(P+1)
        dy = cote/(N+1)

        # cases
        self.cases = {(i, j) : [] for (i, j) in liste_cases(self.grille)}
        for (i, j) in self.cases.keys():
            x1 = dx*((i+1)//2)
            x2 = dx*((i+1)//2 + 1)
            y1 = dy*((j+1)//2)
            y2 = dy*((j+1)//2 + 1) 
            case_id = self.canv.create_rectangle((y1, x1, y2, x2), fill='white', width=1)
            self.cases[(i, j)] = case_id


        # traits
        self.traits = {(i, j) : [] for (i, j) in coups_possibles(self.grille)}

        for (i, j) in self.traits.keys():
            # dessine un trait : (i pair => - ) (j pair => | )
            if j%2:
                x1 = dx*(j//2 + 1)
                y1 = dy*((i+1)//2 + 1)
                x2 = dx*(j//2 + 2)
                y2 = dy*(((i+1)//2 + 1))
            else:
                x1 = dx*((j+1)//2 + 1)
                y1 = dy*(i//2 + 1)
                x2 = dx*((j+1)//2 + 1)
                y2 = dy*((i//2 + 2))
                
            trait_id = self.canv.create_line((x1, y1 , x2, y2), fill='white', width=r)
            self.traits[(i, j)] = trait_id
    
        for t in self.traits:
            self.canv.tag_bind(self.traits[t], f'<Button-1>', lambda e, var=self.traits[t]: self.trace(var))

        # points        
        cote = min(l, L)
        for j in range(1, N+1):
            for i in range(1, P+1):
                x1 = dx*i - r 
                y1 = dy*j - r 
                x2 = dx*i + r 
                y2 = dy*j + r 

                self.canv.create_oval((x1, y1, x2, y2), fill='black')


        self.canv.pack()

        self.tabscore.pack()
        self.score1.pack()
        self.score2.pack()

        self.compte.pack()

    def trace(self, trait):
        # trace un trait
        self.canv.itemconfig(trait, fill='black')

        # détermine la position du trait tracé dans la grille : traits_list[position] = (i, j) , trait = identifiant de (i, j)
        traits_list = list(self.traits.keys())
        traits_ij_list = list(self.traits.values())
        position = traits_ij_list.index(trait)
        (i, j) = traits_list[position]

        # joue un coup dans la grille et procède au décompte des points
        score_precedant = decompte(self.grille)

        jouer(self.grille, (i, j))
        cases = nouv_score(self.grille, self.tour, (i, j))
        score_suivant = decompte(self.grille)

        if score_precedant == score_suivant:
            self.tour = self.tour*(-1)

            if self.tour == self.tour_IA :
                # tour de l'IA
                (i, j) = choix_coups(self.grille, J2, niveau=1)[1][0]
                self.trace(self.traits[(i, j)])
            
        else:
            if self.tour == J1:                
                self.scor1.set(f'joueur 1 : {decompte(self.grille, J1)}')

                for (i, j) in cases:
                    case_formée = self.cases[(i, j)]
                    self.canv.itemconfig(case_formée, fill='blue')

            else:
                self.scor2.set(f'joueur 2 : {decompte(self.grille, J2)}')

                for (i, j) in cases:
                    case_formée = self.cases[(i, j)]
                    self.canv.itemconfig(case_formée, fill='red')

                # tour de l'IA
                (i, j) = choix_coups(self.grille, J2, niveau=1)[1][0]
                self.trace(self.traits[(i, j)])
        

N = 3
P = 3

root = tk.Tk()
myapp = App(root, N, P)
myapp.master.geometry("1200x950")
myapp.mainloop()