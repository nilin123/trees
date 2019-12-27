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
    if k==-1:
        return []
    smalltree=VT(k-1)
    edges=[e for e in smalltree]
    n=3**k
    dirs=[(1,0,0),(0,1,0),(0,0,1),(-1,0,0),(0,-1,0),(0,0,-1)]
    gluedges=[(scale(v,n//2),scale(v,n//2+1)) for v in dirs]
    edges=edges+gluedges
    for v in dirs:
        edges=edges+[shift(e,scale(v,n)) for e in smalltree]
    return edges

edges=VT(k)

N={}
for (v,w) in edges:
    N[v]=set([]); N[w]=set([])

for (v,w) in edges:
    N[v].add(w)
    N[w].add(v)


colors=[1 for e in edges]

spheres=[[(0,0,0)]]
ball=set([])
while len(spheres[-1])>0:
    ball=set.union(ball,spheres[-1])
    allneighbors=set.union(*[N[v] for v in spheres[-1]])
    sphere=set.difference(allneighbors,ball)
    spheres=spheres+[sphere]

Espheres=[[]]*(len(spheres)-1)
for i in range(len(spheres)-1):
    Espheres[i]=[(v,w) for v in spheres[i] for w in N[v] if w in spheres[i+1]]


n=3**k
fig=plt.figure(figsize=(8,8))
ax=fig.add_subplot(111,projection='3d')
for r,E in enumerate(Espheres):
    c=((math.sin(r)+1)/4,(math.sin(r/3)+1)/4,(math.sin(r/9)+1)/2,1)
    print(c)
    lc=Line3DCollection(E,color=c,linewidth=.5)
    ax.add_collection3d(lc)

ax.set_xlim(left=-n,right=n)
ax.set_ylim(bottom=-n,top=n)
ax.set_zlim(-n,n)
ax.set_axis_off()
plt.show()

#mesh=VT(k)
#V=[(i,j,k) for i in range(n) for j in range(n) for k in range(n) if mesh[i,j,k]>0]
#X=[x for (x,_,_) in V]
#Y=[y for (_,y,_) in V]
#Z=[z for (_,_,z) in V]
#print(V)
#
#fig=plt.figure(figsize=(8,8))
#ax=fig.add_subplot(111,projection='3d')
#ax.scatter(X,Y,Z,color='#0000dd',s=1,depthshade=True)
#ax.set_proj_type('ortho')
#ax.set_axis_off()
#
#plt.show()
#
#

#V=[(0,0)]
#I=[set([])]
#R=0
#dx=1
#randsteplist=[]
#t_rand=0
#
#n=int(input("How many vertices? "))
#
#def randstep():
#    global randsteplist
#    global t_rand
#    if t_rand>=len(randsteplist)-1:
#        randsteplist=rnd.normal(0,1,10000000)
#        t_rand=0
#    else:
#        t_rand=t_rand+1
#    return randsteplist[t_rand]
#
#def incr(v,dv):
#    return ((v[0]+dv[0],v[1]+dv[1]))
#
#def addvertex(v,j):
#    global R
#    global V
#    global I
#    V=V+[v]
#    I[j].add(len(I))
#    I=I+[{j}]
#    R=max(R,math.sqrt(v[0]**2+v[1]**2))
#    return
#
#def argmindist(v):
#    global V
#    return np.argmin([(v[0]-x)**2+(v[1]-y)**2 for i,(x,y) in enumerate(V)])
#
#def sqmindist(v):
#    global V
#    w=V[argmindist(v)]
#    return (w[0]-v[0])**2+(w[1]-v[1])**2
#
#def addrandvertex():
#    global R
#    v=(R+100,0)
#    while(sqmindist(v)>1):
#        (x,y)=(rnd.normal(),rnd.normal())
#        r=math.sqrt(x**2+y**2)
#        c=(R+1)/r
#        v=(c*x,c*y)
#        while(sqmindist(v)>1 and v[0]**2+v[1]**2<(R+10)**2):
#            scale=math.sqrt(sqmindist(v))/2+0.1
#            dv=(scale*randstep(),scale*randstep())
#            v=incr(v,dv)
#    j=argmindist(v)
#    addvertex(v,j)
#    return
#
#for i in range(n):
#    addrandvertex()
#
#
#fig=plt.figure(figsize=(8,8))
#ax=fig.add_subplot(111)
#ax.set_xlim(left=-R,right=R)
#ax.set_ylim(bottom=-R,top=R)
#
#
#segmentstable=[[(v,V[j]) for j in I[i]] for i,v in enumerate(V)]
#segments=[]
#for l in segmentstable:
#    segments=segments+l
#lc=LineCollection(segments)
#ax.add_collection(lc)
#plt.show(block=False)
#
#        
#name="data/"+input("file name: ___.npy ")
#np.save(name,[V,I])
#print("Saved to "+name+".npy")
