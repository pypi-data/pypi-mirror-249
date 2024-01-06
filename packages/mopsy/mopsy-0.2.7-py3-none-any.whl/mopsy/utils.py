from typing import Union

import numpy as np
import scipy.sparse as sp

from .nops import Nops
from .sops import Sops

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def get_matrix_type(mat: Union[np.ndarray, sp.spmatrix], non_zero: bool = False):
    """Get an internal matrix state.

    Args:
        mat:
            An input numpy or scipy matrix.

        non_zero:
            Whether to filter zero value. Defaults to False.

    Raises:
        Exception:
            TypeNotSupported, when the matrix type is not supported.

    Returns:
        An internal matrix representation object.
    """
    if isinstance(mat, np.ndarray):
        return Nops(mat, non_zero=non_zero)

    if isinstance(mat, sp.spmatrix):
        return Sops(mat, non_zero=non_zero)

    # TODO: zarr, xarray, idk what else, pandas df/sparsedf ?

    raise TypeError(f"mat is neither a numpy nor sparse matrix. provided {type(mat)}")
