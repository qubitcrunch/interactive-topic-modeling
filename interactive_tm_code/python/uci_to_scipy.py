import sys
import scipy.io
import scipy
import numpy as np

def uci_to_scipy(input_matrix):
	"""
    input_matrix: the file of the matrix in uci format
	"""
	infile = file(input_matrix)
	num_docs = int(infile.readline())
	num_words = int(infile.readline())
	nnz = int(infile.readline())
	output_matrix = scipy.sparse.lil_matrix((num_words, num_docs))
	for l in infile:
		d, w, v = [int(x) for x in l.split()]
		output_matrix[w-1, d-1] = v
	
	return(output_matrix)

