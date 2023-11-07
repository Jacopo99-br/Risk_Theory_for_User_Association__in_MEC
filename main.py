import User
import MEC
import Static_2 as st
import random
import numpy as np


BASE_STATIONS_NUM=3
USERS_NUMBER=200


AVAILABLE_SYSTEM_BANDWIDTH=20000000 #Hz  (20MHz) 
for i in range(10,USERS_NUMBER+1,10):
    #creazione del sistema
    mec_List=[]
    user_List=[]


    for j in range(0,BASE_STATIONS_NUM):
        m=MEC.MEC()
        #m.print_Mec()
        mec_List.append(m)

    for j in range(0,i):
        u=User.User(random.randint(User.MIN_TOTAL_DATA_SIZE_KB,User.MAX_TOTAL_DATA_SIZE_KB-1))
        #u.print_user()
        user_List.append(u)



    #Creati Users e MECs del sistema

    
    total_users=len(user_List)
    print('total:'+str(total_users))
    
    ruin_result = st.Static.Ruin_Theory_for_User_association(mec_List,user_List)

    associated_users = np.count_nonzero(ruin_result==1)
    print('ruin :'+str(associated_users))

    for m in mec_List:
        m.buffer_size=MEC.BUFFER_SIZE_MB
    
    random_result = st.Static.Random_Association(mec_List,user_List)

    associated_users = np.count_nonzero(random_result==1)
    print('random :'+str(associated_users))
    for m in mec_List:
        m.buffer_size=MEC.BUFFER_SIZE_MB



