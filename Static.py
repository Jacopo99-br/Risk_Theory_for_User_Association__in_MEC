import math
import numpy as np

MIN_BUFFER_SIZE=0.005 ############# Valore casuale da rivedere

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
    def Ruin_Theory(MECs,Users):
        X=np.zeros((MECs.len(),Users.len())) #creo la matrice di partenza per l'associazione
        A=np.zeros((Users.len())) #creo la matrice di partenza per 
        assigned_users=[]
        while True:
            for u in Users:

                u.user_preference_profile(MECs)
                u_preference_MEC=u.preference 
                A=

                #prende il MEC migliore e propone l'associazione: l'aggiunge alla lista di chi si propone per l'associazione con quel MEC
                for m in MECs:

                    MEC_proposers_queue=m.MEC_priority_queue()

                    while(not MEC_proposers_queue.isempty() or m.buffer_size>= MIN_BUFFER_SIZE):

                        selected_user=MEC_proposers_queue.pop()
                        m.buffer_size -= selected_user.data_size
                        MEC_proposers_queue.remove(selected_user)
                        assigned_users.append(selected_user) # controllare metodo per numpy
                        #update X[selected user,m] fai una funzione in Static
                    
                    Users.remove(assigned_users)
                    for user in Users: user.user_preference_profile()
            
            if(Users.isempty() or Static.get_MECs_buffer_available(MECs)<=MIN_BUFFER_SIZE):
                break

    