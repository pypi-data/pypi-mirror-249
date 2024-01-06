from typing import Union

import numpy as np
import scipy as sp

from .checkutils import check_axis
from .sops import Sops

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def append_row(
    mat: sp.sparse.spmatrix, row: Union[sp.sparse.spmatrix, np.ndarray]
) -> sp.sparse.spmatrix:
    """A generic append function for sparse matrices.

    Args:
        mat:
            Sparse matrix.
        row:
            Rows to append.

    Raises:
        TypeError:
            If axis is neither 0 nor 1.

    Returns:
        A new sparse matrix, usually the same type as the input matrix.
    """
    return sparse_append(mat=mat, row_or_column=row, axis=0)


def append_col(
    mat: sp.sparse.spmatrix, col: Union[sp.sparse.spmatrix, np.ndarray]
) -> sp.sparse.spmatrix:
    """A generic append function for sparse matrices.

    Args:
        mat:
            Sparse matrix.

        col:
            Columns to append.

    Raises:
        TypeError:
            If axis is neither 0 nor 1.

    Returns:
        A new sparse matrix, usually the same type as the input matrix.
    """
    return sparse_append(mat=mat, row_or_column=col, axis=1)


def sparse_append(
    mat: sp.sparse.spmatrix,
    row_or_column: Union[sp.sparse.spmatrix, np.ndarray],
    axis: Union[int, bool],
) -> sp.sparse.spmatrix:
    """A generic append function for sparse matrices.

    Args:
        mat:
            Sparse matrix.

        row_or_column:
            Rows or columns to append.

        axis:
            0 for rows, 1 for columns.

    Raises:
        TypeError:
            If axis is neither 0 nor 1.

    Returns:
        A new sparse matrix, usually the same type as the input matrix.
    """

    if not isinstance(mat, sp.sparse.spmatrix):
        raise TypeError(f"mat is not a sparse matrix. provided {type(mat)}")

    check_axis(axis)

    original_sparse_type = Sops.identify_sparse_type(mat)

    new_mat = None
    if axis == 0:
        if mat.shape[0] != row_or_column.shape[0]:
            raise TypeError(
                "Matrix and new row do not have the same shape along the first dimension."
            )

        new_mat = sp.sparse.vstack([mat, row_or_column])
    else:
        if mat.shape[1] != row_or_column.shape[0]:
            raise TypeError(
                "Matrix and new row do not have the same shape along the second dimension."
            )

        new_mat = sp.sparse.hstack([mat, row_or_column])

    if new_mat is None:
        raise Exception("This should never happen")

    cmat = Sops.convert_sparse_type(new_mat, original_sparse_type)
    return cmat
