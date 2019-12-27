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
#flatedges=[((v[0],v[1]),(w[0],w[1])) for (v,w) in edges if v[2]==w[2]==0]
#V=set.union(set([v for (v,_) in flatedges]),set([v for (_,v) in flatedges]))
V=set.union(set([v for (v,_) in edges]),set([w for (_,w) in edges]))
V=[v for v in V]
X=[v[0] for v in V]
Y=[v[1] for v in V]
Z=[v[2] for v in V]
n=3**k//2
fig=plt.figure(figsize=(10,10))
ax=fig.add_subplot(111,projection='3d')
#lc=LineCollection(flatedges,color='b',linewidth=.5)
#ax.add_collection(lc)
ax.voxels(X,Y,Z,filled=np.ones(len(X)))

lc=Line3DCollection(edges,color='b',linewidth=.5)
ax.add_collection3d(lc)
#ax.scatter(X,Y,Z,color='r',s=.5)

ax.set_xlim(left=-n/2,right=n/2)
ax.set_ylim(bottom=-n/2,top=n/2)
ax.set_zlim(-n/2,n/2)
ax.view_init(elev=10)
print(edges)
ax.set_axis_off()
#ax.axis('equal')
plt.show()



