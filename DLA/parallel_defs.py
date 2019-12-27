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

randsteplist=[]
t_rand=0

def randstep():
    global randsteplist
    global t_rand
    if t_rand>=len(randsteplist)-1:
        randsteplist=rnd.choice([-1,1],100000)
        t_rand=0
    else:
        t_rand=t_rand+1
    return randsteplist[t_rand]

def circle(R):
    (x,y)=(rnd.normal(),rnd.normal())
    r=math.sqrt(x**2+y**2)
    c=R/r
    return (round(c*x),round(c*y))

def bounddist(p,R):
    (x,y)=p
    r=math.sqrt(x**2+y**2)
    c=R/r
    if(c<.95):
        return (c*x,c*y)
    return (x,y)

def newrandvertex(MESH,R):
    (x,y)=circle(R)
    M=len(MESH[0])//2
    layers=len(MESH)
    level=layers

    while(abs(x)>M or abs(y)>M or MESH[0][int(round(M+x)),int(round(M+y))]<0):
        (x,y)=bounddist((x,y),R)
        if abs(x)>M or abs(y)>M:
            level=layers
        else:
            colors=[MESH[l][int(round((M+x)//2**l)),int(round((M+y)//2**l))] for l in range(layers)]
            level=max([l for l in range(layers) if colors[l]<0])
        stepsize=2**level
        (x,y)=(int(round(x+stepsize*randstep())),int(round(y+stepsize*randstep())))
    return ((x,y),int(MESH[0][M+x,M+y])) 


