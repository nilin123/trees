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


#### Generate uniform spanning tree by Wilson's algorithm
####_____________________________________________________
####
#### Implementation: Nilin


fig=plt.figure(figsize=(10,10))
ax=fig.gca(projection='3d')
X,Y,Z=np.indices((4,4,4))
x=X[1:,1:,1:]
y=Y[1:,1:,1:]
z=Z[1:,1:,1:]
print(x+y+z)
w=x+y+z>5
ax.voxels(X,Y,Z,w,linewidth=1)

#ax.set_axis_off()
plt.show()



