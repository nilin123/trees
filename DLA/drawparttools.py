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

#################################################################
#### Explore tree constructed using make_tree.py
#### author: Nilin
#################################################################



def centerV(V):
    xmin=min([x for (x,_) in V])
    xmax=max([x for (x,_) in V])
    ymin=min([y for (_,y) in V])
    ymax=max([y for (_,y) in V])
    w=max(xmax-xmin,ymax-ymin)/2
    center=((xmin+xmax)/2,(ymin+ymax)/2)
    V=[((x-center[0])/w,(y-center[1])/w) for (x,y) in V]
    return V

def expand(grid,r):
    (m,n)=np.shape(grid)
    circ=[(i,j) for i in range(-r,r+1) for j in range(-r,r+1) if (r-4)**2<=i**2+j**2<=r**2]
    expgrid=np.zeros([m+2*r,n+2*r])
    for (i,j) in circ:
        expgrid[r+i:m+r+i,r+j:n+r+j]=np.maximum(expgrid[r+i:m+r+i,r+j:n+r+j],grid)
    return expgrid

def outline(V,r1,r2,r3,fill,axtogrid,res):
    (xtoi,ytoj)=axtogrid
    w=1
    grid=np.zeros([res,res])
    for (x,y) in V:
        grid[xtoi(x),ytoj(y)]=1
    blob=expand(grid,r1)
    outer=expand(1-blob,r2)
    inner=expand(1-outer,r3)
    intinner=expand(1-outer,r3-w)

    rrr=r1+r2+r3
    outlinegrid=inner[rrr:-rrr,rrr:-rrr]-(int(not fill))*intinner[rrr-w:-rrr+w,rrr-w:-rrr+w]

    return outlinegrid

def pointsonline(grid,r,gridtoax):
    (itox,jtoy)=gridtoax
    (X,Y)=np.where(grid==1)
    if len(X)==0:
        return [],[]
    i0=rnd.randint(len(X))
    (x,y)=(X[i0],Y[i0])
    J=[j for j in range(len(X))]
    ptlist=[]
    while True: 
        sqdist=(X-x)**2+(Y-y)**2
        J=[j for j,d in enumerate(sqdist) if d>r]
        X=X[J]; Y=Y[J]; sqdist=sqdist[J]

        if(len(sqdist)==0):
            ptlist=ptlist+[ptlist[0]]
            return [itox(i) for (i,_) in ptlist],[jtoy(j) for (_,j) in ptlist]
        j=np.argmin(sqdist)
        (x,y)=(X[j],Y[j]) 
        ptlist=ptlist+[(x,y)]


def drawrichpartition(V,P,theax,outlinegrain,fill,gridtoax,axtogrid,res,zorder=0,drawspine=True):
    (itoy,jtox)=gridtoax
    (xtoi,ytoj)=gridtoax
    colors={'branch':'#ff0000','point':'r','section':'#0000ff','edge':'b'}
    r=outlinegrain
    for (style,subtree,metadata) in P:
        (verts,edges)=subtree
        vertlist=[V[i] for i in verts]
        lc=LineCollection([(V[i],V[j]) for (i,j) in edges],color=colors[style],linewidth=.5,zorder=zorder)
        theax.add_collection(lc)
        if(style=='section' or style=='edge'):
            if drawspine:
                path=metadata
                theax.plot([V[i][0] for i in path],[V[i][1] for i in path],linewidth=2,color='#000099')
            outln=outline([V[i] for i in verts],4*r,4*r,3,fill,axtogrid,res) 
            X,Y=pointsonline(outln,r,gridtoax)
            theax.plot(X,Y,color='b',linewidth=1,zorder=zorder)
            theax.fill(X,Y,color='#ffffff',alpha=.8,zorder=zorder-.5)
        elif(style=='branch'):
            outln=outline([V[i] for i in verts],4*r,5*r,r,fill,axtogrid,res) 
            X,Y=pointsonline(outln,r/2,gridtoax)
            theax.plot(X,Y,color='r',linewidth=1,zorder=zorder)
            theax.fill(X,Y,color='#ffffff',alpha=.8,zorder=zorder-.5)
        elif(style=='point'):
            (a,b)=V[metadata[0]]
            #theax.scatter([a],[b],s=40,zorder=5,color='#000099')
            #theax.scatter([a],[b],s=20,zorder=6,color='r')
    return
