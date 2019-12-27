import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.lines as mlines
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.collections import LineCollection
import math
import sys
import pdb

#################################################################
#### Explore tree constructed using make_tree.py
#### author: Nilin
#################################################################

name=input("\n Load tree from file (exclude .npy): ")
[dims,paths]=np.load(name+".npy",allow_pickle=True)

dim="3d"
if(dims[2]==1):
    dim="2d"
print("_"*100+"\n")


#### N[DO(v)] is the set of neighbors of v.
#### DO=dictionary order
N=[[]]*dims[0]*dims[1]*dims[2]
DO=lambda v:int(v[0]*dims[1]*dims[2]+v[1]*dims[2]+v[2])

for path in paths:
    for t in range(1,len(path)):
        v,w=(path[t-1],path[t])
        N[DO(v)]=N[DO(v)]+[w]
        N[DO(w)]=N[DO(w)]+[v]

def growfrom(v):
    V=-1*np.ones(dims)
    S=[v]
    Spheres=[]
    Normals=[]
    t=0
    while(len(S)>0):
        Spheres=Spheres+[S]
        S_new=[]
        Nor=[]
        for v in S:
            for w in N[DO(v)]:
                if V[w]==-1:
                    V[w]=t
                    S_new=S_new+[w]
                Nor=Nor+[(v,w)]
        Normals=Normals+[Nor]
        S=S_new
        t=t+1

    R=len(Spheres)

    area=[len(S) for S in Spheres]
    volume=[0 for i in range(R)]
    vol=0
    for i in range(R):
        vol=vol+area[i]
        volume[i]=vol
    return [volume,Spheres,Normals]


volume,Spheres,Normals=growfrom((dims[0]//2,dims[1]//2,dims[2]//2))
R=len(Spheres)
drawradius=min(300,R//4)


Nor=[]
for tt in range(1,drawradius):
    Nor=Nor+Normals[tt]



fig=plt.figure(figsize=(14,7))
ax=fig.add_subplot(121)

squareplot=ax.plot([],[],color='#ff0000')
linplot=ax.plot([],[],color='#ff0000')
bplot=ax.plot([],[],color='#00bb00')
medplot=ax.plot([],[],color='#00bb00')
avgplot=ax.plot([],[],color='b')

ax.set_xscale("log")
ax.set_yscale("log")

S=Spheres[drawradius]
if(dim=="3d"):
    ay=fig.add_subplot(122,projection='3d')
    ay.set_xlim(left=0,right=dims[0])
    ay.set_ylim(bottom=0,top=dims[1])
    ay.set_zlim(0,dims[2])
    sphereplot=ay.scatter([v[0] for v in S],[v[1] for v in S],[v[2] for v in S],color='r')
else: 
    ay=fig.add_subplot(122)
    ay.set_xlim(left=0,right=dims[0])
    ay.set_ylim(bottom=0,top=dims[1])
    sphereplot=ay.scatter([v[0] for v in S],[v[1] for v in S],color='r')

if(dim=="3d"):
    lc=Line3DCollection(Nor)
    ay.add_collection3d(lc)
else:
    lc=LineCollection([((x,y),(a,b)) for ((x,y,z),(a,b,c)) in Nor])
    ay.add_collection(lc)

Nc=[[]]*dims[0]*dims[1]*dims[2]
for (v,w) in Nor:
    Nc[DO(v)]=Nc[DO(v)]+[w]
    Nc[DO(w)]=Nc[DO(w)]+[v]
np.save(name+"_ball.npy",[dims,Nc])

print("\n We've loaded a "+dim+" tree with "+str(dims[0]*dims[1]*dims[2])+" vertices.\n\n On the left is a log-log plot of the volume growth of balls as a function of radius (in the tree distance). \nThe blue lines are the average and maximal volumes over runs of DFS around different centers. \n The orange line is quadratic growth.\n\n On the right is a drawing of a ball of radius "+str(drawradius)+".")

volumebundle=[]
avgvol=[1]

def bundle(X,y):
    if X==[]:
        return [y]
    else:
        L=len(X[0])
        Ll=max(L,len(y))
        X=[x+[x[-1]]*(Ll-L) for x in X]
        y=y+[y[-1]]*(Ll-len(y))
        return X+[y]


def animate(t):
    global volumebundle
    global avgvol
#
    v=(np.random.randint(dims[0]),np.random.randint(dims[1]) ,np.random.randint(dims[2]))
    volume,_,_=growfrom(v)
#    volumebundle=bundle(volumebundle,volume)
#    meds=np.median(np.array(volumebundle),axis=0).tolist()
    
    avgvol=avgvol+[avgvol[-1]]*(len(volume)-len(avgvol))
    volume=volume+[volume[-1]]*(len(avgvol)-len(volume))
    I=range(len(avgvol))
    t1=t+1
    avgvol=[avgvol[i]**((t1-1)/t1)*volume[i]**(1/t1) for i in I]

   
    if(dim=="3d"):
        a=3/1.624
    else:
        a=1.25
    #bplot[0].set_data(I,[x**a for x in I])
    squareplot[0].set_data(I,[x**2 for x in I])
    linplot[0].set_data(I,[x for x in I])
#    medplot[0].set_data(I,meds)
    avgplot[0].set_data(I,avgvol)
#
    ax.set_xlim([1,len(avgvol)])
    ax.set_ylim([1,avgvol[-1]])

ani=animation.FuncAnimation(fig,animate,interval=1,frames=200,repeat=False)
plt.show()
