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

[V,N,MESH]=np.load("data/400.npy",allow_pickle=True)
n=len(V)
M=len(MESH[0])//2

def halftree(i0,j0):
    B={j0}
    S={j0}
    while(len(S)>0):
        S_new=set([])
        for i in S:
            S_new=set.difference(set.union(S_new,N[i]),set.union(B,{i0}))
        S=S_new
        B=set.union(B,S)
    return B 

def branch_verts(branch):
    (_,(S,j))=branch
    I=set(range(n))
    for i in S:
        I=set.intersection(I,halftree(i,j))
    return I
#   
def section_verts(section):
    (_,(a,b))=section
    thepath=path_verts(a,b)
    if len(thepath)<2:
        return set([]),thepath
    h1=halftree(a,thepath[1]);h2=halftree(b,thepath[-2])
    return set.intersection(h1,h2)
#
#
def path_verts(a,b):
    dist=[-1]*n
    S=[b]
    dist[b]=0
    t=1
    while(dist[a]==-1):
        S_new=set([])
        for i in S:
            for j in N[i]:
                if dist[j]==-1:
                    dist[j]=t
                    S_new.add(j)
        S=S_new
        t=t+1
    i=a
    totaldist=int(dist[a])
    thepath=[a]
    for t in range(totaldist):
        N_list=list(N[i])
        am=[dist[j] for j in N_list].index(totaldist-t-1)   
        i=N_list[am]
        thepath=thepath+[i]
    return thepath
#
def trisect_branch(branch):
    (_,(S,i))=branch
    S0=S
    i0=i
    VOL=len(branch_verts(branch))
    vlist=[i]
    branchvol=1000000000
    while(2*branchvol>VOL):
        cld=[j for j in N[i] if (j not in S)]
        if len(cld)==0:
            break
        cldvols=[len(halftree(i,j)) for j in cld]
        q=np.argmax(cldvols)
        S={i}
        i=cld[q]
        branchvol=cldvols[q]
        vlist=vlist+[i]
    if(len(vlist)==1):
            return [('point',i0)]
    return compress([('branch',(set.union(S0,{vlist[1]}),i0)),('section',(i0,vlist[-1])),('branch',({vlist[-2]},vlist[-1]))])

#
def trisect_section(section):
    _,(a,b)=section
    path=path_verts(a,b)
    if len(path)==2:
        return [('edge',(a,b))]
    l=len(path)
    weights=[len(branch_verts(('branch',({path[i-1],path[i+1]},path[i])))) for i in range(1,l-1)]
    WEIGHT=np.cumsum([0]+weights+[0])
    m=min([i for i,W in enumerate(WEIGHT) if W>WEIGHT[-1]/2])
    return compress([('section',(a,path[m])),('branch',({path[m-1],path[m+1]},path[m])),('section',(path[m],b))])
#
def compress(l):
    for i,(style,data) in enumerate(l):
        if style=='section':
            (a,b)=data
            if(a in N[b]):
                l[i]=('edge',data)
        if style=='branch' and data[0]==N[data[1]]:
            l[i]=('point',data[1])
    return l


def refine(subtree):
    (style,data)=subtree
    if style=='branch':
        return trisect_branch(subtree)
    elif style=='section':
        l=trisect_section(subtree)
        for i,(style,data) in enumerate(l):
            if style=='branch':
                lb=trisect_branch((style,data))
                del l[i]
                l=l+lb
        return l
    return [subtree]


def makeMT(L):
    P0=[('branch',(set([]),0))]
    MV=[P0]+[[]]*(L-1)
    # ME[l][i] is the position of the first child of i.
    ME=[[]]*(L-1)
    for l in range(1,L):
        for ST in MV[l-1]:
            P_ST=refine(ST)
            MV[l]=MV[l]+P_ST
            ME[l-1]=ME[l-1]+[range(len(MV[l])-len(P_ST),len(MV[l]))]
    return (MV,ME)


def rich(subtree):
    global N
    (style,data)=subtree
    richdata='null'
    if style=='section':
        [verts,mdata]=[section_verts(subtree),path_verts(data[0],data[1])]
    elif style=='branch':
        [verts,mdata]=[branch_verts(subtree),[data[1]]]
    elif style=='edge':
        [verts,mdata]=[{data[0],data[1]},[data[0],data[1]]]
    elif style=='point':
        [verts,mdata]=[{data},[data]]
    edges=[(i,j) for i in verts for j in N[i] if(j in verts and i<j)]

    return (style,(verts,edges),mdata)


fignum=int(input("Number of partitions: "))
name='data/'+str(input("save to data/___?___.npy: "))

MT=makeMT(fignum)
MV=MT[0]
richMV=[[rich(subtree) for subtree in P] for P in MV]
np.save(name,[V,N,(MT[0],richMV,MT[1])])


##
#def drawpartition(P,theax):
#    colors=['r','g','b']
#    #for (S,i,_) in branches:
#        #theax.scatter([V[i][0] for i in branch(S,i)],[V[i][1] for i in branch(S,i)],s=10,color=rnd.choice(colors))
#    for (style,data) in P:
#        if(style=='section' or style=='edge'):
#            path=path_verts(data[0],data[1])
#            section=list(section_verts((style,data)))
#            theax.scatter([V[i][0] for i in section],[V[i][1] for i in section],s=1,color='b',alpha=.3)
#            theax.scatter([V[data[0]][0],V[data[1]][0]],[V[data[0]][1],V[data[1]][1]],s=5,zorder=5,color='w')
#            theax.scatter([V[data[0]][0],V[data[1]][0]],[V[data[0]][1],V[data[1]][1]],s=2,zorder=5,color='r')
#            theax.plot([V[i][0] for i in path],[V[i][1] for i in path],color='b')
#        elif(style=='branch'):
#            branch=branch_verts((style,data))
#            theax.scatter([V[i][0] for i in branch],[V[i][1] for i in branch],s=1,color='r',alpha=.6)
#            theax.scatter([V[data[1]][0]],[V[data[1]][1]],s=5,zorder=5,color='w')
#            theax.scatter([V[data[1]][0]],[V[data[1]][1]],s=2,zorder=5,color='r')
#
#    return
#
#fig=plt.figure(figsize=(18,18))
#figdimlist={3:[1,3],4:[2,2],5:[1,5],6:[2,3]}
#figdims=figdimlist[fignum]
#
#FIGS=[fig.add_subplot(figdims[0],figdims[1],i+1) for i in range(fignum)]
#
#for i in range(fignum):
#    FIGS[i].axis('equal')
#    FIGS[i].set_axis_off()
#    drawpartition(MV[i],FIGS[i])
#
#plt.show()#block=False)
