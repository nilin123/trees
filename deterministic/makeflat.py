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


####_____________________________________________________
####
#### Implementation: Nilin


k=int(input("k: "))

def scale(v,r):
    (x,y,z)=v
    return (r*x,r*y,r*z)

def shift(e,s):
    ((x0,y0,z0),(x1,y1,z1))=e;(a,b,c)=s;
    return ((a+x0,b+y0,c+z0),(a+x1,b+y1,c+z1))


def VT(k):
    if k==0:
        return []
    smalltree=VT(k-1)
    edges=[e for e in smalltree]
    n=3**k
    dirs=[(1,0,0),(0,1,0),(0,0,1),(-1,0,0),(0,-1,0),(0,0,-1)]
    gluedges=[(scale(v,n//6),scale(v,n//6+1)) for v in dirs]
    edges=edges+gluedges
    for v in dirs:
        edges=edges+[shift(e,scale(v,n//3)) for e in smalltree]
    return edges

edges=VT(k)
flatedges=[((v[0],v[1]),(w[0],w[1])) for (v,w) in edges if v[2]==w[2]==0]
V=set.union(set([v for (v,_) in flatedges]),set([v for (_,v) in flatedges]))
V=[v for v in V]
X=[v[0] for v in V]
Y=[v[1] for v in V]
print(X,Y)
n=3**k//2
fig, ax=plt.subplots()
lc=LineCollection(flatedges,color='b',linewidth=.5)
ax.add_collection(lc)
ax.scatter(X,Y,color='r',s=.5)
#for r,E in enumerate(Espheres):
#    c=((math.sin(r)+1)/4,(math.sin(r/3)+1)/4,(math.sin(r/9)+1)/2,1)
#    print(c)
#    lc=LineCollection(E,color=c,linewidth=.5)
#    ax.add_collection(lc)

ax.set_xlim(left=-n,right=n)
ax.set_ylim(bottom=-n,top=n)
ax.set_axis_off()
ax.axis('equal')
plt.show()




#
#N={}
#for (v,w) in edges:
#    N[v]=set([]); N[w]=set([])
#
#for (v,w) in edges:
#    N[v].add(w)
#    N[w].add(v)
#
#
#colors=[1 for e in edges]
#
#spheres=[[(0,0,0)]]
#ball=set([])
#while len(spheres[-1])>0:
#    ball=set.union(ball,spheres[-1])
#    allneighbors=set.union(*[N[v] for v in spheres[-1]])
#    sphere=set.difference(allneighbors,ball)
#    spheres=spheres+[sphere]
#
#Espheres=[[]]*(len(spheres)-1)
#for i in range(len(spheres)-1):
#    Espheres[i]=[(v,w) for v in spheres[i] for w in N[v] if w in spheres[i+1]]
#

