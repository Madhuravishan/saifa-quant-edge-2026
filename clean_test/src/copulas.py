import numpy as np
import pandas as pd
from scipy.stats import norm, t
from scipy.optimize import minimize
from scipy.linalg import cholesky

def fit_gaussian_copula(u):
    """
    Fits a Gaussian copula to pseudo-uniform data.
    u is a TxD numpy array.
    """
    x = norm.ppf(u)
    # Estimate correlation matrix
    corr = np.corrcoef(x, rowvar=False)
    return {'type': 'gaussian', 'corr': corr, 'll': gaussian_copula_ll(u, corr)}

def gaussian_copula_ll(u, corr):
    x = norm.ppf(u)
    inv_corr = np.linalg.inv(corr)
    det_corr = np.linalg.det(corr)
    ll = 0
    for i in range(len(u)):
        ll -= 0.5 * np.log(det_corr) + 0.5 * x[i].T @ (inv_corr - np.eye(len(corr))) @ x[i]
    return ll

def t_copula_ll(params, u):
    nu = params[0]
    if nu <= 2 or nu > 100:
        return 1e9
    x = t.ppf(u, df=nu)
    corr = np.corrcoef(x, rowvar=False)
    
    try:
        inv_corr = np.linalg.inv(corr)
        det_corr = np.linalg.det(corr)
    except:
        return 1e9
        
    d = u.shape[1]
    
    from scipy.special import gammaln
    
    ll = 0
    for i in range(len(u)):
        term1 = gammaln((nu + d)/2) + (d-1)*gammaln(nu/2) - d*gammaln((nu+1)/2)
        term2 = -0.5 * np.log(det_corr)
        term3 = -0.5 * (nu + d) * np.log(1 + (x[i].T @ inv_corr @ x[i]) / nu)
        term4 = 0
        for j in range(d):
            term4 += 0.5 * (nu + 1) * np.log(1 + x[i][j]**2 / nu)
        ll += term1 + term2 + term3 + term4
    return -ll # return negative log-likelihood for minimization

def fit_t_copula(u):
    """
    Fits a Student-t copula to pseudo-uniform data.
    """
    res = minimize(t_copula_ll, x0=[5.0], args=(u,), bounds=[(2.1, 100)])
    nu = res.x[0]
    x = t.ppf(u, df=nu)
    corr = np.corrcoef(x, rowvar=False)
    return {'type': 't', 'corr': corr, 'df': nu, 'll': -res.fun}

def fit_clayton_copula_bivariate(u):
    """
    Fits a bivariate Clayton copula.
    """
    def clayton_ll(theta, u1, u2):
        if theta <= 0: return 1e9
        term1 = (theta + 1) * np.log(u1 * u2)
        term2 = (1 + 1/theta) * np.log(u1**(-theta) + u2**(-theta) - 1)
        ll = np.sum(np.log(theta) - term1 - term2)
        return -ll
        
    res = minimize(clayton_ll, x0=[1.0], args=(u[:,0], u[:,1]), bounds=[(0.01, 50)])
    return {'type': 'clayton', 'theta': res.x[0], 'll': -res.fun}

def simulate_t_copula(corr, df, n):
    d = corr.shape[0]
    # Simulate multivariate t
    z = np.random.multivariate_normal(np.zeros(d), corr, size=n)
    w = np.random.chisquare(df, size=n) / df
    x = z / np.sqrt(w)[:, None]
    return t.cdf(x, df=df)

def select_best_copula_3d(u):
    # Only fit Gaussian and T for 3D since Clayton 3D is symmetric Archimedean and often poor
    g_res = fit_gaussian_copula(u)
    t_res = fit_t_copula(u)
    
    # AIC = 2k - 2ln(L)
    k_g = 3 # 3 correlation params
    k_t = 4 # 3 correlation + 1 df
    
    aic_g = 2*k_g - 2*g_res['ll']
    aic_t = 2*k_t - 2*t_res['ll']
    
    n_samples = len(u)
    bic_g = k_g * np.log(n_samples) - 2*g_res['ll']
    bic_t = k_t * np.log(n_samples) - 2*t_res['ll']
    
    g_res['aic'] = aic_g
    g_res['bic'] = bic_g
    t_res['aic'] = aic_t
    t_res['bic'] = bic_t
    
    if aic_t < aic_g:
        return t_res
    return g_res
    
def select_best_copula_2d(u):
    g_res = fit_gaussian_copula(u)
    t_res = fit_t_copula(u)
    c_res = fit_clayton_copula_bivariate(u)
    
    aic_g = 2*1 - 2*g_res['ll']
    aic_t = 2*2 - 2*t_res['ll']
    aic_c = 2*1 - 2*c_res['ll']
    
    aics = {'gaussian': aic_g, 't': aic_t, 'clayton': aic_c}
    best = min(aics, key=aics.get)
    
    if best == 'gaussian': return g_res
    elif best == 't': return t_res
    else: return c_res
