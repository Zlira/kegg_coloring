import numpy as np


def round_towards_inf(r):
    """
    Round floats toward infinity: 3.4 -> 4.0; -3.4 -> -4

    Args:
        r(float or ndarray of floats)

    Returns:
        floar or ndarray of floats
    """
    return np.ceil(np.abs(r)) * (np.abs(r) / r).astype(int)
