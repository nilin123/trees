import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.lines as mlines
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import LineCollection
import pdb
import sys

#name=input("Load tree from file (exclude .npy): ")
#[V,N,_]=np.load(name+".npy",allow_pickle=True)

name="data/400"#input("Load tree from file (exclude .npy): ")
[V,N,_]=np.load(name+".npy",allow_pickle=True)


fig=plt.figure(figsize=(8,8))
ax=fig.add_subplot(111)
X=[x for (x,y) in V]
Y=[y for (x,y) in V]
#ax.scatter(X,Y)

n=len(V)
edges=set({})
for i in range(n):
    for j in N[i]:
        edges.add((i,j))
lc=LineCollection([(V[i],V[j]) for (i,j) in edges],color=[(.6,.6,1)],linewidth=.5,zorder=-1)
ax.add_collection(lc)

def halfball(c,barrier,R):
    #pdb.set_trace()
    S={c}
    B={c}
    for r in range(R):
        S_prev=S
        S=set.union(*[N[i] for i in S_prev])
        S=set.difference(S,B)
        S=set.difference(S,barrier)
        B=set.union(B,S)
    return [[i for i in B],[i for i in S]]

c=0
barrier=set({N[c].pop()})
[B,S]=halfball(c,barrier,int(input("red ball radius: ")))
#print(B)
ax.scatter([X[i] for i in B],[Y[i] for i in B],s=3,color='r')    
ax.scatter([X[i] for i in S],[Y[i] for i in S],marker="2",s=40,color=[(0,0,0)])    
ax.scatter([X[c]],[Y[c]],marker="2",s=40,color=[(0,0,0)])

#outname=input("output destination")
outname="figures/barrier.pdf"
plt.axis('off')
plt.savefig(outname)
