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

#parse input args
if len(sys.argv) > 6:
    infile = sys.argv[1]
    settings_file = sys.argv[2]
    vocab_file = sys.argv[3]
    K = int(sys.argv[4])
    loss = sys.argv[5]
    outfile = sys.argv[6]
    anchorfile = sys.argv[7]

else:
    print "usage: ./learn_topics.py word_doc_matrix settings_file vocab_file K loss output_filename"
    print "for more info see readme.txt"
    sys.exit()

params = Params(settings_file)
params.dictionary_file = vocab_file

print "loading .mat file"
M = scipy.io.loadmat(infile)['M']

#forms Q matrix from document-word matrix
Q = generate_Q_matrix(M)
vocab = file(vocab_file).read().strip().split()

#Q_bar = Q
#row_sums_full = Q_bar.sum(1)
#for i in xrange(len(Q_bar[:, 0])):
#    Q_bar[i, :] = Q_bar[i, :]/float(row_sums_full[i])


#check that Q sum is 1 or close to it
print "Q sum is", Q.sum()
V = Q.shape[0]
print "done reading documents"


anchor_words = file(anchorfile).read().strip().split()
print len(anchor_words)

anchors = []
for w in anchor_words:
    anchors.append(vocab.index(w))

Q_rows = Q[np.array(anchors),:]
Q_anchors = Q_rows[:,np.array(anchors)]
print Q_anchors.shape
row_sums = Q_anchors.sum(1)
for i in xrange(len(Q_anchors[:, 0])):
    Q_anchors[i, :] = Q_anchors[i, :]/float(row_sums[i])

print "anchors are:"
for i, a in enumerate(anchors):
    print i, vocab[a]

#recover topics
A, C, topic_likelihoods = do_recovery(Q, anchors, loss, params)
print "done recovering"

np.savetxt(outfile+".A", A)
np.savetxt(outfile+".C", C)
np.savetxt(outfile+".topic_likelihoods", topic_likelihoods)
np.savetxt(outfile+".Q_anchors", Q_anchors)
np.savetxt(outfile+".Q", Q)
anchors_file = file(outfile+".anchors", 'w')
K = len(anchors)
for k in xrange(K):
    print>>anchors_file,vocab[anchors[k]]
