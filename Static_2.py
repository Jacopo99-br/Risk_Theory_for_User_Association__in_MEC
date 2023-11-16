import math
import numpy as np
import User
import random
import MEC

MIN_BUFFER_SIZE=50 #### minimo Kb di task richiesto da user
#Però cosi non va in loop infinito nel while dei MEC

class Static:
    @staticmethod
    def getDistance(pos1,pos2):
        distance=math.sqrt((pos1.x-pos2.x)**2 + (pos1.y-pos2.y)**2)
        return distance
    
    @staticmethod
    def get_MECs_buffer_available(MECs):
        res=0
        for m in MECs: res+=m.buffer_size
        return res


    @staticmethod
    def Ruin_Theory_for_User_association(MECs,Users):
        X=np.zeros((len(MECs),len(Users))) #creo la matrice di partenza per l'associazione
        #A=np.zeros(len(Users)) #creo la matrice di partenza per i dati
        assigned_users=[]
        unassignable=[]
        Unassigned_users=Users.copy()

        #Unassigned_users[:].create_preference_profile(MECs)
        [u.create_preference_profile(MECs) for u in Unassigned_users]

        while True:  # I due for non sono più annidati.
            user_preference , unassignable = Static.update_user_profiles_preference(MECs,Unassigned_users)

            for i in range(0,len(MECs)): 
                m=MECs[i]
                m_associated=np.count_nonzero(X[i]==1)
                MEC_proposers_queue=m.MEC_priority_queue(user_preference[i],Unassigned_users,m_associated) #lista dei propositori ordinata secondo Jk_n

                #while(not len(MEC_proposers_queue)==0 and m.buffer_size>= MIN_BUFFER_SIZE):
                while(not len(MEC_proposers_queue)==0):
                    selected_user=MEC_proposers_queue.pop() #li rimuove in automatico dalla lista
                    
                    if(m.buffer_size - selected_user.data_size>=MIN_BUFFER_SIZE):
                        m.buffer_size -= selected_user.data_size

                        X[i][Users.index(selected_user)] = 1
                        assigned_users.append(selected_user)

            Unassigned_users=list(set(Unassigned_users)-set(assigned_users))
            Unassigned_users=list(set(Unassigned_users)-set(unassignable))

            assigned_users.clear()
            unassignable.clear()

            if(len(Unassigned_users)==0 or Static.get_MECs_buffer_available(MECs)<=User.MAX_TOTAL_DATA_SIZE_KB):
                print('Stop ruin')
                break

        tot_free_buffer=0
        for m in MECs:
            tot_free_buffer+=m.buffer_size
        used_resources=((tot_free_buffer*100)/(len(MECs)*MEC.BUFFER_SIZE_MB))
            
        return X,used_resources
    
    @staticmethod
    def update_user_profiles_preference(MECs,un_users):
        user_preference=np.zeros((len(MECs),len(un_users))) #(creo la matrice dei In_k)
        unassignabile=[]
        for u in un_users: 
            
            MEC_idx=u.preference.pop()[0]# usa il pop
            if(len(u.preference)==0):
                unassignabile.append(u)
            user_idx=un_users.index(u)
            user_preference[MEC_idx][user_idx]=1

        return user_preference,unassignabile
    
    @staticmethod
    def Random_Association(MECs,Users):
        X=np.zeros((len(MECs),len(Users))) #creo la matrice di partenza per l'associazione
        Unassigned_users=Users.copy()
        random.shuffle(Unassigned_users)

        for u in range(0,len(Unassigned_users)):
            idx=np.random.randint(0,len(MECs))
            if((MECs[idx].buffer_size - Unassigned_users[u].data_size)>=MIN_BUFFER_SIZE):
                MECs[idx].buffer_size -= Unassigned_users[u].data_size

                X[idx][u] = 1

            if(Static.get_MECs_buffer_available(MECs)<=User.MAX_TOTAL_DATA_SIZE_KB*len(MECs)):
                print('Stop random')
                break
        
        tot_free_buffer=0
        for m in MECs:
            tot_free_buffer+=m.buffer_size
        used_resources=((tot_free_buffer*100)/(len(MECs)*MEC.BUFFER_SIZE_MB))
        if(len(Users)==200):
            print('finale')

        return X,used_resources
    


    

    