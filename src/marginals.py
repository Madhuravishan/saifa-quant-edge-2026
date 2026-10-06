import numpy as np
import pandas as pd
from scipy.stats import rankdata

def to_pseudo_uniform(series):
    """
    Transforms a pandas Series to pseudo-uniform [0, 1] using ranks.
    Scaled to avoid exact 0 and 1.
    """
    n = len(series)
    ranks = rankdata(series)
    # Scale to (0, 1) exclusively
    u = ranks / (n + 1)
    return pd.Series(u, index=series.index, name=series.name)

def to_pseudo_uniform_df(df):
    """
    Applies the pseudo-uniform transformation to all columns.
    """
    return df.apply(to_pseudo_uniform)

def inverse_pseudo_uniform(u, original_series):
    """
    Maps pseudo-uniform variables back to the original domain using the empirical quantile function.
    """
    return np.quantile(original_series, u)
