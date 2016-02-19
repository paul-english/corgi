import math

import numpy as np


def remove_single_value_columns(df):
    drop_ix = df.apply(pd.Series.value_counts,
                       normalize=True,
                       axis=0).max() == 1
    drop_cols = df.columns[drop_ix]
    df = df.drop(drop_cols, axis=1)
    return df


def sample(df, sample_percent=2e-2):
    sample_n = math.floor(len(df) * sample_percent)
    rows = np.random.choice(df.shape[0], sample_n)
    return df.ix[rows]


def sample_columns(df, sample_percent=0.5):
    df = sample(df.T, sample_percent).T
    return df
