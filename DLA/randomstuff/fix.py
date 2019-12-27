import numpy as np

[V,_,parent,mesh,crudemesh]=np.load('data/all_the_data.npy',allow_pickle=True)
n=len(V)
N=['null']*n
for i in range(n):
    N[i]=set([])
for i in range(n):
    p=parent[i]
    N[p].add(i)
    N[i].add(p)
np.save('data/fixed',[V,N,parent,mesh,crudemesh])
