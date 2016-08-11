import numpy as np


def remove_low_variance(X, low_variance_threshold=1e-4, axis=0):
    low_variance = X.var(axis=axis) < low_variance_threshold
    X[:, ~low_variance]
    return X


def normalize(X):
    zero_mean = X - X.mean()
    return (zero_mean + zero_mean.min()) / X.max()


def independent_columns(A, tol=1e-05):
    """
    Return an array composed of independent columns of A.

    Note the answer may not be unique; this function returns one of many
    possible answers.

    http://stackoverflow.com/q/13312498/190597 (user1812712)
    http://math.stackexchange.com/a/199132/1140 (Gerry Myerson)
    http://mail.scipy.org/pipermail/numpy-discussion/2008-November/038705.html
        (Anne Archibald)

    >>> A = np.array([(2,4,1,3),(-1,-2,1,0),(0,0,2,2),(3,6,2,5)])
     2  4  1  3
    -1 -2  1  0
     0  0  2  2
     3  6  2  5
    # try with checking the rank of matrices
    >>> independent_columns(A)
    np.array([[ 2, 1],
              [-1, 1],
              [ 0, 2],
              [ 3, 2]]), np.array([0, 2])
    """
    # TODO need a source for diag(R) > 0, being the independent indices of A
    Q, R = np.linalg.qr(A)
    independent = np.where(np.abs(R.diagonal()) > tol)[0]
    return A[:, independent], independent
