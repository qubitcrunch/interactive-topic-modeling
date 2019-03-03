import errno
import functools
import os
import pickle

import numpy as np

try:
    import numba
    jit = functools.partial(numba.jit, nopython=True)
except ImportError:
    jit = lambda x:x


@jit
def logsumexp(y):
    """Computes the log of the sum of exponentials of y in a numerically stable
    way. Useful for computing sums in log space.
    """
    ymax = y.max()
    return ymax + np.log((np.exp(y - ymax)).sum())


@jit
def lim_plogp(p):
    if not p:
        return 0
    return p * np.log(p)


@jit
def lim_xlogy(x, y):
    if not x and not y:
        return 0
    return x * np.log(y)


def sample_categorical(counts):
    """Samples from a categorical distribution parameterized by unnormalized
    counts. The index of the sampled category is returned.
    """
    sample = np.random.uniform(0, sum(counts))
    for key, count in enumerate(counts):
        if sample < count:
            return key
        sample -= count
    raise ValueError(counts)


def sample_categorical_np(counts):
    return np.random.choice(len(counts), p=np.array(counts)/sum(counts))


def random_projection(A, k):
    """Randomly projects the points (rows) of A into k-dimensions.
    We follow the method given by Achlioptas 2001 which guarantees that
    pairwise distances will be preserved within some epsilon, and is more
    efficient than projections involving sampling from Gaussians.
    """
    R = np.random.choice([-1, 0, 0, 0, 0, 1], (A.shape[1], k))
    return np.dot(A, R * np.sqrt(3))


def ensure_dir(path):
    """Ensures that a directory exists, creating it if it doesn't."""
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def pickle_cache(pickle_path):
    """Decorating for caching a parameterless function to disk via pickle"""
    def _decorator(data_func):
        @functools.wraps(data_func)
        def _wrapper():
            if os.path.exists(pickle_path):
                return pickle.load(open(pickle_path, 'rb'))
            data = data_func()
            pickle.dump(data, open(pickle_path, 'wb'))
            return data
        return _wrapper
    return _decorator