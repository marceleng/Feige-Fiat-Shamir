'''
Created on Dec 18, 2014

@author: marcel
'''
from prover import ffs_prover,dishonest_ffs_prover
from verifier import ffs_verifier
import sys

if len(sys.argv) < 5:
    print "Wrong number of arguments"
    exit()

mode=sys.argv[1]
n=int(sys.argv[2])
k=int(sys.argv[3])
t=int(sys.argv[4])

if mode=='prover':
    prover=ffs_prover(n,k,t)
    prover.run(42424)
elif mode=='verifier':
    verifier=ffs_verifier(n,k,t)
    verifier.listen(42424)
elif mode=='cheater':
    cheater=dishonest_ffs_prover(n,k,t)
    cheater.run(42424)
else:
    print "Wrong argument"