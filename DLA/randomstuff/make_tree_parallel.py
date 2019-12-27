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


#### Generate uniform spanning tree by Wilson's algorithm
####_____________________________________________________
####
#### Implementation: Nilin


M_prelim=int(input("Mesh size: "))
grain=int(input("vertex size: "))
layers=int(input("layers: "))

M_small=M_prelim//(2**layers)
M=M_small*(2**layers)
GRAIN=grain*2**(layers-1)

R_infty=M*int(input("Distance to infinity (ratio): "))

meshsizes=[M//(2**k) for k in range(layers)]
MESH=[-np.ones([2*meshsizes[k]+1,2*meshsizes[k]+1]) for k in range(layers)]


V=[(0,0)]
N=[set([])]

L=GRAIN
t=0
ball=[(i,j) for i in range(-grain,grain) for j in range(-math.ceil(math.sqrt(grain**2-i**2)),math.ceil(math.sqrt(grain**2-i**2)+1))]

def place(p,c):
    (X,Y)=p
    global MESH,ball
    for l,mesh in enumerate(MESH):
        (x,y)=(round(X//(2**l)),round(Y//(2**l)))
        paint(mesh,(x,y),ball,c)
    return

def paint(mesh,p,ball,c):
    (x,y)=p
    M=len(mesh)//2
    for (a,b) in ball:
        if abs(x+a)<=M and abs(y+b)<=M:
            mesh[M+x+a,M+y+b]=c
    return

place((0,0),0)
while L<M:
    ((x,y),s)=defs.newrandvertex(MESH,R_infty)
    L=max(L,max(abs(x),abs(y))+GRAIN)
    t=t+1
    V=V+[(x,y)]
    N=N+[{s}]
    N[s].add(t)
    place((x,y),t)


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
lc=LineCollection([(V[i],V[j]) for i in range(len(V)) for j in N[i] if j>i])
ax.add_collection(lc)
#ax.scatter([x for (x,_) in V],[y for (_,y) in V],s=10)
ay.imshow(MESH[0])
az.imshow(MESH[layers-1])
plt.show()#block=False)

        
#name="data/"+input("file name: ___.npy ")
name="data/justsomedata"
np.save(name,[V,N,MESH])
print("Saved to "+name+".npy")
