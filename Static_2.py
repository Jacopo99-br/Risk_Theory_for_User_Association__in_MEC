import math
import numpy as np
import User

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
        Unassigned_users=Users.copy()

        while True:  # I due for non sono più annidati.
            user_preference = Static.update_user_profiles_preference(MECs,Unassigned_users)
                

            #prende il MEC migliore e propone l'associazione: l'aggiunge alla lista di chi si propone per l'associazione con quel MEC
            for i in range(0,len(MECs)):
                m=MECs[i]
                MEC_proposers_queue=m.MEC_priority_queue(user_preference[i],Unassigned_users) #lista dei propositori ordinata secondo Jk_n

                #while(not len(MEC_proposers_queue)==0 and m.buffer_size>= MIN_BUFFER_SIZE):
                while(not len(MEC_proposers_queue)==0):
                    selected_user=MEC_proposers_queue.pop() #li rimuove in automatico dalla lista
                    
                    if(m.buffer_size-selected_user.data_size>=MIN_BUFFER_SIZE):
                        m.buffer_size -= selected_user.data_size

                        X[i][Users.index(selected_user)] = 1
                        assigned_users.append(selected_user) 
                
                for user in assigned_users:
                    Unassigned_users.remove(user)
                assigned_users.clear()
                user_preference=Static.update_user_profiles_preference(MECs,Unassigned_users)
            print('Before if ruin')
            if(len(Unassigned_users)==0 or Static.get_MECs_buffer_available(MECs)<=User.MAX_TOTAL_DATA_SIZE_KB*len(MECs)):
                print('Stop ruin')
                break
        
        return X
    
    @staticmethod
    def update_user_profiles_preference(MECs,un_users):
        user_preference=np.zeros((len(MECs),len(un_users))) #(creo la matrice dei In_k)
        for u in un_users: #primo ciclo per determinare le preferenze degli utenti non ancora assegnati 
            MEC_idx=u.user_preference_profile(MECs)
            user_idx=un_users.index(u)
            user_preference[MEC_idx][user_idx]=1
        
        return user_preference
    
    @staticmethod
    def update_userRandom_profiles_preference(MECs,un_users):
        user_preference=np.zeros((len(MECs),len(un_users))) #(creo la matrice dei In_k)
        for u in un_users: #primo ciclo per determinare le preferenze degli utenti non ancora assegnati 
            MEC_idx=u.user_random_preference(MECs)
            user_idx=un_users.index(u)
            user_preference[MEC_idx][user_idx]=1
        
        return user_preference
    
    @staticmethod
    def Random_Association(MECs,Users):
        X=np.zeros((len(MECs),len(Users))) #creo la matrice di partenza per l'associazione
        assigned_users=[]
        Unassigned_users=Users.copy()

        while True:  # I due for non sono più annidati.

            user_preference = Static.update_userRandom_profiles_preference(MECs,Unassigned_users)
                

            #prende il MEC migliore e propone l'associazione: l'aggiunge alla lista di chi si propone per l'associazione con quel MEC
            for i in range(0,len(MECs)):
                m=MECs[i]
                MEC_proposers_queue=m.MEC_Random_queue(user_preference[i],Unassigned_users) #lista dei propositori ordinata secondo Jk_n

                while(not len(MEC_proposers_queue)==0 ):

                    selected_user=MEC_proposers_queue.pop() #li rimuove in automatico dalla lista
                    if(m.buffer_size-selected_user.data_size>=MIN_BUFFER_SIZE):
                        m.buffer_size -= selected_user.data_size

                        X[i][Users.index(selected_user)] = 1
                        assigned_users.append(selected_user) 
                
                for user in assigned_users:
                    Unassigned_users.remove(user)
                assigned_users.clear()
                user_preference=Static.update_userRandom_profiles_preference(MECs,Unassigned_users)
            print('before if Random')
            if(len(Unassigned_users)==0 or Static.get_MECs_buffer_available(MECs)<=User.MAX_TOTAL_DATA_SIZE_KB*len(MECs)):
                print('Stop Random')
                break
        
        return X
    


    

    