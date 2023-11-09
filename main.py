import User
import MEC
import Static_2 as st
import random
import numpy as np
import pickle


BASE_STATIONS_NUM=3
USERS_NUMBER=200


AVAILABLE_SYSTEM_BANDWIDTH=20000000 #Hz  (20MHz)


proposed_=[]
random_=[]
for i in range(10,USERS_NUMBER+1,10):
    #creazione del sistema
    mec_List=[]
    user_List=[]
    used_resource=0 # in %

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
    ruin_result,used_resource = st.Static.Ruin_Theory_for_User_association(mec_List,user_List)
    associated_users = np.count_nonzero(ruin_result==1)
    print('ruin :'+str(associated_users))

    proposed_.append([i,associated_users,used_resource])

    for m in mec_List:
        m.buffer_size=MEC.BUFFER_SIZE_MB

    
    random_result,used_resource = st.Static.Random_Association(mec_List,user_List)
    associated_users = np.count_nonzero(random_result==1)
    print('random :'+str(associated_users))


    random_.append([i,associated_users,used_resource])

    for m in mec_List:
        m.buffer_size=MEC.BUFFER_SIZE_MB

'''
print(proposed_)
print("\n\n")
print(random_)'''

with open('pickle_files/Ruin_.pkl','wb') as RuinRes_file:
        pickle.dump(proposed_,RuinRes_file)
with open('pickle_files/Random_.pkl','wb') as RandomRes_file:
    pickle.dump(random_,RandomRes_file)
