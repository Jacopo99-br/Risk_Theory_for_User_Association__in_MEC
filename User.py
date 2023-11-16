import random
import Position as p
import numpy as np
import math
import Static_2 as st
from operator import itemgetter



MAX_TOTAL_DATA_SIZE_KB= 100
MIN_TOTAL_DATA_SIZE_KB= 50
COMPUTATION_CAPACITY_HZ= 70000
UPLINK_TRASMISSION_CAPACITY_MW= 200 #mW
N_USER=1000
SYSTEM_BACKGROUND_NOISE= 10.0**(-17.4) #in mW    #-174 # dBm/Hz


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

    def create_preference_profile(self,MEC_List):
        profile=[]
        for i in range(0,len(MEC_List)):
            profile.append([i,self.get_SNR(MEC_List[i])])

        self.preference=sorted(profile, key=itemgetter(1))

    def get_SNR(self,MEC):
        reference_dis=1000 # in m
        dist=st.Static.getDistance(self.pos,MEC.pos)
        antenna_gain=10
        reciver_height=30 #m
        ref_dist_path_loss=40*np.log10(reference_dis)-10*np.log10(antenna_gain*math.pow(reciver_height,2))
        p_l_exponent=6
        path_loss=ref_dist_path_loss+10*p_l_exponent*np.log10(dist/reference_dis) + np.random.rayleigh() #in db
        ch_gain=10.0**(-path_loss/10.0)

        SNR= 10*np.log10((UPLINK_TRASMISSION_CAPACITY_MW * ch_gain) / SYSTEM_BACKGROUND_NOISE)  # SNR in dB

        return SNR

    def print_user(self):
        s=self.ID+"  data:"+str(self.data_size)+"  pos:"+str(self.pos.x)+","+str(self.pos.y)
        print(s)

