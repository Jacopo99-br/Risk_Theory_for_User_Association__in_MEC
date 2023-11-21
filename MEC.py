import random
import Position as p
import numpy as np
import math
from numpy import random

COMPUTATION_CAPACITY_GHZ=0.0006 # era 6*10^5 Hz
CYCLES_FOR_1_MB=10*8*10**(6) # mu_zero 
INTERVAL=0.01 # in sec   : MAX accomplished deadline
AVAILABLE_SYSTEM_BANDWIDTH=0.02 #GHz  (20MHz)

BUFFER_SIZE_MB=1500  #KB
DATA_PROCESSING_RATE=1.2 #  E' LA COMPUTATION CAPACITY???? 1.2 è un valore casuale
REQUIRED_COMP_CAPACITY=10  #Mu0: è dato!
N_MEC=100


class MEC:
    def __init__(self,computation_capacity=COMPUTATION_CAPACITY_GHZ,buffer_size=BUFFER_SIZE_MB,id_=0):
        
        self.computation_capacity=computation_capacity
        self.buffer_size=buffer_size
        self.id_=id_
        self.ID="MEC_Server_"+str(id_)
        self.pos=p.Position()
        self.associated_users=[]
        #self.queue=BUFFER_SIZE_MB/1000
        self.queue=0

    def printPos(self):
        st="X:"+str(self.pos.x)+"  Y:"+str(self.pos.y)
        print(st)

    def setPos(self,x,y):
        self.pos.x=x
        self.pos.y=y

    def MEC_priority_queue(self,u_lst_preference,user_list):
        stack=[]
        ruin_prob=self.get_Ruin_Probability()
        for i in range(0,len(u_lst_preference)):
            if(u_lst_preference[i]==1):
                stack.append(user_list[i]) # prima c'era .copy()

        stack.sort(key=lambda x: x.data_size/ruin_prob, reverse=True) # eq 17 metto reverse=True perchè facendo il pop 
        #esce quello con valore più basso
        
        return stack

    def get_Ruin_Probability(self):
        
        if(self.associated_users): # ha degli utenti associati
            value=0
            n=len(self.associated_users) # numero degli utenti già connessi al MEC in questione 
            for j in range(1,n+1):
                mu=9.5
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
        # ho convertito tutto in Mb
        initial_surplus=BUFFER_SIZE_MB/1000 #in MB
        n_CPU_CYCL=COMPUTATION_CAPACITY_GHZ/mul  # distribuito equamente per gli utenti associati. Da Task migration... eq.3
        #cosi torna che mi renda il valore in MB
        premium_value=(n_CPU_CYCL*INTERVAL)/(CYCLES_FOR_1_MB)
        
        res=initial_surplus + mul*premium_value
        return res
    

    def get_buffer_queue(self):
        n_CPU_CYCL=COMPUTATION_CAPACITY_GHZ/len(self.associated_users)
        premium_value=(n_CPU_CYCL*INTERVAL)/(CYCLES_FOR_1_MB)
        self.queue=max(self.queue-premium_value,0) + self.get_user_uplink_data_rate()
        print('queue')

    def get_user_uplink_data_rate(self):
        rate_sum=0
        n_users=len(self.associated_users)
        for u in self.associated_users:
            SNR=u.SNR_list[self.id_][1]
            rate=(AVAILABLE_SYSTEM_BANDWIDTH/n_users)*np.log2(1+SNR)
            rate_sum += INTERVAL*rate
        return rate_sum
        

    def print_Mec(self):
        s=self.ID+"  data:"+str(self.buffer_size)+"  pos:"+str(self.pos.x)+","+str(self.pos.y)
        print(s)


