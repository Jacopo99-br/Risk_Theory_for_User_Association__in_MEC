import matplotlib.pyplot as plt
import pickle
import numpy as np
Ruin_=np.array(pickle.load(open("pickle_files\Ruin_.pkl","rb")))
Random_=np.array(pickle.load(open("pickle_files\Random_.pkl","rb")))

legend=["Proposed","Ranodm"]
######################### %utenti associati

fig=plt.figure(1)
plt.style.use('ggplot')

ax=fig.gca()
ax.set_ylim([0,100])
ax.set_ylabel('Assigned Users (%)')
ax.set_xlabel('Users')
x=Ruin_[:,:1]
y_ruin=(Ruin_[:,1:2]*100)/x
y_random=(Random_[:,1:2]*100)/x

plt.plot(x,y_random)
plt.plot(x,y_ruin)

plt.legend(legend)

############### % risorse utilizzate

fig=plt.figure(2)
plt.style.use('ggplot')

ax=fig.gca()

ax.set_ylim([0,100])
ax.set_ylabel('Non-Used resources (%)')
ax.set_xlabel('Users')
x=Ruin_[:,:1]
y_ruin=Ruin_[:,2:3]
y_random=Random_[:,2:3]

#print(x)
print(y_ruin)
#print(y_random)

plt.plot(x,y_random)
plt.plot(x,y_ruin)
plt.legend(legend)

plt.show()
