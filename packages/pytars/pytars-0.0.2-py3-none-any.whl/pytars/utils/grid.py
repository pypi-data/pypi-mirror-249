from typing import Callable, Union

import numpy as np
from scipy.stats import binned_statistic_2d


def bin_grid_2d(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    xi: np.ndarray,
    yi: np.ndarray,
    fun: Union[Callable, str],
):
    """
    Bin the values in z into the bins defined by xg and yg.
    fun is a function that takes a 1d array and returns a scalar.
    """
    return binned_statistic_2d(x, y, z, statistic=fun, bins=[xi, yi]).statistic
