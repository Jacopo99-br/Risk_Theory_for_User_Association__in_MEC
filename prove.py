import numpy as np
import random
from operator import itemgetter
'''for seq in range(10,1000+1,10):
    print(seq)'''
'''
l=[5,45,18,69,58,78,2]
l.sort()
l.pop()
l.append([8,9])
print(l)'''

class Pio:
    dato=None

    def metti_dato(self):
        self.dato=5

l=[]
for i in range(0,5):
    l.append(Pio())

map(lambda x: x.metti_dato(), l)

print(l[0].dato)