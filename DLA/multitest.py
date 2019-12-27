from multiprocessing import Pool
from defs import test
np=int(input("number of processes: "))
pool=Pool(np)
#def test(x):
#    return x*2

print(pool.map(test,[3.14,2,10]))

