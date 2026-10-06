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
    
    # Calculate MRA components using ISWT
    # coeffs is [(cA_3, cD_3), (cA_2, cD_2), (cA_1, cD_1)] for level 3
    mra = {}
    for i in range(level):
        c = [(np.zeros_like(cA), np.zeros_like(cD)) for cA, cD in coeffs]
        c[i] = (np.zeros_like(coeffs[i][0]), coeffs[i][1])
        mra[f'D{level-i}'] = pywt.iswt(c, wavelet_type)[:n]
        
    c = [(np.zeros_like(cA), np.zeros_like(cD)) for cA, cD in coeffs]
    c[0] = (coeffs[0][0], np.zeros_like(coeffs[0][1]))
    mra[f'A{level}'] = pywt.iswt(c, wavelet_type)[:n]
    
    return {
        'short': mra['D1'],
        'medium': mra['D2'],
        'long': mra['D3'],
        'trend': mra[f'A{level}']
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
