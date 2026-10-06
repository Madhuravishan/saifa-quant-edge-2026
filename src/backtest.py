import numpy as np
import scipy.stats as stats

def kupiec_pof_test(returns, var_forecasts, level=0.99):
    """
    Kupiec Proportion of Failures (POF) test.
    returns: actual portfolio returns (array)
    var_forecasts: forecasted VaR values (array, same length as returns). Typically negative.
    """
    # Count violations
    # returns <= var (var is typically negative)
    violations = returns < var_forecasts
    n1 = np.sum(violations)
    n0 = len(returns) - n1
    n = len(returns)
    
    p_expected = 1 - level
    p_obs = n1 / n
    
    if n1 == 0:
        return 0, 1.0 # Cannot reject
        
    # Likelihood ratio test statistic
    # LR = -2 * ln( ((1-p_expected)^n0 * p_expected^n1) / ((1-p_obs)^n0 * p_obs^n1) )
    lr = -2 * (n0 * np.log(1 - p_expected) + n1 * np.log(p_expected) - 
               (n0 * np.log(1 - p_obs) + n1 * np.log(p_obs)))
               
    # p-value from chi-square distribution with 1 DOF
    p_value = 1 - stats.chi2.cdf(lr, df=1)
    
    return lr, p_value

def es_score(returns, var_forecasts, es_forecasts):
    """
    Expected Shortfall backtesting score (McNeil and Frey 2000 approach simplified: 
    calculate the mean difference between actual return and ES when VaR is violated).
    Or use the Acerbi-Szekely (2014) Z2 test statistic approach.
    We'll simply report the average return when violated vs forecasted ES.
    """
    violations = returns < var_forecasts
    if np.sum(violations) == 0:
        return np.nan
        
    actual_es = np.mean(returns[violations])
    avg_forecast_es = np.mean(es_forecasts[violations])
    
    return actual_es - avg_forecast_es
