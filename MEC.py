import random
import Position as p
import numpy as np
import math
from numpy import random

COMPUTATION_CAPACITY_HZ= 600000
BUFFER_SIZE_MB=1500
DATA_PROCESSING_RATE=1.2 #  E' LA COMPUTATION CAPACITY???? 1.2 è un valore casuale
REQUIRED_COMP_CAPACITY=10  #Mu0: è dato!
N_MEC=100


class MEC:
    def __init__(self,computation_capacity=COMPUTATION_CAPACITY_HZ,buffer_size=BUFFER_SIZE_MB):
        
        self.computation_capacity=computation_capacity
        self.buffer_size=buffer_size
        self.ID="MEC_Server_"+str(random.randint(0,N_MEC))
        self.pos=p.Position()

    def printPos(self):
        st="X:"+str(self.pos.x)+"  Y:"+str(self.pos.y)
        print(st)

    def setPos(self,x,y):
        self.pos.x=x
        self.pos.y=y

    def MEC_Random_queue(self,u_lst_preference,user_list):
        stack=[]

        for i in range(0,len(u_lst_preference)):
            if(u_lst_preference[i]==1):
                stack.append(user_list[i].copy())

        random.shuffle(stack) 
        
        return stack

    def MEC_priority_queue(self,u_lst_preference,user_list):
        stack=[]
        ruin_prob=self.get_Ruin_Probability()
        for i in range(0,len(u_lst_preference)):
            if(u_lst_preference[i]==1):
                stack.append(user_list[i]) # prima c'era .copy()

        stack.sort(key=lambda x: x.data_size/ruin_prob, reverse=True) # eq 17 
        
        return stack
    
    def get_Buffer_Surplus(self,X_mec,A): #ad "initial_surplus" ho inserito la buffer_size iniziale (totale) ovvero 1.5Mb
        #X-mec è la riga relativa al mec in questione
        interval=10 #secondi? E' il tau 
        premium_value=(DATA_PROCESSING_RATE*interval)/REQUIRED_COMP_CAPACITY 
        loss_process=np.dot(X_mec,A)
        
        buffer_surplus = BUFFER_SIZE_MB + premium_value - loss_process

    def get_Ruin_Probability(self):
        
        value=0
        n=10 # valre casuale, sarebbe 'n' della sommatoria
        for j in range(1,n+1):
            mu=COMPUTATION_CAPACITY_HZ
            mu_primo=6 #Valore casuale

            first_component=(pow((mu*self.C_(j)),j-1) /math.factorial(j-1))
            exponential = np.exp(-mu_primo*self.C_(j))
            second_component=self.C_(1)/self.C_(j)
            
            value += first_component * exponential * second_component
        return value

    def C_(self,mul=1):
        initial_surplus=BUFFER_SIZE_MB #?? sarebbe B(0)
        interval=10 #secondi? E' il tau 
        premium_value=(DATA_PROCESSING_RATE*interval)/REQUIRED_COMP_CAPACITY 
        
        res=initial_surplus + mul*premium_value
        return res

    def print_Mec(self):
        s=self.ID+"  data:"+str(self.buffer_size)+"  pos:"+str(self.pos.x)+","+str(self.pos.y)
        print(s)


