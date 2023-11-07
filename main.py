import User
import MEC
import Static_2 as st
import random
import numpy as np

ITERATION_NUM=500
BASE_STATIONS_NUM=3
USERS_NUMBER=10


AVAILABLE_SYSTEM_BANDWIDTH=20000000 #Hz  (20MHz) 

#creazione del sistema
mec_List=[]
user_List=[]


for i in range(0,BASE_STATIONS_NUM):
    m=MEC.MEC()
    m.print_Mec()
    mec_List.append(m)

for i in range(0,USERS_NUMBER):
    u=User.User(random.randint(50,User.MAX_TOTAL_DATA_SIZE_KB))
    u.print_user()
    user_List.append(u)



#Creati Users e MECs del sistema

for i in range(0,ITERATION_NUM): #ciclo piu esterno che esegue l'algoritmo e immagazzina i dati
    total_users=len(user_List)
    
    ruin_result = st.Static.Ruin_Theory_for_User_association(mec_List,user_List)

    associated_users = np.where(ruin_result==1)

    for m in mec_List:
        m.buffer_size=MEC.BUFFER_SIZE_MB
    
    random_result = st.Static.Random_Association(mec_List,user_List)

    associated_users = np.where(random_result==1)



