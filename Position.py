import random as r

MAX_X_M=5000
MAX_Y_M=5000

class Position:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __init__(self):
        self.x=r.randint(0,MAX_X_M)
        self.y=r.randint(0,MAX_Y_M)