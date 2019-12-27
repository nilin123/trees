import numpy as np
import numpy.random as rnd
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.lines as mlines
from multiprocessing import Pool
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.collections import LineCollection
import pdb
import time
import parallel_defs as defs


####_____________________________________________________
####
#### Implementation: Nilin


M=int(input("Mesh size: "))
mesh=np.zeros([2*M+1,2*M+1])
crudemesh=np.zeros([2*M+1,2*M+1])

mesh[M,M]=1
V=[(0,0)]
I=[set([])]
parent=[0]
grain=3
GRAIN=10

R=10
t=1
ball=[(i,j) for i in range(-grain,grain) for j in range(-round(math.sqrt(grain**2-i**2)),round(math.sqrt(grain**2-i**2)))]

#def crudepaint(v):
#    a=int(max(M+v[0]-GRAIN,0))
#    c=int(min(M+v[0]+GRAIN,2*M)+1)
#    
#    b=int(max(M+v[1]-GRAIN,0))
#    d=int(min(M+v[1]+GRAIN,2*M)+1)
#
#    crudemesh[a:c,b:d]=np.ones([c-a,d-b])
#    return
#

for (a,b) in ball:
    mesh[M+a,M+b]=t
crudemesh[M-1:M+3,M-1:M+3]=np.ones([4,4])
while R<.8*M:
    ((x,y),s)=defs.newrandvertex(mesh,crudemesh,'fine',GRAIN,R)
    R=max(R,math.sqrt(x**2+y**2)+grain)
    t=t+1
    V=V+[(x,y)]
    I=I+[{s}]
    parent=parent+[s]
    I[s].add(t)
    for (a,b) in ball:
        mesh[M+x+a,M+y+b]=t
    crudemesh[M+(x//GRAIN)-1:M+(x//GRAIN)+3,M+(y//GRAIN)-1:M+(y//GRAIN)+3]=np.ones([4,4])
print(parent)
fig=plt.figure(figsize=(18,6))
ax=fig.add_subplot(131)
ax.set_xlim(left=-M,right=M)
ax.set_ylim(bottom=-M,top=M)

ay=fig.add_subplot(132)
az=fig.add_subplot(133)


#segmentstable=[[(v,V[j]) for j in I[i]] for i,v in enumerate(V)]
#segments=[]
#for l in segmentstable:
#    segments=segments+l
lc=LineCollection([(V[parent[i]],V[i]) for i in range(1,len(V))])
ax.add_collection(lc)
ax.scatter([x for (x,_) in V],[y for (_,y) in V],s=10)
ay.imshow(mesh)
az.imshow(crudemesh)
plt.show()#block=False)

        
#name="data/"+input("file name: ___.npy ")
#np.save(name,[V,I])
#print("Saved to "+name+".npy")
