import math
import numpy as np
import User
import random
import MEC

MIN_BUFFER_SIZE=50 #### minimo Kb di task richiesto da user

class Algorithms:
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
        assigned_users=[]
        unassignable=[]
        Unassigned_users=Users.copy()

        [u.create_preference_profile(MECs) for u in Unassigned_users]

        while True:  # I due for non sono più annidati.
            user_preference , unassignable  = Algorithms.update_user_profiles_preference(MECs,Unassigned_users)

            for i in range(0,len(MECs)): 
                m=MECs[i]
                MEC_proposers_queue=m.MEC_priority_queue(user_preference[i],Unassigned_users) #lista dei propositori ordinata secondo Jk_n

                while(not len(MEC_proposers_queue)==0):
                    selected_user=MEC_proposers_queue.pop() #li rimuove in automatico dalla lista
                    
                    if(m.buffer_size - selected_user.data_size>=MIN_BUFFER_SIZE):
                        m.associated_users.append(selected_user)
                        m.update_Buffer_Surplus()
                        X[i][Users.index(selected_user)] = 1
                        assigned_users.append(selected_user)

            Unassigned_users=list(set(Unassigned_users)-set(assigned_users))
            Unassigned_users=list(set(Unassigned_users)-set(unassignable))


            assigned_users.clear()
            unassignable.clear()

            if(len(Unassigned_users)==0 or Algorithms.get_MECs_buffer_available(MECs)<=MIN_BUFFER_SIZE*len(MECs)):
                print('Stop ruin')
                break

        tot_free_buffer=0
        for m in MECs:
            tot_free_buffer+=m.buffer_size
        used_resources=100-((tot_free_buffer*100)/(len(MECs)*MEC.BUFFER_SIZE_MB))
            
        return X,used_resources
    
    @staticmethod
    def update_user_profiles_preference(MECs,un_users):
        user_preference=np.zeros((len(MECs),len(un_users))) #(creo la matrice dei In_k)
        unassignabile=[]
        for u in un_users: 
            
            m=u.preference.pop()# usa il pop
            MEC_idx=m[0]
            if(len(u.preference)==0):
                unassignabile.append(u)
            user_idx=un_users.index(u)
            user_preference[MEC_idx][user_idx]=1

        return user_preference,unassignabile
    
    
    '''def Random_Association(MECs,Users):
        X=np.zeros((len(MECs),len(Users))) #creo la matrice di partenza per l'associazione

        for i in range(0,len(Users)):
            idx=np.random.randint(0,100)%(len(MECs))   
            if((MECs[idx].buffer_size - Users[i].data_size)>=MIN_BUFFER_SIZE):
                MECs[idx].associated_users.append(Users[i])
                #m.buffer_size -= selected_user.data_size #crea una funzione
                MECs[idx].update_Buffer_Surplus()
                X[idx][i] = 1

            if(Algorithms.get_MECs_buffer_available(MECs)<=User.MAX_TOTAL_DATA_SIZE_KB*len(MECs)):
                print('Stop random')
                break
        
        tot_free_buffer=0
        for m in MECs:
            tot_free_buffer+=m.buffer_size
        used_resources=100-((tot_free_buffer*100)/(len(MECs)*MEC.BUFFER_SIZE_MB))

        return X,used_resources'''
    
    def Random_Association(MECs,Users):
        X=np.zeros((len(MECs),len(Users))) #creo la matrice di partenza per l'associazione
        user_preference=np.zeros((len(MECs),len(Users)))
        for i in range(0,len(Users)):
            idx=np.random.randint(0,100)%(len(MECs))*random.getrandbits(1)
            user_preference[idx][i] = 1

        for m in range(0,len(MECs)):
            for j in range(0,len(Users)):
                if(user_preference[m][j]):
                    if(True): #random.getrandbits(1)
                        if((MECs[m].buffer_size - Users[j].data_size)>=MIN_BUFFER_SIZE):
                            MECs[m].associated_users.append(Users[j])
                            #m.buffer_size -= selected_user.data_size #crea una funzione
                            MECs[m].update_Buffer_Surplus()
                            X[m][j] = 1
                        else:
                            pass

            if(Algorithms.get_MECs_buffer_available(MECs)<=User.MAX_TOTAL_DATA_SIZE_KB*len(MECs)):
                print('Stop random')
                break
        
        tot_free_buffer=0
        for m in MECs:
            tot_free_buffer+=m.buffer_size
        used_resources=100-((tot_free_buffer*100)/(len(MECs)*MEC.BUFFER_SIZE_MB))

        return X,used_resources
    
    


    

    