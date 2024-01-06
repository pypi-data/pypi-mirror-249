from typing import Iterator, Sequence, Tuple, Union

import numpy as np

from .mops import Mops

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


class Nops(Mops):
    """Internal representation for numpy arrays."""

    def __init__(self, mat: np.ndarray, non_zero: bool = False) -> None:
        super().__init__(mat, non_zero=non_zero)

    def iter(
        self, group: Sequence[str] = None, axis: Union[int, bool] = 0
    ) -> Iterator[Tuple]:
        """Iterator over groups and an axis.

        Args:
            group:
                Group variable. Defaults to None.

            axis:
                0 for rows, 1 for columns. Defaults to 0.

        Yields:
            A tuple (str, Nops) of group and the submatrix.
        """
        mat = self.matrix

        if group is None:
            yield (group, self)
        else:
            idx_groups = self.groupby_indices(group)
            for k, v in idx_groups.items():
                if axis == 0:
                    yield (
                        k,
                        Nops(
                            mat[v,],
                            self.non_zero,
                        ),
                    )
                else:
                    yield (k, Nops(mat[:, v], self.non_zero))
