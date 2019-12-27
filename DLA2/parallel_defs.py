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

def newrandvertex(mesh,crudemesh,style,GRAIN,R):
    print(style)
    M=len(mesh)//2
    first=True
    while(first or int(mesh[M+x,M+y])==0):
        if(style=='crude'):
            (x,y)=circle(R)
            R_stop=1.1*R
        else:
            (x0,y0),_=newrandvertex(crudemesh,'null','crude',GRAIN,R)
            (x,y)=(GRAIN*x0,GRAIN*y0)
            R_stop=3*R
        while(int(mesh[M+x,M+y])==0 and x**2+y**2<(R_stop)**2):
            (x,y)=(x+randstep(),y+randstep())
        first=False
    return ((x,y),int(mesh[M+x,M+y])-1) 


