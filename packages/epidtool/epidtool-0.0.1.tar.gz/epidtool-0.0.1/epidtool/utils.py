from collections import Iterable

import numpy as np
from sklearn.preprocessing import MinMaxScaler as Scaler


def normalize(data):
    """Return MinMax scaled data.
    
    Parameters
    ----------
    data : iterable
        The data to be normalized.
    
    Returns
    -------
    numpy.ndarray
        Normalized data.
    """
    if not isinstance(data, Iterable):
        raise ValueError('data must be iterable')
    if isinstance(data, (list, tuple)):
        data = np.array(data)
    if isinstance(data, (np.ndarray)):
        assert data.ndim == 1, 'data must be 1-D'
        assert data.size > 1, 'data must contain at least 2 elements'
    if np.isnan(data).any():
        raise ValueError('data contains one or more NaN values')
    return (data - np.min(data)) / (np.max(data) - np.min(data))


def restore(y_norm, y):
    """Return restored data considering original data.
    
    Parameters
    ----------
    y_norm : iterable
        Scaled data.
    y : iterable
        Original data.
    
    Returns
    -------
    numpy.ndarray
        Restored data.
    """
    if not (isinstance(y_norm, Iterable) and
            isinstance(y, Iterable)):
        raise ValueError('data must be iterable')
    if isinstance(y_norm, (list, tuple)):
        y_norm = np.array(y_norm)
    if isinstance(y, (list, tuple)):
        y = np.array(y)
    if (isinstance(y_norm, (np.ndarray)) and 
            isinstance(y, (np.ndarray))):
        assert y_norm.ndim == 1 and y.ndim == 1, \
            'data must be 1-D'
        assert y_norm.size > 1 or y.size > 1, \
            'data must contain at least 2 elements'
    if np.isnan(y_norm).any() or np.isnan(y).any():
        raise ValueError('data contains one or more NaN values')
    return y_norm * (np.max(y) - np.min(y)) + np.min(y)


def moving_average(y, n=3):
    """Return a array of averages of different subsets of the full data
    set.

    Parameters
    ----------
    y : numpy.ndarray
        Data to be averaged.
    n : int
        Averaging window.

    Returns
    -------
    numpy.ndarray
        Averaged data.
    """
    if not isinstance(n, (int)):
        raise ValueError('Averaging windows should be an integer.')
    if not isinstance(y, Iterable):
        raise ValueError('data must be iterable')
    if isinstance(y, (list, tuple)):
        y = np.array(y)
    if isinstance(y, (np.ndarray)):
        assert y.ndim == 1, 'data must be 1-D'
        assert y.size >= n, 'data must contain at least `n` elements'
    if n == 0:
        return y
    ret = np.cumsum(y, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n
