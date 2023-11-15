import random
import Position as p
import numpy as np
import math
from numpy import random
import User

COMPUTATION_CAPACITY_HZ= 600000
CYCLES_FOR_1_BIT=10 # mu_zero
INTERVAL=0.01 # in sec   : MAX accomplished deadline
DATA_BIT=10 # KB

BUFFER_SIZE_MB=1500  #KB
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
                stack.append(user_list[i])

        random.shuffle(stack) 
        
        return stack

    def MEC_priority_queue(self,u_lst_preference,user_list,n_users):
        stack=[]
        ruin_prob=self.get_Ruin_Probability(n_users)
        for i in range(0,len(u_lst_preference)):
            if(u_lst_preference[i]==1):
                stack.append(user_list[i]) # prima c'era .copy()

        stack.sort(key=lambda x: x.data_size/ruin_prob, reverse=True) # eq 17 metto reverse=True perchè facendo il pop 
        #esce quello con valore più basso
        
        return stack
    
    '''def get_Buffer_Surplus(self,X_mec,A): #ad "initial_surplus" ho inserito la buffer_size iniziale (totale) ovvero 1.5Mb
        #X-mec è la riga relativa al mec in questione
        interval=10 #secondi? E' il tau 
        premium_value=(DATA_PROCESSING_RATE*interval)/REQUIRED_COMP_CAPACITY 
        loss_process=np.dot(X_mec,A)
        
        buffer_surplus = BUFFER_SIZE_MB + premium_value - loss_process'''

    def get_Ruin_Probability(self,n_users):
        
        if(n_users>0): # ha degli utenti associati
            value=0
            n=n_users # numero degli utenti già connessi al MEC in questione 
            for j in range(1,n+1):
                mu=1
                first_component=(pow((mu*self.C_(j)),j-1) /math.factorial(j-1))
                exponential = np.exp(-mu*self.C_(j)) #c'era un - a sx di mu_primo
                second_component=self.C_(1)/self.C_(j)
                
                value += first_component * exponential * second_component
            if value==0:
                print('ruin = 0')
                value=1
            #print('n_users='+str(n)+'   buffer_free:'+str(self.buffer_size)+'   val:'+str(value))
            return value
        else:
            return 1

    def C_(self,mul=1):
        #initial_surplus=self.buffer_size #?? sarebbe B(0)
        initial_surplus=BUFFER_SIZE_MB #?? sarebbe B(0)
        n_CPU_CYCL=(User.MAX_TOTAL_DATA_SIZE_KB/DATA_BIT)*CYCLES_FOR_1_BIT # num_bit approssimativi per ogni user * cicli per 1 bit

        premium_value=(n_CPU_CYCL*INTERVAL)/CYCLES_FOR_1_BIT 
        
        res=initial_surplus + mul*premium_value
        return res

    def print_Mec(self):
        s=self.ID+"  data:"+str(self.buffer_size)+"  pos:"+str(self.pos.x)+","+str(self.pos.y)
        print(s)


