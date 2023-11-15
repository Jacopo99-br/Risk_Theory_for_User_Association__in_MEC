import User
import MEC
import Static_2 as st
import random
import numpy as np
import pickle

SIMULATION_RUNS=50

BASE_STATIONS_NUM=3
USERS_NUMBER=100


AVAILABLE_SYSTEM_BANDWIDTH=20000000 #Hz  (20MHz)


#questo ciclo va eseguito 500 volte e calcolato la media #SIMULATION_RUNS=500
ruin_mean=np.zeros((int(USERS_NUMBER/10),3))
random_mean=np.zeros((int(USERS_NUMBER/10),3))

for run in range(0,SIMULATION_RUNS):


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
        random.shuffle(mec_List)

        for j in range(0,i):
            u=User.User(random.randint(User.MIN_TOTAL_DATA_SIZE_KB,User.MAX_TOTAL_DATA_SIZE_KB-1))
            #u.print_user()
            user_List.append(u)
        random.shuffle(user_List)



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

    for n in range(0,len(proposed_)):
         ruin_mean[n][0]=proposed_[n][0]
         ruin_mean[n][1]+=proposed_[n][1]
         ruin_mean[n][2]+=proposed_[n][2]
         
         random_mean[n][0]=random_[n][0]
         random_mean[n][1]+=random_[n][1]
         random_mean[n][2]+=random_[n][2]



'''
print(proposed_)
print("\n\n")
print(random_)'''
ruin_mean[:,1:3]=(ruin_mean[:,1:3]/SIMULATION_RUNS)
random_mean[:,1:3]=(random_mean[:,1:3]/SIMULATION_RUNS)


with open('pickle_files/Ruin_.pkl','wb') as RuinRes_file:
    pickle.dump(ruin_mean,RuinRes_file)
with open('pickle_files/Random_.pkl','wb') as RandomRes_file:
    pickle.dump(random_mean,RandomRes_file)
