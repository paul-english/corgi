from __future__ import print_function

import numpy as np


def hist(data, width=20):
    counts, values = np.histogram(data)
    max_count = counts.max()

    for (count, value) in zip(counts, values):
        scaled = int(round((count / max_count) * width))
        print('%5.2f' % value, ':', 'X'*scaled)
