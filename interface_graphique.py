import tkinter as tk
from minmax import choix_coups
from jeu import J1, J2, liste_cases, coups_possibles, decompte, jouer, nouv_score

niveau_ia = 3

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
                (i, j) = choix_coups(self.grille, J2, niveau=niveau_ia)[1][0]
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
                (i, j) = choix_coups(self.grille, J2, niveau=niveau_ia)[1][0]
                self.trace(self.traits[(i, j)])
        

N = 4
P = 4

root = tk.Tk()
myapp = App(root, N, P)
myapp.master.geometry("1200x950")
myapp.mainloop()
