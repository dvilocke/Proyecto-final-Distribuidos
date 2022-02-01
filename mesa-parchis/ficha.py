from math import sqrt

turn_pontis = [
    (0,2), (2,2), (2,0),
    (4,0), (4,2), (6,2),
    (6,4), (4,4), (4,6),
    (2,6), (2,4), (0,4),
]

end_points = [
    (0,3),
    (3,0),
    (6,3),
    (3,6)
]

jails = [
    (0,0), (0,1), (1,0), (1,1),
    (5,0), (5,1), (6,0), (6,1),
    (5,5), (5,6), (6,5), (6,6),
    (0,5), (0,6), (1,5), (1,6)
]

starts = [
    (1,2),
    (4,1),
    (5,4),
    (2,5),
]

goal = (3,3)

dirs = {
    'S':(0,0),
    'R':(0,1),
    'L':(0,-1),
    'U':(-1,0),
    'D':(1,0)
}

class Ficha():
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.lap = 0
        self.color = 1
        self.inTurn = 0
        self.inJail = False
        
    def setStart(self):
        self.x, self.y = starts[self.color-1]
        
    def getPos(self):
        return (self.x, self.y)
        
    def setSequence(self):
        self.seqStep = 0
        if self.color == 1:
            self.seq = ('D', 'L', 'D', 'R', 'D', 'R', 'U', 'R', 'U', 'L', 'U', 'L', 'D')
        elif self.color == 2:
            self.seq = ('R', 'D', 'R', 'U', 'R', 'U', 'L', 'U', 'L', 'D', 'L', 'D', 'R')
        elif self.color == 3:
            self.seq = ('U', 'R', 'U', 'L', 'U', 'L', 'D', 'L', 'D', 'R', 'D', 'R', 'U')
        elif self.color == 4:
            self.seq = ('L', 'U', 'L', 'D', 'L', 'D', 'R', 'D', 'R', 'U', 'R', 'U', 'L')
            
    def shiftSeq(self):
        self.seqStep = (self.seqStep + 1) % len(self.seq)
        
    def sendToJail(self):
        self.inJail = True
        self.setSequence()
        if self.color == 1:
            self.x = 0
            self.y = 0
        elif self.color == 2:
            self.x = 5
            self.y = 0
        elif self.color == 3:
            self.x = 5
            self.y = 5
        elif self.color == 4:
            self.x = 0
            self.y = 5
            
    def scapeJail(self):
        print(str(self.color) + ' escapo de la carcel')
        self.inJail = False
        if self.color == 1:
            self.x = 1
            self.y = 2
        elif self.color == 2:
            self.x = 4
            self.y = 1
        elif self.color == 3:
            self.x = 5
            self.y = 4
        elif self.color == 4:
            self.x = 2
            self.y = 5
            
    def endTurn(self):
        self.inTurn = 0
        
    def step(self):
        if (self.x, self.y) not in jails:
            self.inTurn = 1
            self.x = self.x + dirs[self.seq[self.seqStep]][0]
            self.y = self.y + dirs[self.seq[self.seqStep]][1]
            if (self.x, self.y) in turn_pontis:
                self.shiftSeq()
            if (self.x, self.y) == end_points[self.color-1]:
                print(str(self.color) + ' llegó a su meta')
                print()
                self.shiftSeq()
                self.lap = 1
                
    def move(self, steps):
        if not self.inJail:
            if self.lap:
                deltaX = self.getPos()[0]-3
                deltaY = self.getPos()[1]-3
                distancia = sqrt(deltaX**2 + deltaY**2)
                if distancia >= steps:
                    for _ in range(steps):
                        self.step()
            else:       
                for _ in range(steps):
                    self.step()
        else:
            if steps == 4:
                self.scapeJail()