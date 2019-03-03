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
#import rpy2.robjects as robjects

class Params:

    def __init__(self, filename):
        self.log_prefix=None
        self.checkpoint_prefix=None
        self.seed = int(time.time())

        for l in file(filename):
            if l == "\n" or l[0] == "#":
                continue
            l = l.strip()
            l = l.split('=')
            if l[0] == "log_prefix":
                self.log_prefix = l[1]
            elif l[0] == "max_threads":
                self.max_threads = int(l[1])
            elif l[0] == "eps":
                self.eps = float(l[1])
            elif l[0] == "checkpoint_prefix":
                self.checkpoint_prefix = l[1]
            elif l[0] == "new_dim":
                self.new_dim = int(l[1])
            elif l[0] == "seed":
                self.seed = int(l[1])
            elif l[0] == "anchor_thresh":
                self.anchor_thresh = int(l[1])
            elif l[0] == "top_words":
                self.top_words = int(l[1])



settings_file = sys.argv[1]
loss = sys.argv[2]
outfile= sys.argv[3]
#infile = sys.argv[4]
params = Params(settings_file)

#robjects.reval('Q_S <- get(load("../tmp/Q"))')
#robjects.reval('anchors <- get(load("../tmp_interactive_chris/anchor_inds"))')
#Q       = np.transpose(np.array(list(robjects.r.Q_S)).reshape(robjects.r.Q_S.dim))
#anchors = np.array(list(robjects.r.anchors)).tolist()

#infile = file("../tmp/Q_sparse.txt")
#num_words = int(open("../tmp/vocab_length.txt","r").read())
#output_matrix = scipy.sparse.lil_matrix((num_words,num_words))
#print "loading Q matrix"
#for l in infile:
#    d, w, v = [int(x) for x in l.split()]
#    output_matrix[w-1, d-1] = v

#Q	= np.array(np.transpose(output_matrix.todense()))
#M = scipy.io.loadmat(infile)['M']
#Q = generate_Q_matrix(M)
Q= np.loadtxt("../tmp/Q_matrix")
anchors	= np.loadtxt("../tmp/anchor_inds_copy.txt",dtype="int").tolist()
print anchors
#Q      	= Q/Q.sum()
print "sum of Q is", Q.sum()

print "recovering topics ..."
A, topic_likelihoods = do_recovery(Q, anchors, loss , params)
print "finished recovery"

np.savetxt(outfile+"A", A)
np.savetxt(outfile+"topic_likelihoods", topic_likelihoods)
