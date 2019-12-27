import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.lines as mlines
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.collections import LineCollection
import pdb
import sys

name=input("Load tree from file (exclude .npy): ")
[dims,paths]=np.load(name+".npy")

N=dims[0]*dims[1]*dims[2]

if(N>15000):
    ok=input("\nThis feature displays the entire tree.\nIt may be slow for this tree with "+str(N)+">15,000 vertices.\nContinue? (y/n): ")
    if(ok!="y"):
        print("Exiting")
        sys.exit()

fig=plt.figure(figsize=(8,8))
#if(dims[2]==1):
#    ax=fig.add_subplot(111)
#    for path in paths:
#        ax.plot([v[0] for v in path],[v[1] for v in path],color='#0000dd')
#else:
#    ax=fig.add_subplot(111,projection='3d')
#    for path in paths:
#        ax.plot([v[0] for v in path],[v[1] for v in path],[v[2] for v in path],color='#0000dd')

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
