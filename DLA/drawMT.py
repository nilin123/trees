import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.lines as mlines
import matplotlib.colors as mcolors
import matplotlib.transforms as mtransforms
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.collections import LineCollection
#from refine import branch_verts, path_verts, section_verts
import math
import scipy.spatial as spatial
import sys
import pdb
import drawparttools as tk

#################################################################
#### Explore tree constructed using make_tree.py
#### author: Nilin
#################################################################

name="data/"+input("file name: ____.npy\n")+".npy"
[V,N,MT]=np.load(name,allow_pickle=True)
(MV,richMV,ME)=MT
n=len(V)

V=tk.centerV(V)
theta=math.pi/4
V=[(math.cos(theta)*x-math.sin(theta)*y,math.cos(theta)*y+math.sin(theta)*x) for (x,y) in V]

res=200
margin=2
xtoi=lambda x:round((x+1)/2*(res-2*margin)+margin)
itox=lambda i:(i-margin)*2/res-1


layers=min(len(MV),int(input("number of layers: ")))
if layers>=len(MV):
    Elayers=layers-1
else:
    Elayers=layers
heights=[-math.tanh(i/layers)*layers*.9 for i in range(len(MV))]
h=.35


fig,ax=plt.subplots()#figsize=(3,5))
ax.axis('scaled')
ax.set_xlim(left=-1,right=1)
ax.set_ylim(top=heights[0]+2*h,bottom=heights[-1]-2*h-1)
#plt.text(0,heights[0]+.8,"dimension index")
#plt.text(0,heights[-1]-.8,"physical indices")

for i in range(layers):
    W=[(x,h*y+heights[i]) for (x,y) in V]
    ytoj=lambda y:round((y-heights[i]+h)/(2*h)*(res-2*margin)+margin)
    jtoy=lambda j:h*((j-margin)*2/res-1)+heights[i]
    axtogrid=(xtoi,ytoj)
    gridtoax=(itox,jtoy)
    tk.drawrichpartition(W,richMV[i],ax,int((res/15)//2**(i/2)),False,gridtoax,axtogrid,res,zorder=-2*i,drawspine=False)


def centroid(subtree):
    vertindices=list(subtree[1][0])
    verts=[V[i] for i in vertindices]
    return np.sum(np.array(verts),0)/len(verts)

CENTERS=[[centroid(subtree) for subtree in P] for P in richMV]

def vertline(top,bottom,htop,hbottom,theax,h,zorder):
    (x0,y0)=top
    (x,y)=bottom

    T=np.linspace(0,1,num=11,endpoint=True)
    I=range(len(T))
    w0=[(1+math.cos(math.pi*t))/2 for t in T]
    w1=[(1-math.cos(math.pi*t))/2 for t in T]
    X=[x0*w0[i]+x*w1[i] for i in I]; Y=[h*(y0*w0[i]+y*w1[i])+T[i]*hbottom+(1-T[i])*htop for i in I]
    theax.plot(X,Y,color='#000000',linewidth=4*(1.2**zorder),alpha=1.1**zorder,zorder=zorder)

for i,CLDlist in enumerate(ME[:Elayers]):
    for pa,CLD in enumerate(CLDlist):
        (x0,y0)=CENTERS[i][pa]
        CLDpos=[CENTERS[i+1][cld] for cld in CLD]
        for (x,y) in CLDpos:
            vertline((x0,y0),(x,y),heights[i],heights[i+1],ax,h,-2*i-1)

(x0,y0)=CENTERS[0][0]
ax.plot([x0,x0],[h*y0+.6,h*y0],zorder=10,linewidth=4,color="#000000")
#lc=LineCollection([((x,heights[layers-1]+h*y-1),(x,heights[layers-1]-1.03+h*y)) for (x,y) in V],linewidth=.5,zorder=-10,color="#000000")
#ax.add_collection(lc)
if layers>=len(MV):
    for (x,y) in CENTERS[-1]:
        ax.plot([x,x],[heights[layers-1]+h*y,heights[layers-1]-.2+h*y],zorder=-10,linewidth=.5,alpha=1.1**(-2*layers),color="#000000")



ax.set_axis_off()
plt.show()

