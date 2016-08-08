import math

import numpy as np


def remove_single_value_columns(df):
    drop_ix = df.apply(pd.Series.value_counts,
                       normalize=True,
                       axis=0).max() == 1
    drop_cols = df.columns[drop_ix]
    df = df.drop(drop_cols, axis=1)
    return df
