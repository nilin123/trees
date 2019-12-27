import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.lines as mlines
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.collections import LineCollection
import math
import sys
import pdb

#################################################################
#### Explore tree constructed using make_tree.py
#### author: Nilin
#################################################################

#name=input("\n Load tree from file (exclude .npy): ")
#name="data/xs"
#[dims,paths]=np.load(name+".npy",allow_pickle=True)
#[dims,N]=np.load(name+".npy",allow_pickle=True)
[dims,Nc]=np.load("data/2d4_ball.npy",allow_pickle=True)
N=[[(v[0],v[1]) for v in Nc[i]] for i in range(dims[0]*dims[1])]

dim="2d"
print("_"*100+"\n")


#### N[DO(v)] is the set of neighbors of v.
#### DO=dictionary order
#N=[[]]*dims[0]*dims[1]
DO=lambda v:int(v[0]*dims[1]+v[1])

#for path in paths:
#    for t in range(1,len(path)):
#        v,w=(path[t-1],path[t])
#        vv=(v[0],v[1])
#        ww=(w[0],w[1])
#        N[DO(vv)]=N[DO(vv)]+[ww]
#        N[DO(ww)]=N[DO(ww)]+[vv]

vol=lambda V: sum([sum(col) for col in V])


def half(v0,v1):
    V=-1*np.ones(dims)
    S=[v1]
    V[v0]=-2;V[v1]=0
    t=0
    while(len(S)>0):
        S_new=[]
        for v in S:
            for w in N[DO(v)]:
                if V[w]==-1:
                    V[w]=t
                    S_new=S_new+[w]
        S=S_new
        t=t+1
    return [[int(V[(x,y)])>=0 for y in range(dims[1])] for x in range(dims[0])]

v0=(0,0)
while(len(set(N[DO(v0)]))<2):
    v0=(rnd.randint(dims[0]),rnd.randint(dims[1]))
w0=N[DO(v0)][0]
h11=half(v0,w0);h22=half(w0,v0)
whole=[[h11[i][j] or h22[i][j] for j in range(dims[1])] for i in range(dims[0])]

def branch(S,v):
    V=whole
    for w in S:
        h=half(w,v)
        V=[[V[i][j] and h[i][j] for j in range(dims[1])] for i in range(dims[0])]

    return V 
   
def hammock(v1,v2):
    thepath=path_between(v1,v2)
    if len(thepath)<2:
        return [[0]*dims[0]]*dims[1],thepath
    h1=half(v1,thepath[1]);h2=half(v2,thepath[-2])
    return [[h1[i][j] and h2[i][j] for j in range(dims[1])] for i in range(dims[0])],thepath


def path_between(v1,v2):
    dist=-1*np.ones(dims)
    S=[v2]
    dist[v2]=0
    t=1
    while(dist[v1]==-1):
        S_new=[]
        for v in S:
            #pdb.set_trace()
            for w in N[DO(v)]:
                if dist[w]==-1:
                    dist[w]=t
                    S_new=S_new+[w]
#                Nor=Nor+[(v,w)]
#        Normals=Normals+[Nor]
        S=S_new
        t=t+1
    v=v1
    totaldist=int(dist[v1])
    thepath=[v1]
    for t in range(totaldist):
        neighbors=N[DO(v)]
        whichnb=[dist[nb] for nb in neighbors].index(totaldist-t-1)   
        v=neighbors[whichnb]
        thepath=thepath+[v]
    return thepath

def cutbranch(S,v):
    VOL=vol(branch(S,v))
    vlist=[v]
    branchvol=1000000000
    #pdb.set_trace()
    while(2*branchvol>VOL):
        cld=[w for w in N[DO(v)] if(w not in S)]
        if len(cld)==0:
            break
        cldvols=[vol(half(v,w)) for w in cld]
        i=np.argmax(cldvols)
        S=[v]
        v=cld[i]
        branchvol=cldvols[i]
        vlist=vlist+[v]
    return vlist

fig=plt.figure(figsize=(21,7))


def drawfromV(charac,theax,thecolor):
    segments=[];bdsegments=[]
    for x in range(dims[0]):
        for y in range(dims[1]):
            if charac[x][y]:
                for w in N[DO((x,y,0))]:
                    if charac[w[0]][w[1]]:
                        segments=segments+[((x,y),(w[0],w[1]))]
    for x in range(dims[0]):
        for y in range(1,dims[1]):
            if charac[x][y-1]!=charac[x][y]:
                bdsegments=bdsegments+[((x-.5,y-.5),(x+.5,y-.5))]
    for x in range(1,dims[0]):
        for y in range(dims[1]):
            if charac[x-1][y]!=charac[x][y]:
                bdsegments=bdsegments+[((x-.5,y-.5),(x-.5,y+.5))]
    lc=LineCollection(segments,color=thecolor)
    bd=LineCollection(bdsegments,color='#ffffff',linewidth=9)
    bd2=LineCollection(bdsegments,color='#ff00ff',linewidth=1)
    theax.add_collection(lc)
    theax.add_collection(bd)
    theax.add_collection(bd2)

def halve(v_1,v_2):
    thepath=path_between(v_1,v_2)
    l=len(thepath)
    thesize=[0]*(l-1)
    for i in range(1,l-1):
        theslice=branch([thepath[i-1],thepath[i+1]],thepath[i])
        thesize[i]=thesize[i-1]+vol(theslice)
    j=0
    while 2*thesize[j]<thesize[-1]:
        j=j+1
    return thepath[j],[thepath[j-1],thepath[j+1]]

def drawhammock(vl,vr,theax,thecolor):
    H,thepath=hammock(vl,vr)
    #v1=thepath[0];v2=thepath[1];v3=thepath[-2];v4=thepath[-1]
    drawfromV(H,theax,'#00bb00')
    #theax.plot([v1[0],v2[0]],[v1[1],v2[1]],ls=':',color=thecolor)
    #theax.plot([v3[0],v4[0]],[v3[1],v4[1]],ls=':',color=thecolor)
    theax.plot([v[0] for v in thepath],[v[1] for v in thepath],color='#000000',linewidth=2)
    theax.scatter([vl[0],vr[0]],[vl[1],vr[1]],color='#000000',s=20,zorder=5)
    theax.scatter([vl[0],vr[0]],[vl[1],vr[1]],color='#ff00ff',s=10,zorder=6)




#
#v=(5,5)
#thehalf=half(N[DO(v)][0],v)
#
#ax=fig.add_subplot(121)
#ax.set_xlim(left=0,right=dims[0])
#ax.set_ylim(bottom=0,top=dims[1])
#drawfromV(thehalf,ax,'#0000ff')
#
#thebranch=branch(N[DO(v)],v)


def trisectb(S,v):
    thepath=cutbranch(S,v)
    if len(thepath)<2:
        return [[(S,v,'b')],[]]
    return [[(S+[thepath[1]],v,'b'),([thepath[-2]],thepath[-1],'b')],[(v,thepath[-1],'h')]]

def trisecth(v0,v1):
    (m,[m0,m1])=halve(v0,v1)
    return [[([m0,m1],m,'b')],[(v0,m,'h'),(m,v1,'h')]]

def trisectall(P):
    branches=P[0]
    hammocks=P[1]
    Pb_list=[trisectb(S,v) for (S,v,t) in branches]
    Ph_list=[trisecth(v,w) for (v,w,t) in hammocks]
    P_list=Pb_list+Ph_list
    P_new=[[],[]]
    for P_ in P_list:
        P_new[0]=P_new[0]+P_[0]
        P_new[1]=P_new[1]+P_[1]
    return P_new

ax=fig.add_subplot(131)
ax.set_xlim(left=0,right=dims[0])
ax.set_ylim(bottom=0,top=dims[1])
ay=fig.add_subplot(132)
ay.set_xlim(left=0,right=dims[0])
ay.set_ylim(bottom=0,top=dims[1])
az=fig.add_subplot(133)
az.set_xlim(left=0,right=dims[0])
az.set_ylim(bottom=0,top=dims[1])
#aw=fig.add_subplot(144)
#aw.set_xlim(left=0,right=dims[0])
#aw.set_ylim(bottom=0,top=dims[1])
#v1=(3,2)
S=[]
thepath=cutbranch(S,v0)
#x=[v[0] for v in thepath]
#y=[v[1] for v in thepath]
#ax.plot(x,y,color='#0000dd')

def randcolor():
    colorlist=['red','green','blue']
    return colorlist[rnd.randint(3)]

def drawpartition(P,theax):
    branches=P[0]
    hammocks=P[1]
    #pdb.set_trace()
    for (S,v,t) in branches:
        drawfromV(branch(S,v),theax,'#ff22cc')
    for (v,w,t) in hammocks:
        drawhammock(v,w,theax,'blue')

#drawfromV(branch(S+[thepath[1]],v0),ax,'red')
#drawhammock(thepath[0],thepath[-1],ax,'#00dd00')
#drawfromV(half(thepath[-2],thepath[-1]),ax,'blue')
#ax.scatter([x[0],x[-1]],[y[0],y[-1]],color='red')


P0=[[([],v0,'b')],[]]


P1=trisectall(P0)
P2=trisectall(P1)
P3=trisectall(P2)
drawpartition(P1,ax)
drawpartition(P2,ay)
drawpartition(P3,az)
#drawpartition(P3,aw)

#vl=(dims[0]//2.2,dims[1]//2.2);vr=(dims[0]//1.8,dims[0]//1.8)
#vm,S=halve(vl,vr)
#
#
#
#ay=fig.add_subplot(122)
#ay.set_xlim(left=0,right=dims[0])
#ay.set_ylim(bottom=0,top=dims[1])
#drawhammock(vl,vm,ay,'#ff0000')
#drawhammock(vm,vr,ay,'#00ff00')
#drawfromV(branch(S,vm),ay,'#0000ff')
#



plt.show()
