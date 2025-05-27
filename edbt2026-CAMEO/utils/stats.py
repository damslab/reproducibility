import numpy as np
from statsmodels.api import tsa
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.seasonal import seasonal_decompose


def auto_corr(x, max_lag=10, use_tsa=True):
    if use_tsa:
        return tsa.acf(x, nlags=max_lag, fft=False if len(x) < 100 else True)[1:]

    return np.asarray([np.corrcoef(x[:-lag], x[lag:])[0, 1] for lag in range(1, max_lag+1)])


def triangle_area(p1, p2, p3):
    """
    calculates the area of a triangle given its vertices
    """
    return abs(p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])) / 2.


def seasonal_strength(series, acf):
    scaler = StandardScaler()
    series = np.squeeze(scaler.fit_transform(series[:, np.newaxis]))
    result = seasonal_decompose(series, model='additive', period=acf)
    return max(0, 1 - np.var(result.resid[acf//2:-acf//2])/np.var(result.resid[acf//2:-acf//2] + result.seasonal[acf//2:-acf//2]))


def remove(s, i):
    """
    Quick trick to remove an item from a numpy array without
    creating a new object.  Rather than the array shape changing,
    the final value just gets repeated to fill the space.
    ~3.5x faster than numpy delete
    """
    s[i:-1] = s[i+1:]


def triangle_areas_from_array(arr):
    """
    take an (N,2) array of points and return an (N,1)
    array of the areas of those triangles, where the first
    and last areas are np.inf
    see triangle_area for algorithm
    """

    result = np.empty((len(arr),), np.float64)
    result[0] = np.inf
    result[-1] = np.inf

    p1 = arr[:-2]
    p2 = arr[1:-1]
    p3 = arr[2:]

    # an accumulators to avoid unnecessary intermediate arrays
    accr = result[1:-1]  # Accumulate directly into result
    acc1 = np.empty_like(accr)

    np.subtract(p2[:, 1], p3[:, 1], out=accr)
    np.multiply(p1[:, 0], accr, out=accr)
    np.subtract(p3[:, 1], p1[:, 1], out=acc1)
    np.multiply(p2[:, 0], acc1, out=acc1)
    np.add(acc1, accr, out=accr)
    np.subtract(p1[:, 1], p2[:, 1], out=acc1)
    np.multiply(p3[:, 0], acc1, out=acc1)
    np.add(acc1, accr, out=accr)
    np.abs(accr, out=accr)
    accr /= 2.
    return result