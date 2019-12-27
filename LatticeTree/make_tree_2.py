import numpy as np
import numpy.random as rnd
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.lines as mlines
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.collections import LineCollection
import pdb
import time


#### Generate uniform spanning tree by Wilson's algorithm
####_____________________________________________________
####
#### Implementation: Nilin


#### Inputs ####
d=input("\nWe will generate a tree in a lattice. Dimension 2 or 3? \n")
vertexnumber=int(input("\nHow many vertices? (Suggestion: 10,000) \n"))
scale=math.ceil(vertexnumber**(1.0/int(d)))
name=input("\nExport tree as [Please input file name].npy: \n")


dims=[scale]*3
if(d=="2"):
    dims[2]=1
    print("I'll generate a UST on the "+str(scale)+"x"+str(scale)+" square.")
else:
    print("I'll generate a UST on the "+str(scale)+"x"+str(scale)+"x"+str(scale)+" cube.")

#### Current tree T=(V,E) ####

#### Characteristic function of V ####
V=np.zeros(dims)

#### paths is a list of LERWs. Each LERW is a sequence of vertices ####
paths=[[]]

add=lambda v,w:(v[0]+w[0],v[1]+w[1],v[2]+w[2])
dilate=lambda r,v:((r*v[0]),(r*v[1]),(r*v[2]))    

def dirs(v):
    D=[(1,0,0),(0,1,0),(0,0,1),(-1,0,0),(0,-1,0),(0,0,-1)]
    for d in range(3):
        e=tuple([1 if i==d else 0 for i in range(3)])
        if(v[d]==0):
            D.remove(dilate(-1,e))
        if(v[d]==dims[d]-1):
            D.remove(e)
    return D

def uniformOutside():
    complement=1-V
    S0=complement.sum(axis=(1,2))
    p0=S0/sum(S0)
    x=np.random.choice(dims[0],p=p0)

    S1=complement[x,:,:].sum(axis=1)
    p1=S1/sum(S1)
    y=np.random.choice(dims[1],p=p1)

    S2=complement[x,y,:]
    p2=S2/sum(S2)
    z=np.random.choice(dims[2],p=p2)
    return (x,y,z)


#### Each vertex of LERW marked with its time starting from 1. Time goes back when loop is erased.
#### Each vertex of tree marked with -1.

def LERW(V):
    W=-1*V
    v=uniformOutside()
    t=1
    path=[v]
    while(W[v]>=0):
        D=dirs(v)
        w=add(v,D[np.random.choice(len(D))])
        if(W[v]==0):
            W[v]=t
        else:
            t=W[v]
            W=(W<=t)*W
            path=path[:int(t)]
        path=path+[w]
        v=w
        t=t+1
    return (path,W)

v=uniformOutside()
V[v]=1
n=1
lastpercent=0
while n<dims[0]*dims[1]*dims[2]:
    (path,W)=LERW(V)
    n=n+len(path)-1
    V=(W!=0)
    paths=paths+[path]
    percent=100*n//(dims[0]*dims[1]*dims[2])
    if(percent>lastpercent):
        print("["+"#"*percent+"."*(100-percent)+"]")
        lastpercent=percent
np.save(name,[dims,paths])
print("\nTree constructed.\n")

fig=plt.figure(figsize=(8,8))
if(dims[2]>1):
    ax=fig.add_subplot(111,projection='3d')
    ax.set_xlim(left=0,right=dims[0])
    ax.set_ylim(bottom=0,top=dims[1])
    ax.set_zlim(0,dims[2])
    lc=Line3DCollection(paths[1:])
    ax.add_collection3d(lc)
else:
    ax=fig.add_subplot(111)
    ax.set_xlim(left=0,right=dims[0])
    ax.set_ylim(bottom=0,top=dims[1])
    segments=[[(v[0],v[1]) for v in path] for path in paths[1:]]
    lc=LineCollection(segments)
    ax.add_collection(lc)
plt.show()
        
print("\nTree saved to "+name+".npy\n")
