import random
import Position as p
import math
import Static_2 as st


MAX_TOTAL_DATA_SIZE_KB= 100
MIN_TOTAL_DATA_SIZE_KB= 10
COMPUTATION_CAPACITY_HZ= 70000
UPLINK_TRASMISSION_CAPACITY_MW= 200 #mW
N_USER=1000
SYSTEM_BACKGROUND_NOISE=-174 # dBm/Hz


class User:
    def __init__(self,data_size=MAX_TOTAL_DATA_SIZE_KB,computation_capacity=COMPUTATION_CAPACITY_HZ,uplink_trasmission_capacity=UPLINK_TRASMISSION_CAPACITY_MW):
        
        self.data_size=data_size
        self.computation_capacity=computation_capacity
        self.uplink_trasmission_capacity=uplink_trasmission_capacity
        self.ID="User_"+str(random.randint(0,N_USER))
        self.pos=p.Position()
        self.preference=None

    def printPos(self):
        s="X:"+str(self.pos.x)+"  Y:"+str(self.pos.y)
        print(s)

    def setPos(self,x,y):
        self.pos.x=x
        self.pos.y=y

    def user_preference_profile(self,MEC_List):
        preference_value=0
        x=0
        for i in range(0,len(MEC_List)):
            ch_gain = st.Static.getDistance(self.pos,MEC_List[i].pos)  #channel gain basato solo sulla distanza dal MEC, da rivedere!
            value= ((UPLINK_TRASMISSION_CAPACITY_MW * ch_gain) / 10) * MEC_List[i].buffer_size #era diviso SYSTEM BACKGROUND NOISE, cambiato per fare prove

            if(value>preference_value):
                x=i
                preference_value=value

        self.preference=MEC_List[x]
        return x
    
    def user_random_preference(self,MECs):
        idx=random.randint(0,len(MECs)-1)
        return idx


    def print_user(self):
        s=self.ID+"  data:"+str(self.data_size)+"  pos:"+str(self.pos.x)+","+str(self.pos.y)
        print(s)

