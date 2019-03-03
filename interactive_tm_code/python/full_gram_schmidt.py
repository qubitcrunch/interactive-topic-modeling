import sys
import random_projection as rp
from numpy.random import RandomState
import numpy as np
from anchors import findAnchors
import scipy.sparse as sparse
import time
from Q_matrix import generate_Q_matrix
import scipy.io

class Params:
    seed = 100
    new_dim = 1000
    checkpoint_prefix=None
    max_threads = 8
    eps = 10e-7
    anchor_thresh = 10
params = Params()

infile = file("../tmp/cnn.mat.trunc.mat")
M = scipy.io.loadmat(infile)['M']
print "identifying candidate anchors"
candidate_anchors = []
#only accept anchors that appear in a significant number of docs
for i in xrange(M.shape[0]):
    if len(np.nonzero(M[i, :])[1]) > params.anchor_thresh:
        candidate_anchors.append(i)

print len(candidate_anchors), "candidates"
#forms Q matrix from document-word matrix
Q = generate_Q_matrix(M)
vocab = file("../../anchor_word_objects/vocabulary").read().strip().split()

#check that Q sum is 1 or close to it
print "Q sum is", Q.sum()
V = Q.shape[0]
print "done reading documents"
anchors = findAnchors(Q, 2000, params, candidate_anchors)
np.savetxt("../../anchor_word_objects/anchor_words_GS_RP_15000", anchors)


infile = file("../../anchor_word_objects/Q")
num_words = len(vocab)
output_matrix = scipy.sparse.lil_matrix((num_words,num_words))
print "loading Q matrix"
for l in infile:
    d, w, v = [int(x) for x in l.split()]
    output_matrix[w-1, d-1] = v

Q    = np.array(np.transpose(output_matrix.todense()))
Q          = Q/Q.sum()
print "sum of Q is", Q.sum()
anchors = findAnchors(Q, 2000, params, candidate_anchors)
np.savetxt("../../anchor_word_objects/anchor_words_orig_GS_RP_1000", anchors)



