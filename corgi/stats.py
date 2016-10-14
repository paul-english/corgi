import numpy as np

import pandas as pd
from scipy import stats


def boxcox(y, ld=None, offset=None):
    if offset is None:
        offset = abs(y.min()) + 1
    if ld is None:
        yt, ld = stats.boxcox(y + offset)
    else:
        yt = stats.boxcox(y + offset, ld)
    return pd.Series(yt), ld, offset


def invboxcox(y, ld, offset=0):
    if ld == 0:
        return np.exp(y) - offset
    else:
        return np.exp(np.log(ld*y+1)/ld) - offset
