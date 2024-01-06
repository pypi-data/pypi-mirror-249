from itertools import groupby
from typing import Any, Callable, Optional, Sequence, Tuple, Union

import numpy as np

from .checkutils import check_axis

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


class Mops:
    """Base class for all matrix operations."""

    def __init__(self, mat, non_zero: bool = False) -> None:
        """Intialize the matrix.

        Args:
            mat:
                Input matrix.

            non_zero:
                Whether to filter zero values.
                Defaults to False.
        """
        self.matrix = mat
        self.non_zero = non_zero

    def groupby_indices(self, group: Sequence) -> dict:
        """From a group vector, get the list of indices that map to each group.

        Args:
            group:
                Group vector, expected to ne the same as the
                number of rows or column.

        Returns:
            A dictionary with each group name as the key and the values containing
            the list of indices that map to it.
        """
        return {
            k: [x[0] for x in v]
            for k, v in groupby(
                sorted(enumerate(group), key=lambda x: x[1]), lambda x: x[1]
            )
        }

    def _apply(self, func: Callable[[list], Any], axis: Union[int, bool]):
        if self.non_zero:

            def funcwrapper(mat):
                tmat = mat[mat != 0]
                return func(tmat) if len(tmat) > 0 else 0

            return np.apply_along_axis(funcwrapper, axis, self.matrix)

        return np.apply_along_axis(func, axis, self.matrix)

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

        Returns:
            A tuple of matrix and its labels.
        """

        check_axis(axis)

        result = None
        rgroups = None
        try:
            if group is None:
                tmat = self._apply(func, axis=axis)
                result = tmat[np.newaxis] if axis == 0 else tmat[np.newaxis].T
            else:
                rgroups = []
                result = []
                for kcat, kmat in self.iter(group, axis):
                    tmat = kmat._apply(func, axis=axis)
                    result.append(tmat)
                    rgroups.append(kcat)
                result = np.stack(result, axis=axis)
        except Exception as e:
            raise Exception(f"Error: applying function: {str(e)}")

        return result, rgroups

    def multi_apply(
        self,
        funcs: Sequence[Callable[[list], Any]],
        group: list = None,
        axis: int = 0,
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

        Returns:
            A tuple of matrix and its labels.
        """

        check_axis(axis)

        result = None
        rgroups = None
        try:
            if group is None:
                tmats = [self._apply(f, axis=axis) for f in funcs]
                nmats = [x[np.newaxis] if axis == 0 else x[np.newaxis].T for x in tmats]
                result = nmats
            else:
                rgroups = []
                tmats = []
                for kcat, kmat in self.iter(group, axis):
                    tmats.append([kmat._apply(f, axis=axis) for f in funcs])
                    rgroups.append(kcat)

                nmats = []
                for smats in zip(*tmats):
                    nmats.append(np.stack(smats, axis=axis))

                result = nmats

        except Exception as e:
            raise Exception(f"Error: applying function: {str(e)}")

        return result, rgroups
