import math
import numpy as np

MIN_BUFFER_SIZE=1000 ############# Valore casuale da rivedere

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
            user_preference=np.zeros((len(MECs),len(Unassigned_users))) #(creo la matrice dei In_k)
            for u in Unassigned_users: #primo ciclo per determinare le preferenze degli utenti non ancora assegnati 
                MEC_idx=u.user_preference_profile(MECs)
                user_idx=Unassigned_users.index(u)
                user_preference[MEC_idx][user_idx]=1
                

            #prende il MEC migliore e propone l'associazione: l'aggiunge alla lista di chi si propone per l'associazione con quel MEC
            for i in range(0,len(MECs)):
                m=MECs[i]
                MEC_proposers_queue=m.MEC_priority_queue(user_preference[i],Unassigned_users) #lista dei propositori ordinata secondo Jk_n

                while(not len(MEC_proposers_queue)==0 or m.buffer_size>= MIN_BUFFER_SIZE):

                    selected_user=MEC_proposers_queue.pop() #li rimuove in automatico dalla lista
                    m.buffer_size -= selected_user.data_size

                    X[i][Users.index(selected_user)] = 1
                    assigned_users.append(selected_user) 
                
                Unassigned_users.remove(assigned_users)
            
            if(len(Unassigned_users)==0 or Static.get_MECs_buffer_available(MECs)<=MIN_BUFFER_SIZE):
                break
        
        return X
    
    @staticmethod
    def Random_Association(MECs,Users):
        X=np.zeros((len(MECs),len(Users))) #creo la matrice di partenza per l'associazione
        assigned_users=[]
        Unassigned_users=Users.copy()

        while True:  # I due for non sono più annidati.
            user_preference=np.zeros((len(MECs),len(Unassigned_users))) #(creo la matrice dei In_k)
            for u in Unassigned_users: #primo ciclo per determinare le preferenze degli utenti non ancora assegnati 
                MEC_idx=u.user_random_preference(len(MECs))
                user_idx=Unassigned_users.index(u)
                user_preference[MEC_idx][user_idx]=1
                

            #prende il MEC migliore e propone l'associazione: l'aggiunge alla lista di chi si propone per l'associazione con quel MEC
            for i in range(0,len(MECs)):
                m=MECs[i]
                MEC_proposers_queue=m.MEC_Random_queue(user_preference[i],Unassigned_users) #lista dei propositori ordinata secondo Jk_n

                while(not MEC_proposers_queue.isempty() or m.buffer_size>= MIN_BUFFER_SIZE):

                    selected_user=MEC_proposers_queue.pop() #li rimuove in automatico dalla lista
                    m.buffer_size -= selected_user.data_size

                    X[i][Users.index(selected_user)] = 1
                    assigned_users.append(selected_user) 
                
                Unassigned_users.remove(assigned_users)
            
            if(Unassigned_users.isempty() or Static.get_MECs_buffer_available(MECs)<=MIN_BUFFER_SIZE):
                break
        
        return X

    

    