import os
import random

from ficha import Ficha
from tablero import Tablero

t = Tablero()
for i in range(4):
    f = Ficha()
    f.color = i+1
    f.setStart()
    f.setSequence()
    t.fichas.append(f)
    
t.update()
input('start')
os.system('cls')

while not t.ended:
    for f in t.fichas:
        print('turno de ' + str(f.color))
        dado = random.randrange(1, 5)
        print('dado '+str(dado))
        f.move(dado)
        t.update()
        input()
        os.system('cls')
        