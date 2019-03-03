import sys
import numpy as np
from anchors import findAnchors
import scipy.sparse as sparse
import time
from Q_matrix import generate_Q_matrix 
import scipy.io
from anchor_facets import tandem_anchors,exponentiated_gradient,recover_topics
import json


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
       
filename=sys.argv[1]

infile = sys.argv[2]
loss = sys.argv[3]
params = Params(filename)
outfile = "../py_code_output/result_"
print "loading .mat file"
M = scipy.io.loadmat(infile)['M']

#forms Q matrix from document-word matrix
Q_glob = generate_Q_matrix(M)
print "Q sum is", Q_glob.sum()


this_file ="../py_code_output/anchor_groups.json"

with open(this_file) as f:
    anchor_list=json.load(f)

anchors = range(Q_glob.shape[0],Q_glob.shape[0]+len(anchor_list))
print "calculating tandem anchors"
facets = tandem_anchors(anchor_list, Q_glob, corpus=None, epsilon=1e-10)
print facets.shape

#new_Q = np.vstack((Q_glob,facets))
#print new_Q.shape
#print "new_Q sum is", new_Q.sum()

print "recovering ..."
A,topic_likelihoods = recover_topics(Q_glob,facets)

np.savetxt(outfile+".A_facets", A)
#np.savetxt(outfile+".C", C)
np.savetxt(outfile+".topic_likelihoods_facets", topic_likelihoods)