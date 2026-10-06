import numpy as np
import pandas as pd
from src.copulas import simulate_t_copula
from scipy.stats import norm

def calculate_var_es(returns, level=0.99):
    """
    Calculates Historical VaR and Expected Shortfall (ES).
    Returns are portfolio returns.
    """
    var = np.percentile(returns, 100 * (1 - level))
    es = np.mean(returns[returns <= var])
    return var, es

def simulate_portfolio_returns(copula_model, marginals_train, weights, n_sims=10000, seed=42):
    """
    Simulates portfolio returns using 3D copula and empirical marginals.
    """
    np.random.seed(seed)
    # Simulate pseudo-uniforms
    if copula_model['type'] == 't':
        u_sim = simulate_t_copula(copula_model['corr'], copula_model['df'], n_sims)
    elif copula_model['type'] == 'gaussian':
        d = copula_model['corr'].shape[0]
        z = np.random.multivariate_normal(np.zeros(d), copula_model['corr'], size=n_sims)
        u_sim = norm.cdf(z)
    else:
        raise ValueError("Unsupported 3D copula")
        
    # Apply inverse empirical CDF for each asset
    sim_returns = np.zeros_like(u_sim)
    for i, col in enumerate(marginals_train.columns):
        sim_returns[:, i] = np.quantile(marginals_train[col].values, u_sim[:, i])
        
    # Aggregate to portfolio simple returns
    w = np.array([weights[col] for col in marginals_train.columns])
    
    # Assuming sim_returns are log returns for mapping, we convert to simple for portfolio aggregation
    # R = exp(r) - 1
    sim_simple = np.exp(sim_returns) - 1
    port_simple = sim_simple @ w
    
    # Return as log returns for consistent risk metric if desired, but VaR is usually on simple or log. 
    # Log return of portfolio = ln(1 + port_simple)
    port_log = np.log(1 + port_simple)
    return port_log, sim_returns
    
def calculate_historical_risk(returns, weights, level=0.99):
    simple_returns = np.exp(returns) - 1
    w = np.array([weights[col] for col in returns.columns])
    port_simple = simple_returns.dot(w)
    port_log = np.log(1 + port_simple)
    return calculate_var_es(port_log, level)
