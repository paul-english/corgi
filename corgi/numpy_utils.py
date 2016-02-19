def remove_low_variance(X, low_variance_threshold=1e-4, axis=0):
    low_variance = X.var(axis=axis) < low_variance_threshold
    X[:, ~low_variance]
    return X


def normalize(X):
    zero_mean = X - X.mean()
    return (zero_mean + zero_mean.min()) / X.max()
