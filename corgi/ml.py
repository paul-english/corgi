import numpy as np

import pandas as pd
from scipy.stats import kendalltau, spearmanr
from sklearn.metrics import (accuracy_score, f1_score, log_loss,
                             mean_squared_error, precision_score, recall_score)
from sklearn.model_selection import StratifiedKFold
from tqdm import tqdm


classifier_scoring = {
    'accuracy': accuracy_score,
    'log_loss': log_loss,
    'f1_score': lambda x, y: f1_score(x, y, average='weighted'),
    'precision': lambda x, y: precision_score(x, y, average='weighted'),
    'recall': lambda x, y: recall_score(x, y, average='weighted'),
}

regression_scoring = {
    'mean_squared_error': mean_squared_error,
    'kendalltau': lambda x, y: kendalltau(x, y).correlation,
    'spearmanr': lambda x, y: spearmanr(x, y)[0],
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
            except:
                pass
        scores.append(score)

    return pd.DataFrame(scores)
