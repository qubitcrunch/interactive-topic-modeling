import numpy as np
import scipy.sparse
import scipy.io
import sys

def truncate_vocabulary(input_matrix,full_vocab,cutoff,stopwords_file):
    """
    input matrix: Matrix in scipy format
    vocab file: file with full vocabulary
    cutoff: cutoff for the number of distinct documents that each word appears in
    stopwords_file: a file with stop words
    """
    
    # Read in the vocabulary and build a symbol table mapping words to indices
    table = dict()
    numwords = 0
    with open(full_vocab, 'r') as file:
        for line in file:
            table[line.rstrip()] = numwords
            numwords += 1

    remove_word = [False]*numwords
    # Read in the stopwords
    with open(stopwords_file, 'r') as file:
        for line in file:
            if line.rstrip() in table:
                remove_word[table[line.rstrip()]] = True
    # Load previously generated document 
    #S = scipy.io.loadmat(input_matrix)
    #M = S['M']

    if input_matrix.shape[0] != numwords:
        print 'Error: vocabulary file has different number of words', input_matrix.shape, numwords
        sys.exit()
    print 'Number of words is ', numwords
    print 'Number of documents is ', input_matrix.shape[1]

    input_matrix = input_matrix.tocsr()
    new_indptr = np.zeros(input_matrix.indptr.shape[0], dtype=np.int32)
    new_indices = np.zeros(input_matrix.indices.shape[0], dtype=np.int32)
    new_data = np.zeros(input_matrix.data.shape[0], dtype=np.float64)

    indptr_counter = 1
    data_counter = 0

    for i in xrange(input_matrix.indptr.size - 1):
        #if this is not a stopword
        if not remove_word[i]:
            # start and end indices for row i
            start = input_matrix.indptr[i]
            end = input_matrix.indptr[i + 1]
        
            # if number of distinct documents that this word appears in is >= cutoff
            if (end - start) >= cutoff:
                new_indptr[indptr_counter] = new_indptr[indptr_counter-1] + end - start
                new_data[new_indptr[indptr_counter-1]:new_indptr[indptr_counter]] = input_matrix.data[start:end]
                new_indices[new_indptr[indptr_counter-1]:new_indptr[indptr_counter]] = input_matrix.indices[start:end]
                indptr_counter += 1
            else:
                remove_word[i] = True

    new_indptr = new_indptr[0:indptr_counter]
    new_indices = new_indices[0:new_indptr[indptr_counter-1]]
    new_data = new_data[0:new_indptr[indptr_counter-1]]

    output_matrix = scipy.sparse.csr_matrix((new_data, new_indices, new_indptr))
    output_matrix = output_matrix.tocsc()
    #scipy.io.savemat(output_matrix, {'M' : M}, oned_as='column')

    print 'New number of words is ', output_matrix.shape[0]
    print 'New number of documents is ', output_matrix.shape[1]

    # Output the new vocabulary
    output_vocab = []
    row = 0
    with open(full_vocab, 'r') as file:
        for line in file:
            if not remove_word[row]:
                output_vocab.append(line)
            row += 1
    
    return(output_matrix,output_vocab)
