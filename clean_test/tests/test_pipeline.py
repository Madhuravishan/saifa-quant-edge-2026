import pytest
import numpy as np
import pandas as pd
import yaml
import os
import sys

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.risk import calculate_var_es
from src.wavelets import decompose_dataframe
from src.tail_dependence import empirical_lower_tail_dependence

@pytest.fixture
def config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def test_portfolio_weights_sum_to_one(config):
    weights = config['data']['weights']
    assert np.isclose(sum(weights.values()), 1.0), "Portfolio weights must sum to exactly 1"

def test_log_return_calculation():
    prices = pd.DataFrame({'A': [100, 105, 102]})
    rets = np.log(prices / prices.shift(1)).dropna()
    assert np.isclose(rets.iloc[0, 0], np.log(105/100)), "Log returns incorrect"

def test_var_sign_convention():
    # VaR should be negative for a typical loss
    returns = pd.Series([-0.05, -0.02, 0.01, 0.03, -0.08, -0.01, 0.02, 0.05, 0.01, -0.03])
    var, es = calculate_var_es(returns, level=0.90)
    assert var < 0, "VaR should be negative"
    assert es < var, "ES must be more extreme (lower) than VaR"

def test_tail_dependence_bounds():
    # Perfect dependence
    td_perfect = empirical_lower_tail_dependence(np.array([0.01, 0.02, 0.05]), np.array([0.01, 0.02, 0.05]), threshold=0.1)
    assert np.isclose(td_perfect, 1.0)
    
    # No dependence
    td_none = empirical_lower_tail_dependence(np.array([0.01, 0.02, 0.05]), np.array([0.9, 0.8, 0.7]), threshold=0.1)
    assert np.isclose(td_none, 0.0)

def test_wavelet_decomposition():
    df = pd.DataFrame({'A': np.random.randn(100)})
    decomp = decompose_dataframe(df, 'db4', 3)
    assert list(decomp.keys()) == ['short', 'medium', 'long', 'trend'], "Wavelet horizons must match specification"
    
    # Check linear reconstruction
    reconstructed = sum([decomp[k]['A'] for k in decomp.keys()])
    assert len(reconstructed) == len(df['A']), "MODWT decomposed arrays must match input length"
