import math

import numpy as np

import pandas as pd

one_hot = lambda df: pd.get_dummies(df)
zero_mean = lambda df: df - df.mean(axis=0)
one_dev = lambda df: df / df.std(axis=0)
no_nan = lambda df: df.fillna(0)
shuffled = lambda df: df.sample(frac=1)
remove_constant_cols = lambda df: df.loc[:, (df != df.iloc[0]).any()]

def date_features(df):
    df = df.apply(pd.to_datetime)
    date_features = [
        'month', 'day', 'dayofyear',
        'week', 'weekday', 'quarter',
        'year', 'is_month_start', 'is_month_end',
        'is_quarter_start', 'is_quarter_end', 'is_year_start',
        'is_year_end'
    ]

    cols = df.columns

    for date_feature in date_features:
        new_cols = [c + '_' + date_feature for c in cols]
        df[new_cols] = df[cols].apply(
            lambda x: getattr(x.dt, date_feature)
        )

    # we've extracted some potentially useful date features, lets convert
    # the original dates to seconds so they can be used as a numeric feature
    df[cols] = df[cols].astype(np.int64)

    return df

def clean(df, drop_cols=None, categorical_cols=None, date_cols=None):
    cols = df.columns

    if date_cols is not None:
        df = pd.concat(
            [
                df.drop(date_cols, axis=1),
                date_features(df[date_cols]),
            ],
            axis=1
        )

    if categorical_cols is not None:
        df = pd.concat(
            [
                df.drop(categorical_cols, axis=1),
                one_hot(df[categorical_cols].astype(object))
            ],
            axis=1
        )

    # Drop unneeded and non-informative
    if drop_cols is not None:
        df = df.drop(drop_cols, axis=1)

    df = remove_constant_cols(df)

    return df
