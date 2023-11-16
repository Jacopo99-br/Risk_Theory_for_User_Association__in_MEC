import random as r
import numpy as np

MAX_X_M=5000 #m
MAX_Y_M=5000 #m

class Position:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __init__(self):
        '''self.x=r.randint(0,MAX_X_M)
        self.y=r.randint(0,MAX_Y_M)'''
        self.x=np.random.randint(0,MAX_X_M)
        self.y=np.random.randint(0,MAX_Y_M)


