import numpy as np

def empirical_lower_tail_dependence(u1, u2, threshold=0.05):
    """
    Empirical lower tail dependence: P(U2 < q | U1 < q)
    """
    mask1 = u1 < threshold
    if np.sum(mask1) == 0:
        return 0.0
    mask2 = u2 < threshold
    return np.sum(mask1 & mask2) / np.sum(mask1)

def theoretical_lower_tail_dependence(copula_model):
    """
    Calculates theoretical lower tail dependence for 2D.
    """
    ctype = copula_model['type']
    if ctype == 'gaussian':
        return 0.0
    elif ctype == 't':
        nu = copula_model['df']
        # For 2D, the correlation is a scalar (off-diagonal element)
        rho = copula_model['corr'][0, 1]
        
        from scipy.stats import t
        # Lambda_L = 2 * t_{nu+1}( - sqrt((nu+1)*(1-rho)/(1+rho)) )
        val = -np.sqrt((nu + 1) * (1 - rho) / (1 + rho + 1e-8))
        return 2 * t.cdf(val, df=nu+1)
    elif ctype == 'clayton':
        theta = copula_model['theta']
        return 2 ** (-1 / theta)
    return 0.0
