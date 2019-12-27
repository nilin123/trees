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


res=200
margin=2
xtoi=lambda x:round((x+1)/2*(res-2*margin)+margin)
ytoj=lambda y:round((y+1)/2*(res-2*margin)+margin)
axtogrid=(xtoi,ytoj)
itox=lambda i:(i-margin)*2/res-1
jtoy=lambda j:(j-margin)*2/res-1
gridtoax=(itox,jtoy)


fignum=len(MV)
figdimlist={3:[1,3],4:[2,2],5:[1,5],6:[2,3],7:[2,4],8:[2,4]}
fig=plt.figure(figsize=(6*figdimlist[fignum][0],8*figdimlist[fignum][0]))
figdims=figdimlist[fignum]
PLOTS=[fig.add_subplot(figdims[0],figdims[1],i+1) for i in range(fignum)]


for i in range(fignum):
    PLOTS[i].axis('scaled')

    PLOTS[i].set_xlim(left=-1,right=1)
    PLOTS[i].set_ylim(bottom=-1,top=1)
    tk.drawrichpartition(V,richMV[i],PLOTS[i],int((res/15)//2**(i/2)),False,gridtoax,axtogrid,res)


plt.show()

