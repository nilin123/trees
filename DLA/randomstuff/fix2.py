import numpy as np

[V,N,parent,mesh,crudemesh]=np.load('data/fixed.npy',allow_pickle=True)
N[0].remove(0)
parent[0]='null'
np.save('data/fixed',[V,N,parent,mesh,crudemesh])
