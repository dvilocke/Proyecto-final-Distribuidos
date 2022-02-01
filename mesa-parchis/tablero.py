import colorama
from colorama import Fore, Style

from ficha import Ficha


class Tablero():
    def __init__(self, dim = 7):
        self.dim = dim
        self.ended = False
        self.casillas = [[0 for i in range(dim)] for j in range(dim)]
        self.fichas = []
        
    def wipe(self):
        self.casillas = [[0 for i in range(self.dim)] for j in range(self.dim)]
        
    def interaction(self):
        for ficha in self.fichas:
            if ficha.inTurn:
                for comida in self.fichas:
                    if (not comida.inTurn) and comida.getPos() == ficha.getPos() and comida.color != ficha.color:
                        comida.sendToJail()
                        print(str(ficha.color) + " se comió a: " + str(comida.color))
                ficha.inTurn = 0
                
    def win(self):
        for ficha in self.fichas:
            if ficha.getPos() == (3,3):
                print("el ganador es " + ficha.color)
                self.ended = True
                
            
    def update(self):
        self.win()
        self.interaction()
        self.wipe()
        for ficha in self.fichas:
            self.casillas[ficha.x][ficha.y] = ficha.color
            
        self.prettyPrint()
            
    def prettyPrint(self):
        for casilla in self.casillas:
            for casillita in casilla:
                if(casillita == 1):
                    print(f"{Fore.BLUE}1  {Style.RESET_ALL}", end ='')
                elif(casillita == 2):
                    print(f"{Fore.YELLOW}2  {Style.RESET_ALL}", end ='')
                elif(casillita == 3):
                    print(f"{Fore.GREEN}3  {Style.RESET_ALL}", end ='')
                elif(casillita == 4):
                    print(f"{Fore.RED}4  {Style.RESET_ALL}", end ='')
                else:
                    print('0  ', end ='')
            print()
                    