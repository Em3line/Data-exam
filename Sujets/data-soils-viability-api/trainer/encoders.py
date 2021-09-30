from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd


class TimeFeaturesExtractor(BaseEstimator, TransformerMixin):

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X_ = X.copy()
        X_ = X_[[self.start, self.end]]
        X_[self.start] = pd.to_datetime(X_[self.start])
        X_[self.end] = pd.to_datetime(X_[self.end])

        X_["month"] = X_[self.start].dt.month
        X_["duration"] = (X_[self.end] - X_[self.start]) / \
            np.timedelta64(1, 'h')

        return X_[["month", "duration"]] \
            .reset_index(drop=True)


class CyclicalEncoder(BaseEstimator, TransformerMixin):

    def __init__(self, col):
        self.col = col

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X_ = X.copy()
        X_ = X_[[self.col]]
        month_norm = 2 * np.pi * X[['month']] / 12
        X_["month_cos"] = np.cos(month_norm)
        X_["month_sin"] = np.sin(month_norm)

        return X_[["month_cos", "month_sin"]]


class OrdinalEncoder(BaseEstimator, TransformerMixin):

    def __init__(self, feature):
        self.feature = feature

    def fit(self, X, y=None):
        return self

    def _cat_to_num(self, cat):
        map_ = {"poor": -1, "normal": 0, "rich": 1}
        return map_.get(cat)

    def transform(self, X, y=None):
        X_ = X.copy()
        return X_[[self.feature]].applymap(self._cat_to_num)
