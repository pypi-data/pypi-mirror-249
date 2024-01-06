from mopsy import sparse_append
from scipy.sparse import eye
import numpy as np

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_sparse_add_row():
    mat = eye(5).tocsr()
    tmat = sparse_append(mat, np.array([0, 0, 0, 0, 0]), axis=0)

    assert tmat is not None
    assert tmat.shape[0] == mat.shape[0] + 1
    assert type(tmat) == type(mat)


def test_sparse_add_col():
    mat = eye(5).tocsr()
    tmat = sparse_append(mat, np.array([[0], [0], [0], [0], [0]]), axis=1)

    assert tmat is not None
    assert tmat.shape[1] == mat.shape[1] + 1
    assert type(tmat) == type(mat)
