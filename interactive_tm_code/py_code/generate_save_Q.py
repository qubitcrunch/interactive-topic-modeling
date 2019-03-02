import sys
import numpy as np
from anchors import findAnchors
import scipy.sparse as sparse
import time
from Q_matrix import generate_Q_matrix 
import scipy.io
from anchor_facets import tandem_anchors,exponentiated_gradient,recover_topics
import json


infile = sys.argv[1]
outfile = sys.argv[2]

print "loading .mat file"
M = scipy.io.loadmat(infile)['M']

#forms Q matrix from document-word matrix
Q = generate_Q_matrix(M)
print "Q sum is", Q.sum()

np.savetxt(outfile+".Q", Q)
