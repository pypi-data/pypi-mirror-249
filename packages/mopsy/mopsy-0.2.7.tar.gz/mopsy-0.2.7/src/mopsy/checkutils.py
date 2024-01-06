# this file only exists because of circular imports error

from typing import Union

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def check_axis(axis: Union[int, bool]):
    """Check if axis has a correct value.

    Args:
        axis:
            Axis, 0 for rows, 1 for columns

    Raises:
        ValueError:
            If axis is neither 0 nor 1
    """
    if not (axis == 0 or axis == 1):
        raise ValueError(f"'axis' is neither 0 or 1, provided {axis}.")
