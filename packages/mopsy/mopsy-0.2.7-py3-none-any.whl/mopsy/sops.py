from statistics import mean
from typing import Any, Callable, Iterator, Optional, Sequence, Tuple, Union

import numpy as np
from scipy import sparse as sp

from .mops import Mops
from .nops import Nops

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


class Sops(Mops):
    """Sops, Sparse Matrix Operation Class."""

    def __init__(self, mat: sp.spmatrix, non_zero: bool = False) -> None:
        """Initialize the class from a scipy sparse matrix.

        Args:
            mat:
                Input scipy sparse matrix.

            non_zero:
                Whether to filter zero values.
                Defaults to False.
        """
        super().__init__(mat, non_zero=non_zero)

    def iter(self, group: list = None, axis: Union[int, bool] = 0) -> Iterator[Tuple]:
        """Iterator over groups and an axis.

        Args:
            group:
                Group variable. Defaults to None.

            axis:
                0 for rows, 1 for columns. Defaults to 0.

        Yields:
            a tuple (str, matrix) of group and the submatrix.
        """
        mat = self.matrix.tocsr() if axis == 0 else self.matrix.tocsc()
        if group is None:
            yield (group, self)
        else:
            idx_groups = self.groupby_indices(group)
            for k, v in idx_groups.items():
                if axis == 0:
                    yield (
                        k,
                        Sops(
                            mat[v,],
                            self.non_zero,
                        ),
                    )
                else:
                    yield (k, Sops(mat[:, v], self.non_zero))

    def _apply(
        self, func: Callable[[list], Any], axis: Union[int, bool] = 0
    ) -> np.ndarray:
        mat = self.matrix.tocsc() if axis == 0 else self.matrix.tocsr()
        if self.non_zero:
            # reduction along an axis
            fmat = np.zeros(mat.shape[1] if axis == 0 else mat.shape[0])
            for i in range(len(mat.indptr) - 1):
                start_idx = mat.indptr[i]
                end_idx = mat.indptr[i + 1]
                if start_idx == end_idx:
                    fmat[i] = 0
                else:
                    mslice = mat.data[slice(start_idx, end_idx)]
                    fmat[i] = 0 if len(mslice) == 0 else func(mslice)

            return fmat if axis == 0 else fmat.T
        else:
            if func in [sum, mean, min, max]:
                if func == sum:
                    mat = mat.sum(axis=axis)
                elif func == mean:
                    mat = mat.mean(axis=axis)
                elif func == min:
                    mat = mat.min(axis=axis).todense()
                elif func == max:
                    mat = mat.max(axis=axis).todense()

                # flatten
                tmat = mat.getA1()
                return tmat if axis == 0 else tmat.T
            else:
                dense_mat = Nops(self.matrix.toarray(), self.non_zero)
                return dense_mat._apply(func, axis)

    def apply(
        self,
        func: Callable[[list], Any],
        group: Sequence = None,
        axis: Union[int, bool] = 0,
    ) -> Tuple[np.ndarray, Optional[Sequence]]:
        """Apply a function to groups along an axis.

        Args:
            func:
                List of function to apply over the groups.

            group:
                Group vector, must be the same length as the number
                of rows or columns depending on the axis.
                Defaults to None.

            axis:
                0 for rows, 1 for columns.

        Raises:
            Exception:
                ApplyFuncError, when a function cannot be applied.

        Returns:
            A tuple of matrix and its labels.
        """
        original_sparse_type = Sops.identify_sparse_type(self.matrix)
        mat, groups = super().apply(func, group, axis)

        cmat = Sops.convert_sparse_type(mat, original_sparse_type)

        return cmat, groups

    def multi_apply(
        self,
        funcs: Sequence[Callable[[list], Any]],
        group: list = None,
        axis: Union[int, bool] = 0,
    ) -> Tuple[np.ndarray, Optional[Sequence]]:
        """Apply multiple functions, the first axis of the ndarray specifies the results of the inputs functions in the
        same order.

        Args:
            func:
                List of function to apply over the groups.

            group:
                Group vector, must be the same length as the number
                of rows or columns depending on the axis.
                Defaults to None.

            axis:
                0 for rows, 1 for columns.

        Raises:
            Exception:
                ApplyFuncError, when a function cannot be applied.

        Returns:
            A tuple of matrix and its labels.
        """
        original_sparse_type = Sops.identify_sparse_type(self.matrix)
        mats, groups = super().multi_apply(funcs, group, axis)
        cmats = [Sops.convert_sparse_type(m, original_sparse_type) for m in mats]

        return cmats, groups

    @staticmethod
    def identify_sparse_type(mat: sp.spmatrix):
        """Identify the sparse matrix format.

        Args:
            mat:
                Input scipy matrix.

        Raises:
            TypeError:
                If matrix is not sparse.

        Returns:
            An internal matrix representation object
        """
        if not isinstance(mat, sp.spmatrix):
            raise TypeError(f"mat is not a sparse representation, it is {type(mat)}")

        if sp.isspmatrix_csc(mat):
            return "csc"
        elif sp.isspmatrix_csr(mat):
            return "csr"
        elif sp.isspmatrix_bsr(mat):
            return "bsr"
        elif sp.isspmatrix_coo(mat):
            return "coo"
        elif sp.isspmatrix_dia(mat):
            return "dia"
        elif sp.isspmatrix_dok(mat):
            return "dok"
        elif sp.isspmatrix_lil(mat):
            return "lil"

    @staticmethod
    def convert_sparse_type(mat: sp.spmatrix, format: str):
        """Convert to a sparse matrix format.

        Args:
            mat:
                A numpy or scipy matrix.

            format:
                Sparse matrix format, one of `identify_sparse_type()`.

        Raises:
            TypeError:
                If matrix is not sparse.

        Returns:
            An internal matrix representation object.
        """
        if isinstance(mat, np.ndarray):
            if format == "csc":
                return sp.csc_matrix(mat)
            elif format == "csr":
                return sp.csr_matrix(mat)
            elif format == "bsr":
                return sp.bsr_matrix(mat)
            elif format == "coo":
                return sp.coo_matrix(mat)
            elif format == "dia":
                return sp.dia_matrix(mat)
            elif format == "dok":
                return sp.dok_matrix(mat)
            elif format == "lil":
                return sp.lil_matrix(mat)
        elif isinstance(mat, sp.spmatrix):
            if format == "csc":
                return mat.tocsc()
            elif format == "csr":
                return mat.tocsr()
            elif format == "bsr":
                return mat.tobsr()
            elif format == "coo":
                return mat.tocoo()
            elif format == "dia":
                return mat.todia()
            elif format == "dok":
                return mat.todok()
            elif format == "lil":
                return mat.tolil()
        else:
            raise Exception("unknown matrix format.")
