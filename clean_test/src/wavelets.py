import pywt
import numpy as np
import pandas as pd

def get_swt_components(series, wavelet_type='db4', level=3):
    # SWT requires length to be divisible by 2^level
    n = len(series)
    pad_len = (2**level - (n % 2**level)) % 2**level
    if pad_len > 0:
        # Pad symmetrically
        padded_series = np.pad(series, (0, pad_len), mode='symmetric')
    else:
        padded_series = series.values if isinstance(series, pd.Series) else series

    # Perform SWT
    coeffs = pywt.swt(padded_series, wavelet_type, level=level, start_level=0)
    
    # coeffs is [(cA_L, cD_L), (cA_{L-1}, cD_{L-1}), ..., (cA_1, cD_1)]
    # We want to return details D1, D2, D3 and approximation A3
    
    # Extract components and trim padding
    # D1 is in coeffs[-1][1]
    # D2 is in coeffs[-2][1]
    # D3 is in coeffs[-3][1]
    # A3 is in coeffs[0][0]  (since it's level 3)
    
    D1 = coeffs[-1][1][:n]
    D2 = coeffs[-2][1][:n]
    D3 = coeffs[-3][1][:n]
    A3 = coeffs[0][0][:n]
    
    return {
        'short': D1,
        'medium': D2,
        'long': D3,
        'trend': A3
    }

def decompose_dataframe(df, wavelet_type='db4', level=3):
    """
    Decomposes a DataFrame of returns into horizons.
    Returns a dictionary of DataFrames: 'short', 'medium', 'long', 'trend'
    """
    results = {'short': pd.DataFrame(index=df.index),
               'medium': pd.DataFrame(index=df.index),
               'long': pd.DataFrame(index=df.index),
               'trend': pd.DataFrame(index=df.index)}
               
    for col in df.columns:
        comps = get_swt_components(df[col], wavelet_type, level)
        results['short'][col] = comps['short']
        results['medium'][col] = comps['medium']
        results['long'][col] = comps['long']
        results['trend'][col] = comps['trend']
        
    return results
