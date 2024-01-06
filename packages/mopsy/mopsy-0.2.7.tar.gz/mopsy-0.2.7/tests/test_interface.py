import numpy as np
from mopsy import apply, multi_apply
from scipy.sparse import eye
from statistics import mean

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"

mat = eye(5).tocoo()
group = ["col1", "col2", "col1", "col2", "col2"]


def test_apply_cols():
    tmat = apply(mean, mat, 1, None, False)
    assert tmat is not None


def test_multiapply_cols():
    rmat = multi_apply([mean], mat, 1, None, False)
    assert rmat is not None
