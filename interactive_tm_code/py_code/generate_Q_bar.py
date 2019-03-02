import sys
import random_projection as rp
from numpy.random import RandomState
import numpy as np
from fastRecover import do_recovery
from anchors import findAnchors
import scipy.sparse as sparse
import time
from Q_matrix import generate_Q_matrix 
import scipy.io
import scipy.sparse


infile = sys.argv[1]
outfile  = sys.argv[2]
print outfile
print "loading .mat file"
M = scipy.io.loadmat(infile)['M']
print "loaded M"

Q = generate_Q_matrix(M)
row_sums = Q.sum(1)
for i in xrange(len(Q[:, 0])):
	Q[i, :] = Q[i, :]/float(row_sums[i])
 

print Q.shape
#print A.shape
sQ = sparse.csr_matrix(Q)
print sQ.shape
#print sA.shape()
scipy.io.mmwrite(outfile+".mmx",sQ)
#np.savetxt(outfile,Q)
#