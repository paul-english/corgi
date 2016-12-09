import numpy as np

import pandas as pd
from scipy.stats import kendalltau, spearmanr
from sklearn.metrics import (accuracy_score, f1_score, log_loss,
                             mean_absolute_error, mean_squared_error,
                             precision_score, recall_score)
from sklearn.model_selection import StratifiedKFold
from tqdm import tqdm


def discounted_cumulative_gain(y, y_pred, k=None):
    if k is None:
        k = y.shape[0]
    order = np.argsort(y_pred)[::-1]
    y = np.take(y, order[:k])
    return (y / np.log2(np.arange(y.shape[0]) + 2)).sum()

def exponential_discounted_cumulative_gain(y, y_pred, k=None):
    if k is None:
        k = y.shape[0]
    order = np.argsort(y_pred)[::-1]
    y = np.take(y, order[:k])
    return ((2**y - 1) / np.log2(np.arange(y.shape[0]) + 2)).sum()

def normalized_discounted_cumulative_gain(y, y_pred, k=None):
    return discounted_cumulative_gain(y, y_pred, k) / discounted_cumulative_gain(y, y, k)

def exponential_normalized_discounted_cumulative_gain(y, y_pred, k=None):
    return exponential_discounted_cumulative_gain(y, y_pred, k) \
        / exponential_discounted_cumulative_gain(y, y, k)


classifier_scoring = {
    'accuracy': accuracy_score,
    'log_loss': log_loss,
    'f1_score': lambda x, y: f1_score(x, y, average='weighted'),
    'precision': lambda x, y: precision_score(x, y, average='weighted'),
    'recall': lambda x, y: recall_score(x, y, average='weighted'),
}

regression_scoring = {
    'mean_squared_error': mean_squared_error,
    'mean_absolute_error': mean_absolute_error,
    'kendalltau': lambda x, y: kendalltau(x, y).correlation,
    'spearmanr': lambda x, y: spearmanr(x, y)[0],
}

rank_scoring = {
    'kendalltau': lambda x, y: kendalltau(x, y).correlation,
    'spearmanr': lambda x, y: spearmanr(x, y)[0],
    'ndcg': normalized_discounted_cumulative_gain,
    'endcg': exponential_normalized_discounted_cumulative_gain,
}

def scores(y, y_pred, scoring=None):
    if scoring is None:
        raise Exception("cross_val_scores requires a dict of measures.")

    scores = {}
    for k, metric in scoring.items():
        scores[k] = metric(y, y_pred)
    return scores


def cross_val_scores(clf, X, y, cv=3, scoring=None):
    if scoring is None:
        raise Exception("cross_val_scores requires a dict of measures.")

    X, y = np.array(X), np.array(y)
    skf = StratifiedKFold(n_splits=cv)
    scores = []
    for train, test in tqdm(skf.split(X, y)):
        clf.fit(X[train], y[train])
        y_pred = clf.predict(X[test])
        score = {}
        for k, metric in scoring.items():
            try:
                score[k] = metric(y[test], y_pred)
            except Exception as e:
                print('Warning: Exception trying to score', k, e)
                pass
        scores.append(score)

    return pd.DataFrame(scores)
