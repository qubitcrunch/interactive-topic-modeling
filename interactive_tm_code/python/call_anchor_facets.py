import sys
import numpy as np
from anchors import findAnchors
import scipy.sparse as sparse
from Q_matrix import generate_Q_matrix
import scipy.io
from anchor_facets import tandem_anchors, exponentiated_gradient, recover_topics
import json


#parse input args
infile = sys.argv[1]
facet_group_file = sys.argv[2]
outfile = sys.argv[3]


M = scipy.io.loadmat(infile)['M']
Q = generate_Q_matrix(M)
print "Q sum is", Q.sum()


with open(facet_group_file) as f:
	anchor_list=json.load(f)

print anchor_list

#anchors = range(Q_glob.shape[0],Q_glob.shape[0]+len(anchor_list))


print "calculating tandem anchors"
facets = tandem_anchors(anchor_list, Q)
print facets.shape


print "recovering ..."
A, topic_likelihoods = recover_topics(Q, facets)

np.savetxt(outfile+".A", A)
np.savetxt(outfile+".topic_likelihoods", topic_likelihoods)
