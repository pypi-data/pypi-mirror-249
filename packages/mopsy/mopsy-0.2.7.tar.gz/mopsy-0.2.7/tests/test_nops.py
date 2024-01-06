import numpy as np
from mopsy.nops import Nops
from scipy.sparse import eye
from statistics import mean

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"

mat = eye(5).toarray()
group = ["col1", "col2", "col1", "col2", "col2"]


def test_init():
    tmat = Nops(mat)
    assert tmat is not None


def test_group_iter_rows():
    tmat = Nops(mat)

    groups = tmat.iter(group, axis=0)
    assert sum(1 for _ in groups) == 2


def test_group_iter_cols():
    tmat = Nops(mat)

    groups = tmat.iter(group, axis=1)
    assert sum(1 for _ in groups) == 2


def test_group_apply_rows():
    tmat = Nops(mat)
    rmat, rgroups = tmat.apply(sum, group=group, axis=0)
    assert len(rgroups) == len(set(group))
    assert rmat.shape[0] == 2
    assert rmat.shape[1] == 5
    assert rmat[0, :].flatten().tolist() == [1.0, 0.0, 1.0, 0.0, 0.0]
    assert rmat[1, :].flatten().tolist() == [0.0, 1.0, 0.0, 1.0, 1.0]


def test_group_apply_cols():
    tmat = Nops(mat)
    rmat, rgroups = tmat.apply(sum, group=group, axis=1)
    assert len(rgroups) == len(set(group))
    assert rmat.shape[0] == 5
    assert rmat.shape[1] == 2
    assert rmat[:, 0].flatten().tolist() == [1.0, 0.0, 1.0, 0.0, 0.0]
    assert rmat[:, 1].flatten().tolist() == [0.0, 1.0, 0.0, 1.0, 1.0]


def test_group_apply_row_None():
    tmat = Nops(mat)
    rmat, rgroups = tmat.apply(sum, group=None, axis=0)
    assert rmat is not None
    assert rgroups is None
    assert rmat.shape[0] == 1
    assert rmat.shape[1] == 5
    assert rmat[:,].flatten().tolist() == [1.0, 1.0, 1.0, 1.0, 1.0]


def test_group_apply_col_None():
    tmat = Nops(mat)
    rmat, rgroups = tmat.apply(sum, group=None, axis=1)
    assert rmat is not None
    assert rgroups is None
    assert rmat.shape[0] == 5
    assert rmat.shape[1] == 1
    assert rmat[:,].flatten().tolist() == [1.0, 1.0, 1.0, 1.0, 1.0]


def test_multi_apply_rows_None():
    tmat = Nops(mat)
    rmat, rgroups = tmat.multi_apply([np.sum, np.mean], axis=0)
    assert rmat is not None
    assert rgroups is None
    assert len(rmat) == 2
    assert rmat[0].shape[0] == 1
    assert rmat[0].shape[1] == 5
    assert rmat[0].tolist() == [[1.0, 1.0, 1.0, 1.0, 1.0]]
    assert rmat[1].tolist() == [[0.2, 0.2, 0.2, 0.2, 0.2]]


def test_multi_apply_cols_None():
    tmat = Nops(mat)
    rmat, rgroups = tmat.multi_apply([np.sum, np.mean], axis=1)
    assert rmat is not None
    assert rgroups is None
    assert len(rmat) == 2
    assert rmat[0].shape[0] == 5
    assert rmat[0].shape[1] == 1
    assert rmat[0].tolist() == [[1.0], [1.0], [1.0], [1.0], [1.0]]
    assert rmat[1].tolist() == [[0.2], [0.2], [0.2], [0.2], [0.2]]


def test_multi_apply_rows():
    tmat = Nops(mat)
    rmat, rgroups = tmat.multi_apply([np.sum, np.mean], group=group, axis=0)
    assert rmat is not None
    assert len(rgroups) == len(set(group))
    assert len(rmat) == 2
    assert rmat[0].shape[0] == 2
    assert rmat[0].shape[1] == 5
    assert rmat[0].tolist() == [[1.0, 0.0, 1.0, 0.0, 0.0], [0.0, 1.0, 0.0, 1.0, 1.0]]
    assert rmat[1].tolist() == [
        [0.5, 0.0, 0.5, 0.0, 0.0],
        [0.0, 0.3333333333333333, 0.0, 0.3333333333333333, 0.3333333333333333],
    ]


def test_multi_apply_cols():
    tmat = Nops(mat)
    rmat, rgroups = tmat.multi_apply([np.sum, np.mean], group=group, axis=1)
    assert rmat is not None
    assert len(rgroups) == len(set(group))
    assert len(rmat) == 2
    assert rmat[0].shape[0] == 5
    assert rmat[0].shape[1] == 2
    assert rmat[0].tolist() == [
        [1.0, 0.0],
        [0.0, 1.0],
        [1.0, 0.0],
        [0.0, 1.0],
        [0.0, 1.0],
    ]
    assert rmat[1].tolist() == [
        [0.5, 0.0],
        [0.0, 0.3333333333333333],
        [0.5, 0.0],
        [0.0, 0.3333333333333333],
        [0.0, 0.3333333333333333],
    ]


def test_group_apply_rows_nnzero():
    tmat = Nops(mat, non_zero=True)
    rmat, rgroups = tmat.apply(sum, group=group, axis=0)
    assert len(rgroups) == len(set(group))
    assert rmat.shape[0] == 2
    assert rmat.shape[1] == 5
    assert rmat.tolist() == [[1.0, 0.0, 1.0, 0.0, 0.0], [0.0, 1.0, 0.0, 1.0, 1.0]]


def test_group_apply_cols_nnzero():
    tmat = Nops(mat, non_zero=True)
    rmat, rgroups = tmat.apply(sum, group=group, axis=1)
    assert len(rgroups) == len(set(group))
    assert rmat.shape[0] == 5
    assert rmat.shape[1] == 2
    assert rmat.tolist() == [[1.0, 0.0], [0.0, 1.0], [1.0, 0.0], [0.0, 1.0], [0.0, 1.0]]


def test_group_apply_rows_mean_nnzero():
    tmat = Nops(mat, non_zero=True)
    rmat, rgroups = tmat.apply(mean, group=group, axis=0)
    assert len(rgroups) == len(set(group))
    assert rmat.shape[0] == 2
    assert rmat.shape[1] == 5
    assert rmat.tolist() == [[1.0, 0.0, 1.0, 0.0, 0.0], [0.0, 1.0, 0.0, 1.0, 1.0]]


def test_group_apply_cols_mean_nnzero():
    tmat = Nops(mat, non_zero=True)
    rmat, rgroups = tmat.apply(mean, group=group, axis=1)
    assert len(rgroups) == len(set(group))
    assert rmat.shape[0] == 5
    assert rmat.shape[1] == 2
    assert rmat.tolist() == [[1.0, 0.0], [0.0, 1.0], [1.0, 0.0], [0.0, 1.0], [0.0, 1.0]]
