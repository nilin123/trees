import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.lines as mlines
import matplotlib.colors as mcolors
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

name="data/"+input("file name: ____.npy\n")+".npy"
[V,N,MT]=np.load(name,allow_pickle=True)
(MV,richMV,ME)=MT
n=len(V)



res=200
margin=2
gx_=lambda x:round((x-xlim[0])/W*(res-2*margin)+margin)
gy_=lambda y:round((y-ylim[0])/W*(res-2*margin)+margin)
cx=lambda i:xlim[0]+(i-margin)*W/res
cy=lambda j:ylim[0]+(j-margin)*W/res



def expand(grid,r):
    (m,n)=np.shape(grid)
    circ=[(i,j) for i in range(-r,r+1) for j in range(-r,r+1) if (r-4)**2<=i**2+j**2<=r**2]
    expgrid=np.zeros([m+2*r,n+2*r])
    for (i,j) in circ:
        expgrid[r+i:m+r+i,r+j:n+r+j]=np.maximum(expgrid[r+i:m+r+i,r+j:n+r+j],grid)
    return expgrid

def outline(V,r1,r2,r3,fill):
    global res
    w=1
    grid=np.zeros([res,res])
    for (x,y) in V:
        grid[gx_(x),gy_(y)]=1
    blob=expand(grid,r1)
    outer=expand(1-blob,r2)
    inner=expand(1-outer,r3)
    intinner=expand(1-outer,r3-w)

    rrr=r1+r2+r3
    outlinegrid=inner[rrr:-rrr,rrr:-rrr]-(int(not fill))*intinner[rrr-w:-rrr+w,rrr-w:-rrr+w]

    #outlinegrid=smooth(outlinegrid,20)
    return outlinegrid# [(cx(i),cy(j)) for i in range(res) for j in range(res) if outlinegrid[i,j]==1]

def smooth(mesh,k):
    for i in range(k):
        mesh[1:-1,1:-1]=.2*(mesh[1:-1,1:-1]+mesh[2:,1:-1]+mesh[:-2,1:-1]+mesh[1:-1,2:]+mesh[1:-1,:-2])
    return mesh

def drawrichpartition(P,theax,outlinegrain,fill):
    global res
    global xlim, ylim
    colors={'branch':'#ff0000','point':'r','section':'#0000ff','edge':'b'}
    r=outlinegrain
    mesh=np.zeros([res,res])
    secmesh=np.zeros([res,res])
    for (style,subtree,metadata) in P:
        (verts,edges)=subtree
        vertlist=[V[i] for i in verts]
        lc=LineCollection([(V[i],V[j]) for (i,j) in edges],color=colors[style],linewidth=.5)
        theax.add_collection(lc)
            
        if(style=='section' or style=='edge'):
            path=metadata
            theax.plot([V[i][0] for i in path],[V[i][1] for i in path],linewidth=2,color='#000099')
            secmesh=np.maximum(secmesh,outline([V[i] for i in verts],5*r,5*r,r,fill))
        elif(style=='branch'):
            mesh=np.maximum(mesh,outline([V[i] for i in verts],5*r,6*r,r,fill))
        elif(style=='point'):
            (a,b)=V[metadata[0]]
            theax.scatter([a],[b],s=40,zorder=5,color='#000099')
            theax.scatter([a],[b],s=20,zorder=6,color='r')
    redmap=mcolors.LinearSegmentedColormap.from_list("",["white","red"])
    blumap=mcolors.LinearSegmentedColormap.from_list("",["white","blue"])
    theax.imshow([[mesh[j,i]/2+.5 for j in range(res)] for i in range(res)],origin='lower',extent=[xlim[0],xlim[1],ylim[0],ylim[1]],zorder=-10,cmap=redmap)
    theax.imshow([[secmesh[j,i]/2+.5 for j in range(res)] for i in range(res)],origin='lower',extent=[xlim[0],xlim[1],ylim[0],ylim[1]],zorder=-9,cmap=blumap,alpha=.3)
    #theax.pcolormesh([cy(j) for j in range(res)],[cx(i) for i in range(res)],[[mesh[j,i] for j in range(res)] for i in range(res)],zorder=-10,cmap=lambda x:(1,1-x,1-x,1))

    return



fignum=len(MV)-1
figdimlist={3:[1,3],4:[2,2],5:[1,5],6:[2,3]}
fig=plt.figure(figsize=(6*figdimlist[fignum][0],8*figdimlist[fignum][0]))
figdims=figdimlist[fignum]
PLOTS=[fig.add_subplot(figdims[0],figdims[1],i+1) for i in range(fignum)]




xmin=min([x for (x,_) in V])
xmax=max([x for (x,_) in V])
ymin=min([y for (_,y) in V])
ymax=max([y for (_,y) in V])
W=max(xmax-xmin,ymax-ymin)
center=((xmin+xmax)/2,(ymin+ymax)/2)
xlim=(center[0]-W/2,center[0]+W/2)
ylim=(center[1]-W/2,center[1]+W/2)
fills=[0,0,0,0]

for i in range(fignum):
    PLOTS[i].axis('equal')

    PLOTS[i].set_xlim(left=xlim[0],right=xlim[1])
    PLOTS[i].set_ylim(bottom=ylim[0],top=ylim[1])
    PLOTS[i].set_axis_off()
    drawrichpartition(richMV[i],PLOTS[i],int((res/15)//2**(i/2)),fills[i])




#mfig=plt.figure()
#mplot=mfig.add_subplot()
#mplot.set_xlim(left=xlim[0],right=xlim[1])
#mplot.set_ylim(bottom=ylim[0],top=ylim[1])
#mplot.set_axis_off()
#for i in range(fignum):
#    drawrichpartition(richMV[i],mplot,int((res/15)//2**(i/2)),fills[i])



#outfig,outplot=plt.subplots()


#drawoutline(richMV[2],outplot)




plt.show()

