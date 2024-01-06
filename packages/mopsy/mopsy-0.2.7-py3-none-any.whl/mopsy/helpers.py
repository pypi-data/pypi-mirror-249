from statistics import mean, median
from typing import Callable, Sequence, Union

import numpy
import scipy

from .checkutils import check_axis
from .utils import get_matrix_type

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def colsum(
    mat: Union[numpy.ndarray, scipy.sparse.spmatrix],
    group: Sequence = None,
    non_zero: bool = False,
) -> numpy.ndarray:
    """Apply column sum.

    Args:
        mat:
            Input matrix.

        group:
            Group vector, must be the same length as the number
            of columns.
            Defaults to None.

        non_zero:
            Whether to filter zero values.
            Defaults to False.

    Returns:
        A matrix with the column sums.
    """
    return apply(sum, mat, group=group, axis=1, non_zero=non_zero)


def rowsum(
    mat: Union[numpy.ndarray, scipy.sparse.spmatrix],
    group: Sequence = None,
    non_zero: bool = False,
) -> numpy.ndarray:
    """Apply row sum.

    Args:
        mat:
            Input matrix.

        group:
             Group vector, must be the same length as the number
            of rows. Defaults to None.

        non_zero:
            Whether to filter zero values.
            Defaults to False.

    Returns:
        A matrix with the row sums.
    """
    return apply(sum, mat, group=group, axis=0, non_zero=non_zero)


def colmean(
    mat: Union[numpy.ndarray, scipy.sparse.spmatrix],
    group: Sequence = None,
    non_zero: bool = False,
) -> numpy.ndarray:
    """Apply column mean.

    Args:
        mat:
            Input matrix.

        group:
            Group vector, must be the same length as the number
            of columns. Defaults to None.

        non_zero:
            Whether to filter zero values.
            Defaults to False.

    Returns:
        A matrix with the column means.
    """
    return apply(mean, mat, group=group, axis=1, non_zero=non_zero)


def rowmean(
    mat: Union[numpy.ndarray, scipy.sparse.spmatrix],
    group: Sequence = None,
    non_zero: bool = False,
) -> numpy.ndarray:
    """Apply row mean.

    Args:
        mat:
            Input matrix.

        group:
            Group vector, must be the same length as the number
            of rows. Defaults to None.

        non_zero:
            Whether to filter zero values.
            Defaults to False.

    Returns:
        A matrix with the row means.
    """
    return apply(mean, mat, group=group, axis=0, non_zero=non_zero)


def colmedian(
    mat: Union[numpy.ndarray, scipy.sparse.spmatrix],
    group: Sequence = None,
    non_zero: bool = False,
) -> numpy.ndarray:
    """Apply column median.

    Args:
        mat:
            Input matrix.

        group:
            Group vector, must be the same length as the number
            of columns. Defaults to None.

        non_zero:
            Whether to filter zero values.
            Defaults to False.

    Returns:
        A matrix with the column medians.
    """
    return apply(median, mat, group=group, axis=1, non_zero=non_zero)


def rowmedian(
    mat: Union[numpy.ndarray, scipy.sparse.spmatrix],
    group: Sequence = None,
    non_zero: bool = False,
) -> numpy.ndarray:
    """Apply row median.

    Args:
        mat:
            Input matrix.

        group:
            Group vector, must be the same length as the number
            of rows. Defaults to None.

        non_zero:
            Whether to filter zero values.
            Defaults to False.

    Returns:
        A matrix with the row medians.
    """
    return apply(median, mat, group=group, axis=0, non_zero=non_zero)


def apply(
    func: Callable,
    mat: Union[numpy.ndarray, scipy.sparse.spmatrix],
    axis: Union[int, bool],
    group: Sequence = None,
    non_zero: bool = False,
):
    """A generic `apply` function.

    Args:
        func:
            Function to apply over the groups.

        mat:
            Input matrix.

        group:
            Group vector, must be the same length as the number
            of rows or columns depending on the axis.
            Defaults to None.

        axis:
            0 for rows, 1 for columns.

        non_zero:
            Whether to filter zero values. Defaults to False.

    Returns:
        A matrix containing the result of the function.
    """
    check_axis(axis)

    tmat = get_matrix_type(mat, non_zero=non_zero)
    return tmat.apply(func, group=group, axis=axis)


def multi_apply(
    funcs: Sequence[Callable],
    mat: Union[numpy.ndarray, scipy.sparse.spmatrix],
    axis: Union[int, bool],
    group: Sequence = None,
    non_zero: bool = False,
):
    """A generic `multi_apply` to apply multiple function over the subset matrices.

    Args:
        func:
            List of function to apply over the groups.

        mat:
            Input matrix.

        group:
            Group vector, must be the same length as the number
            of rows or columns depending on the axis.
            Defaults to None.

        axis:
            0 for rows, 1 for columns.

        non_zero:
            Whether to filter zero values. Defaults to False.

    Returns:
        A list of matrices, in the same order as the functions
        containing the result of each the function.
    """
    check_axis(axis)

    tmat = get_matrix_type(mat, non_zero=non_zero)
    return tmat.multi_apply(funcs, group=group, axis=axis)
