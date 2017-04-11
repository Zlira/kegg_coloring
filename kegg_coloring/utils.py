from collections import Counter

import numpy as np
import pandas as pd


def round_towards_inf(r):
    """
    Round floats toward infinity: 3.4 -> 4.0; -3.4 -> -4

    Args:
        r(float or ndarray of floats)

    Returns:
        floar or ndarray of floats
    """
    return np.ceil(np.abs(r)) * (np.abs(r) / r).astype(int)


def most_common_row(arr):
    """
    Returns most common row in 2D numpy array.
    """
    # TODO this is obviously not a very efficient way to
    # to this because it doesn't use vectorization.
    # I haven't manged to get it to work with numpy.unique
    # or scipy.stats.mode yet.
    return np.array(
        Counter(tuple(row) for row in arr)
        .most_common(1)[0][0]
    )


def dict_to_df(dct, key_col_name='key', val_col_name='val'):
    """
    Coverts python dictionary to a DataFrame with two columns
    """
    return pd.DataFrame(list(dct.items()),
                        columns=[key_col_name, val_col_name])
