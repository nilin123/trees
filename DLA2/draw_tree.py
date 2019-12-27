import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.lines as mlines
from mpl_toolkits.mplot3d import Axes3D
import pdb
import sys

name=input("Load tree from file (exclude .npy): ")
[dims,paths]=np.load(name+".npy",allow_pickle=True)

N=dims[0]*dims[1]*dims[2]

if(N>15000):
    ok=input("\nThis feature displays the entire tree.\nIt may be slow for this tree with "+str(N)+">15,000 vertices.\nContinue? (y/n): ")
    if(ok!="y"):
        print("Exiting")
        sys.exit()


fig=plt.figure(figsize=(8,8))
if(dims[2]==1):
    ax=fig.add_subplot(111)
    for path in paths:
        ax.plot([v[0] for v in path],[v[1] for v in path],color='#0000dd')
else:
    ax=fig.add_subplot(111,projection='3d')
    for path in paths:
        ax.plot([v[0] for v in path],[v[1] for v in path],[v[2] for v in path],color='#0000dd')


#plt.show()
outname=input("output destination")
plt.savefig(outname)

