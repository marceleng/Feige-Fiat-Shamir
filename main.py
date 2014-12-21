'''
Created on Dec 18, 2014

@author: marcel
'''
from prover import ffs_prover,dishonest_ffs_prover
from verifier import ffs_verifier
import sys

if len(sys.argv) < 2:
    print "Wrong number of arguments"
    exit()

mode=sys.argv[1]
n=int(sys.argv[2])
k=int(sys.argv[3])

if mode=='prover':
    prover=ffs_prover(n,k)
    prover.run(42424)
elif mode=='verifier':
    t=int(sys.argv[4])
    verifier=ffs_verifier(n,k,t)
    verifier.listen(42424)
elif mode=='cheater':
    cheater=dishonest_ffs_prover(n,k)
    cheater.run(42424)
else:
    print "Wrong argument"
