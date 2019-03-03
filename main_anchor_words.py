import sys
import interactive_tm_code.python.random_projection as rp
from numpy.random import RandomState
import numpy as np
from interactive_tm_code.python.fastRecover import do_recovery
from interactive_tm_code.python.anchors import findAnchors
import scipy.sparse as sparse
import time
from interactive_tm_code.python.Q_matrix import generate_Q_matrix 
import scipy.io
from interactive_tm_code.python.uci_to_scipy import *
from interactive_tm_code.python.truncate_vocabulary import *
from argparse import ArgumentParser


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


parser = ArgumentParser("Anchor word based topic modeling")
parser.add_argument("--settings_file", required=True, help="A file containing various settings.")
parser.add_argument("--uci_file", required=True, help="A file with the documents in uci format.")
parser.add_argument("--full_vocab_file", required=True, help="A file with the full vocabulary.")
parser.add_argument("--cut_off", required=True,type=int,help="Cutoff for the number of distinct documents that each word appears in.")
parser.add_argument("--stopwords_file", required=True,help="A file containing stopwords.")
parser.add_argument("--num_anchors", required=True,type=int,help="The number of anchor words.")
parser.add_argument("--recovery", required=True,type=lambda x: (str(x).lower() == 'true'),help="Boolean argument to perform recovery.")
parser.add_argument("--loss", required=False,type=str,help="Optional, the loss to be used in recovery. Default is L2.",default="L2")
parser.add_argument("--out_file", required=True,help="An output file string.")
parser.add_argument("--save_trunc", required=False,type=lambda x: (str(x).lower() == 'true'),default=False,help="Optional, a boolean argument to save the truncated bow matrix vocab.")
parser.add_argument("--save_Q", required=False,type=lambda x: (str(x).lower() == 'true'),default="False",help="Optinal, a boolean argument to save the full Q (word by word) matrix.")


args = parser.parse_args()
settings_file = args.settings_file
input_matrix  = args.uci_file
full_vocab = args.full_vocab_file
cutoff = args.cut_off
stopwords = args.stopwords_file
K = args.num_anchors
recovery =args.recovery
loss = args.loss
outfile = args.out_file
savetrunc = args.save_trunc
saveQ = args.save_Q


params = Params(settings_file)

print("Creating data in scipy format ...")
M_in = uci_to_scipy(input_matrix)

print("Truncating vocabulary ...")
M_out, vocab_out =  truncate_vocabulary(M_in,full_vocab,cutoff,stopwords)
params.dictionary = vocab_out

if savetrunc:
    print("Saving truncated objects ...")
    scipy.io.savemat(outfile+".M.trunc", {'M' : M_out}, oned_as='column')
    trunc_file = file(outfile+".vocab.trunc", 'w')
    for w in vocab_out:
        print>>trunc_file,w
    
print("Identifying candidate anchors ...")
candidate_anchors = []
#only accept anchors that appear in a significant number of docs
for i in xrange(M_out.shape[0]):
    if len(np.nonzero(M_out[i, :])[1]) > params.anchor_thresh:
        candidate_anchors.append(i)

print("Found " + str(len(candidate_anchors)) + " candidates.")

print("Computing Q ...")
Q = generate_Q_matrix(M_out)
print("Q sum is "+ str(Q.sum()))

#find anchors- this step uses a random projection
#into low dimensional space
print("Finding anchors ...")
anchors = findAnchors(Q, K, params, candidate_anchors)

anchors_file = file(outfile+".anchors", 'w')
for k in xrange(K):
    print>>anchors_file,vocab_out[anchors[k]]

Q_S = Q[np.array(anchors),:]
np.savetxt(outfile+".Q_anchors", Q_S)

#recover topics
if recovery:
    print ("Starting recovery ...")
    A, C, topic_likelihoods = do_recovery(Q, anchors, loss, params)
    print ("Done recovering.")

    np.savetxt(outfile+".A", A)
    np.savetxt(outfile+".C", C)
    np.savetxt(outfile+".topic_likelihoods", topic_likelihoods)

    #display
    f = file(outfile+".topwords", 'w')
    for k in xrange(K):
        topwords = np.argsort(A[:, k])[-params.top_words:][::-1]
        print vocab_out[anchors[k]], ':',
        print >>f, vocab_out[anchors[k]], ':',
        for w in topwords:
            print vocab_out[w],
            print >>f, vocab_out[w],
        print ""
        print >>f, ""
