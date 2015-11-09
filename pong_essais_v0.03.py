#~ from tkinter import *
import tkinter as tk
from math import *
from random import randrange, uniform

class Raquette(object):
    GAUCHE = 0
    DROITE = 1
    #~ BAS = 2
    #~ HAUT = 3
    def __init__(self, canvas, position, longueur=100, largeur=20, vitesse=2):
        # Canvas où dessiner la raquette        
        self.canvas = canvas 
        self.xmax = int(canvas.cget('width'))  ## Récupération des dimensions
        self.ymax = int(canvas.cget('height')) ## du canvas
        
        # Type de raquette (GAUCHE, DROITE, HAUT ou BAS)
        self.position= position
        self.longueur = longueur
        self.largeur = largeur
        
        self.vitesse = vitesse
        
        # Paramètres de déplacement de la raquette :
        #  - self.x, self.y : coordonnées du centre de la raquette
        #  - self.touche_avance, self.touche_recule : touches pour déplacer la raquette
        
        if position == Raquette.GAUCHE :
            self.x = self.largeur/2+10          
        else :
            self.x = self.xmax-self.largeur/2-10
        self.y = self.ymax/2
        
        self.xdef = self.x
        self.ydef = self.y
        
        self.touche_avance = 'Down'
        self.touche_recule = 'Up'
        
        # Dessin de la raquette
        self.graph = self.canvas.create_rectangle(self.x-self.largeur/2 , self.y-self.longueur/2 ,self.x+self.largeur/2 , self.y+self.longueur/2 , width = 2 , fill = 'white')

        """
        # Pour les autres raquettes (haut, bas, gauche et droite)
        if position == Raquette.GAUCHE :
            self.x = self.largeur/2+10
            self.y = self.ymax/2
            self.graph = self.canvas.create_rectangle(self.x-self.largeur/2 , self.y-self.longueur/2 ,self.x+self.largeur/2 , self.y+self.longueur/2 , width = 2 , fill = 'white')
            self.touche_avance = 'Down'
            self.touche_recule = 'Up'
            self.direction = (0,1)
        elif position == Raquette.DROITE :
            self.x = self.xmax-self.largeur/2-10
            self.y = self.ymax/2
            self.graph = self.canvas.create_rectangle(self.x-self.largeur/2 , self.y-self.longueur/2 ,self.x+self.largeur/2 , self.y+self.longueur/2 , width = 2 , fill = 'white')
            self.touche_avance = 'Down'
            self.touche_recule = 'Up'
            self.direction = (0,1)
        #~ elif position == Raquette.BAS :
            #~ self.x = self.xmax/2
            #~ self.y = self.ymax-self.largeur/2-10
            #~ self.graph = self.canvas.create_rectangle(self.x-self.longueur/2 , self.y-self.largeur/2 ,self.x+self.longueur/2 , self.y+self.largeur/2 , width = 2 , fill = 'white')
            #~ self.touche_avance = 'Right'
            #~ self.touche_recule = 'Left'
            #~ self.direction = (1,0)
        #~ elif position == Raquette.HAUT :
            #~ self.x = self.xmax/2
            #~ self.y = self.largeur/2+10
            #~ self.graph = self.canvas.create_rectangle(self.x-self.longueur/2 , self.y-self.largeur/2 ,self.x+self.longueur/2 , self.y+self.largeur/2 , width = 2 , fill = 'white')
            #~ self.touche_avance = 'Right'
            #~ self.touche_recule = 'Left'
            self.direction = (0,1)
        """
        
    def redraw(self):
        """Redessine la raquette à la nouvelle position"""
        self.canvas.coords(self.graph , self.x-self.largeur/2 , self.y-self.longueur/2 ,self.x+self.largeur/2 , self.y+self.longueur/2)
    
    def deplace(self, direction):
        """Déplace la raquette de self.vitesse.
            Renvoie True si le déplacement est possible"""
        if (direction<0 and self.y-self.longueur/2 > self.vitesse) or (direction>0 and self.y+self.longueur/2 < self.ymax-self.vitesse):
            self.y = self.y + direction*self.vitesse
            self.redraw()
            return True
        else:
            return False


class Balle(object):
    """Classe de définition de la balle"""
    def __init__(self , canvas , x , y , rayon =15 , vitesse = 1.2):
        """Initialisation de la balle"""
        self.canvas = canvas

        ## rayon
        self.rayon = rayon

        ## Coordonnées initiales
        self.xdef = x
        self.ydef = y
        ## Coordonnées actuelles
        self.x = x
        self.y = y
        ## Vitesse (nombre de pixels à chaque déplacement) et accélération
        self.vitesse_init = vitesse  ## Vitesse de base
        self.vitesse = vitesse       ## Vitesse courante
        self.vitesse_max = 3
        #~ self.vitesse_lv = vitesse
        #~ self.acceler_brique = 0.001      ## Accélération quand on touche une brique
        self.acceler_raquette = 0.05
        #~ self.acceler_lv = 0.05       ## Accélération quand on change de lv
        ## Direction
        self.dirx = 1
        self.diry = -1
        self.normalise()            ## AVoir un vecteur vitesse de norme 1
        ## Dessin
        self.graph = self.canvas.create_oval(self.x-self.rayon , self.y+self.rayon , \
            self.x+self.rayon , self.y-self.rayon , width = 2 , fill = 'white')

    def redraw(self):
        """Redessine la balle à la nouvelle position"""
        self.canvas.coords(self.graph , self.x-self.rayon , \
            self.y-self.rayon , self.x+self.rayon , self.y+self.rayon)

    def deplace(self):
        """ Déplace la balle de v dans la direction (dirx , diry)"""
        self.x += self.dirx*self.vitesse
        self.y += self.diry*self.vitesse
        self.redraw()
    
    def accelere(self) :
        """Accélération à chaque contact"""
        self.vitesse += self.acceler_raquette

    ## Tests de Collisions
    ## -------------------
    ## Principe :
    ##      On regarde pour chaque "point cardinal" de la balle
    ##      s'il est dans un rectangle de test et si sa direction
    ##      est cohérente avec ce rectangle
    ##      Si oui ,  on change la direction de la balle
    ##      et éventuellement on l'accélère
    ##      On test également si la balle touche un coin

    def normalise(self):
        """Normalise le vecteur direction """
        hypo=sqrt(self.dirx**2+self.diry**2)
        if hypo != 0:
            self.dirx=self.dirx/hypo
            self.diry=self.diry/hypo

    def changedir(self,u,v):
        """Change la direction de la balle suivant le vecteur (u,v)
           de norme 1"""
        self.dirx = u
        self.diry = v
        self.normalise()
        #~ self.accelere()

    def test_haut(self , xa , ya , xb , yb):
        """ Test si la balle a un contact au dessus"""
        if ((xa <= self.x <= xb) and (ya <= self.y-self.rayon <= yb)) and self.diry<0:
            self.changedir(self.dirx,abs(self.diry))
            return True
        else:
            return False

    def test_bas(self , xa , ya , xb , yb):
        """ Test si la balle a un contact en dessous"""
        if (xa <= self.x <= xb) and (ya <= self.y+self.rayon <= yb) and self.diry>0 :
            self.changedir(self.dirx,-abs(self.diry))
            return True
        else:
            return False

    def test_gauche(self , xa , ya , xb , yb):
        """ Test si la balle a un contact à sa gauche"""
        if (xa <= self.x-self.rayon <= xb) and (ya <= self.y <= yb) and self.dirx<0 :
            self.changedir(abs(self.dirx),self.diry)
            return True
        else:
            return False

    def test_droite(self , xa , ya , xb , yb):
        """ Test si la balle a un contact à sa droite"""
        if (xa <= self.x+self.rayon <= xb) and (ya <= self.y <= yb)  and self.dirx>0:
            self.changedir(-abs(self.dirx),self.diry)
            return True
        else:
            return False

    def test_coins(self , xa , ya , xb , yb):
        """Test si la balle touche un coin du rectangle (xa,ya,xb,yb)"""
        ## Principe :
        ## ----------
        ## La balle est découpé en 8 secteurs d'angles pi/4,
        ## et on test si les coins de la bique sont dans ces quartiers
        ##
        ## Récupération des paramètres de la balle pour alléger les notations
        x=self.x        ## (x,y) : Coordonnées du centre de la balle
        y=-self.y       ## Passage dans un repère "normal"
        ya,yb=-ya,-yb   ## ie avec l'axe des ordonnées vers le haut
        r=self.rayon    ## (beaucoup plus pratique pour moi....)
        r2=r*sqrt(2)/2  ## r2=r*cos(pi/4)=r*sin(pi/4)

        ## Coins au dessus de la balle
        if        ( ((0 <= xa-x <= r*sqrt(2)/2) and (r2 <= yb-y <= r)) \
                or  ((-r2 <= xb-x <= 0) and (r2 <= yb-y <= r)) \
                or ( (yb-y>=xa-x)    and (0<=yb-y<=r2) and (0<=xa-x<=r2))\
                or ( (yb-y>=-(xb-x)) and (0<=yb-y<=r2) and (0<=xb-x<=r2)) )\
                and self.diry<0 :
            self.changedir(self.dirx, abs(self.diry))
            return True

        ## Coins en dessous de la balle
        elif      ( ((0 <= xa-x <= r2) and (-r <= ya-y <= -r2)) \
                or  ((-r2 <= xb-x <= 0) and (-r <= ya-y <= -r2)) \
                or ( (ya-y<=-(xa-x)) and (0>=ya-y>=-r2) and (0<=xa-x<=r2))\
                or ( (ya-y<=xb-x)    and (0>=ya-y>=-r2) and (0>=xb-x>=-r2)) )\
                and self.diry>0 :
            self.changedir(self.dirx, -abs(self.diry))
            return True

        ## Coins à gauche de la balle
        elif      ( ((-r <= xb-x <= -r2) and (0 <= yb-y <= r2)) \
                or  ((-r <= xb-x <= -r2) and (-r2 <= ya-y <= 0)) \
                or ( (yb-y<=-(xb-x)) and (0<=yb-y<=r2)  and (-r2<=xb-x<=0))\
                or ( (ya-y>=-(xb-x)) and (-r2<=ya-y<=0) and (-r2<=xb-x<=0)) )\
                and self.dirx<0 :
            self.changedir(abs(self.dirx), self.diry)
            return True

        ## Coins à droite de la balle
        elif      ( ((r2 <= xa-x <= r) and (0 <= yb-y <= r2)) \
                or ((r2 <= xa-x <= r) and (-r2 <= ya-y <= 0))\
                or ( (yb-y<=xa-x) and (0<=yb-y<=r2) and(0<=xa-x<=r2))\
                or ( (ya-y>=-(xa-x)) and (0>=ya-y>=-r2) and(0<=xa-x<=r2)) )\
                and self.dirx>0 :
            self.changedir(-abs(self.dirx),self.diry)
            return True
        else:
            return False

    def test_raquette_gauche(self,xa,ya,xb,yb):
        """ Test si la balle a un contact avec la raquette en dessous
            Idem test_bas + coin bas sauf pas de changement de direction
            qui se fait dans le prog principal
            (besoin des coordonnées de la balle)"""
        if       ( (ya <= self.y <= yb) and (xa <= self.x-self.rayon <= xb) \
                or ( ((0 <= ya-self.y <= self.rayon) and (-self.rayon <= self.x-xa <= 0 )) \
                or  ((-self.rayon <= yb-self.y <= 0) and (-self.rayon <= self.x-xa <= 0 )) ) )\
                and self.dirx<0 :
            self.accelere()
            return True
        else:
            return False
    
    def test_raquette_droite(self,xa,ya,xb,yb):
        """ Test si la balle a un contact avec la raquette en dessous
            Idem test_bas + coin bas sauf pas de changement de direction
            qui se fait dans le prog principal
            (besoin des coordonnées de la balle)"""
        if       ( (ya <= self.y <= yb) and (xa <= self.x+self.rayon <= xb) \
                or ( ((0 <= ya-self.y <= self.rayon) and (-self.rayon <= self.x-xa <= 0 )) \
                or  ((-self.rayon <= yb-self.y <= 0) and (-self.rayon <= self.x-xa <= 0 )) ) )\
                and self.dirx>0 :
            self.accelere()
            return True
        else:
            return False
 

class Application:
    """Programme principal"""
    def __init__(self , dimx = 1000 , dimy = 600):
        """Constructeur de l'interface"""

        ## Variables de jeu
        self.maxtiming = 2
        self.timing = self.maxtiming      ## Vitesse de la balle

        self.activekey = {}
        for k in ['Left', 'Up', 'Right', 'Down']:
            self.activekey[k] = False

        ## Variables globales de contôle
        self.fen = 0            ## 0: aucune fenetre n'est ouverte
        self.lance = 0          ## 0: La balle est arêtée ,  1: Elle est lancée
        self.pause = 0               ## 0: Le jeu n'est pas en pause ,  1:Pause
        self.pos_init = 1          ## 1: Le jeu est en position initiale

        ## Création de la fenêtre de jeu et récupération des sous-objets
        self.dimx,self.dimy=dimx,dimy
        self.main=Fenetre(self,dimx , dimy )
        

        ## Création (instanciation) des objets du jeu
        self.raquettes = [0,0]
        self.creer_raquette(Raquette.GAUCHE,0)
        self.creer_raquette(Raquette.DROITE,1)
        self.creer_balle()

        ## Partir sur de bonnes bases
        self.main.root.update()
        self.newgame()
        


    def creer_raquette(self, position, player):
        """Construit la raquette"""
        self.raquettes[player] = Raquette(self.main.canvas , position)

    def creer_balle(self):
        """Construit la balle"""
        rayon = 15 ## Rayon de la balle
        x,y=self.dimx/2,self.dimy/2
        self.balle = Balle(self.main.canvas , x,y , rayon)



    def newgame(self):
        """ Lance une nouvelle partie"""
        self.reinit()
    
    def reinit(self):
        """Redessine un niveau complet"""
        ## Position de départ pour la raquette et la balle
        self.stop()


    def start(self , event):
        """Lance la balle ou met en pause/dépause"""
        if self.fen==1 :
            return
        self.pos_init = 0
        ## Si la balle est à l'arret (pause ou début du tableau)
        if self.lance == 0 :
            ## On informe qu'elle est lancée
            self.lance = 1
            ## On informe que le jeu n'est pas en pause
            self.pause = 0

            ## On lance la balle
            self.avance_balle()
            self.bouge_raquette()
        ## Sinon, si elle est lancée, on met le jeu en pause
        elif self.lance == 1 :
            self.lance = 0
            self.pause = 1

    def stop(self):
        """Stop la balle et remet raquette+balle à leur position d'origine"""
        ## La balle est arrêtée,
        ## le jeu n'est pas en pause et on est en position initiale
        self.lance = 0
        self.pause = 0
        self.pos_init = 1
        ## Raquette au point de départ
        for k in range(2):
            self.raquettes[k].x = self.raquettes[k].xdef
            self.raquettes[k].y = self.raquettes[k].ydef
            self.raquettes[k].redraw()
        
        self.balle.x = self.balle.xdef
        self.balle.y = self.balle.ydef
        self.balle.redraw()
        
        self.balle.vitesse = self.balle.vitesse_init
        
        ## Reinitialisation de la direction de la balle
        self.balle.dirx = 1.0                       ## Direction verticale aléatoire
        self.balle.diry = uniform(-1,1)             ## fait partie des choses à revoir
        self.balle.normalise()
        #~ self.balle.vitesse = self.balle.vitesse_lv



    def test_bords(self):
        """Test si la balle touche un bord de l'écran ou la raquette"""
        ## Test si la balle touche les bords du jeu
        tol=self.balle.vitesse+1
        self.balle.test_haut(0 , 0 , self.dimx , tol)
        #~ self.balle.test_droite(self.dimx-tol , 0 , self.dimx , self.dimy)
        #~ self.balle.test_gauche(0 , 0 , tol , self.dimy)
        self.balle.test_bas(0 , self.dimy-tol , self.dimx , self.dimy)
        self.test_raquette()


    def test_raquette(self):
        """Test si la balle rebodit surla raquette"""
        ## La direction de la balle dépend de la distance
        ## de son point de contact avec le milieu de la raquette
        ## Milieu : rebond horizontal, Extrémités : 45°
        if self.balle.test_raquette_gauche(self.raquettes[0].x-self.raquettes[0].largeur/2 , \
                self.raquettes[0].y-self.raquettes[0].longueur/2 , \
                self.raquettes[0].x+self.raquettes[0].largeur/2 , \
                self.raquettes[0].y+self.raquettes[0].longueur/2):

            self.balle.changedir(1.0,(self.balle.y-self.raquettes[0].y)/(self.raquettes[0].longueur/2))
        
        if self.balle.test_raquette_droite(self.raquettes[1].x-self.raquettes[1].largeur/2 , \
                self.raquettes[1].y-self.raquettes[1].longueur/2 , \
                self.raquettes[1].x+self.raquettes[1].largeur/2 , \
                self.raquettes[1].y+self.raquettes[1].longueur/2):
            self.balle.changedir(-1.0,(self.balle.y-self.raquettes[1].y)/(self.raquettes[1].longueur/2))


    def test_mort(self):
        """Test si la balle passe sous la raquette"""
        if self.balle.x<=0 or self.balle.x>=self.dimx :
            self.stop()
            self.reinit()

    def avance_balle(self):
        """Boucle de déplacement de la balle"""
        if self.lance == 1:
            ## On déplace la balle
            self.balle.deplace()
            ## On test alors les collisions avec les objets
            self.test_bords()
            #~ self.test_briques()
            self.test_mort()
            ## On boucle (récusrsion)
            self.main.root.after(self.timing , self.avance_balle)
    
    # Gestion des événements clavier
    def pressed(self,event):
        key = event.keysym
        if key in self.activekey:
            self.activekey[key] = True
     
    def released(self,event):
        key = event.keysym
        if key in self.activekey:
            self.activekey[key] = False
    
    def bouge_raquette(self):
        if self.lance == 1:
            if self.activekey['Down']:
                self.raquettes[0].deplace(1)
                self.raquettes[1].deplace(1)
            if self.activekey['Up']:
                self.raquettes[0].deplace(-1)
                self.raquettes[1].deplace(-1)
            self.main.root.after(5, self.bouge_raquette)
            
    def bonus_long(self,event):
        # Test d'un petit bonus
        self.raquettes[0].longueur*=2
        self.raquettes[0].redraw()

class Fenetre :
    def __init__(self , appli, dimx = 1000 , dimy = 600):
        """Constructeur de l'interface"""
        ## Classe Application qui invoque la fenêtre
        self.appli=appli

        ## Fenêtre de jeu
        self.main = tk.Tk()
        self.main.title("Arkapython")

        self.root=tk.Frame(self.main,bg='black')
        self.root.pack()
        
        ## Canvas
        self.dimx , self.dimy = dimx , dimy   ## Dimensions du canevas
        self.canvas = tk.Canvas(self.root , bg = 'black' , width = self.dimx , height = self.dimy)
        #~ self.canvas.grid(row = 2 , column = 1 , columnspan = 2 , \
            #~ padx = 5 , pady = 5)
        self.canvas.pack()
        self.canvas.bind_all('<Return>',self.appli.start)
        self.canvas.bind_all('a',self.appli.bonus_long)
        self.canvas.bind_all("<KeyPress>", self.appli.pressed)
        self.canvas.bind_all("<KeyRelease>", self.appli.released)
        
        
if __name__=="__main__":
    app = Application()
    app.main.root.mainloop()

    quit()

