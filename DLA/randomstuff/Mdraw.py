import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.lines as mlines
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.collections import LineCollection
#from refine import branch_verts, path_verts, section_verts
import math
import sys
import pdb

#################################################################
#### Explore tree constructed using make_tree.py
#### author: Nilin
#################################################################

[V,N,MT]=np.load("data/refine400.npy",allow_pickle=True)
(MV,richMV,ME)=MT
n=len(V)

fh=lambda t:-t**2

def drawrichpartition(P,theax,t):
    #colors={'branch':'r','point':'r','section':b,'edge':'b'}
    for (style,(verts,edges),metadata) in P:
        if(style=='section' or style=='edge'):
            path=metadata
            #theax.scatter([V[i][0] for i in verts],[V[i][1] for i in verts],[h]*len(verts),s=6,color='b',alpha=.1)
            v=V[path[0]]
            w=V[path[-1]]
            #theax.scatter([v[0],w[0]],[v[1],w[1]],[h,h],s=12,zorder=5,color='b')
            #theax.scatter([v[0],w[0]],[v[1],w[1]],[h,h],s=3,zorder=6,color='r')
            theax.plot([V[i][0] for i in path],[V[i][1] for i in path],[fh(t)]*len(path),color='b')
        elif(style=='branch'):
            #theax.scatter([V[i][0] for i in verts],[V[i][1] for i in verts],[h]*len(verts),s=6,color='r',alpha=.3)
            r=metadata[0]
            #theax.scatter([V[r][0]],[V[r][1]],[h],s=12,zorder=5,color='b')
            #theax.scatter([V[r][0]],[V[r][1]],[h],s=3,zorder=5,color='r')
        drawcentroid((style,verts,metadata),theax,t)
    return

def drawcentroid(subtree,theax,t):
    style=subtree[0]
    (x,y)=centroid(subtree)
    colors={'edge':'b','section':'b','point':'r','branch':'r'}
    size={'edge':20,'section':5,'point':5,'branch':30}
    theax.scatter([x],[y],[fh(t)],s=size[style],color=colors[style])


def drawM(P_t,P_b,cldlist,theax,t):
    for i,cldn in enumerate(cldlist):
        c_t=centroid(P_t[i])
        for j in cldn:
            c_b=centroid(P_b[j])
            theax.plot([c_t[0],c_b[0]],[c_t[1],c_b[1]],[fh(t),fh(t+1)],linewidth=.5,color='#00aa00',alpha=.3)
    return


def centroid(subtree):
    (xv,yv)=centroid_verts(subtree[1])
    (xp,yp)=centroid_verts(subtree[2])
    if subtree[0]=='section':
        return ((xp),(yp))
    else:
        return ((xp),(yp))

def centroid_verts(verts):
    xsum=sum([V[i][0] for i in verts])
    ysum=sum([V[i][1] for i in verts])
    l=len(verts)
    return (xsum/l,ysum/l)

fig=plt.figure(figsize=(7,20))
ax=fig.add_subplot(111,projection='3d')
ax.xaxis.set_pane_color((1,1,1,0))
ax.set_axis_off()

#height=int(input("height: "))
#height=min(height,len(MV))
height=len(MV)

for t in range(height):
    drawrichpartition(richMV[t],ax,t)

for t in range(height-1):
    print(ME[t])
    drawM(richMV[t],richMV[t+1],ME[t],ax,t)

print(ME[0],ME[1])

plt.show()#block=False)

