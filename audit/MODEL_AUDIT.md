# Model Audit

## Wavelet Decomposition
- **Method**: Maximum Overlap Discrete Wavelet Transform (MODWT) / Stationary Wavelet Transform (SWT).
- **Family**: Daubechies 4 (db4).
- **Implementation**: Uses `pywt.swt` and `pywt.iswt` from the PyWavelets library in `src/wavelets.py`. The linear additive property is preserved.

## Copula Fitting
- **Marginals**: Pseudo-uniforms generated using empirical CDF (rank-based) in `src/marginals.py`.
- **Optimization**: Parameters (correlation and degrees-of-freedom) estimated via Maximum Likelihood in `src/copulas.py`.
- **Selection**: AIC correctly applied to choose between Gaussian and Student-t for 3D modeling.

## Risk Calculation
- **VaR/ES**: 99% thresholds correctly extracted from 10,000 Monte Carlo simulated returns.
- **Aggregation**: Independent simulated wavelet horizons are correctly summed (due to SWT additivity) and transformed back to simple returns before portfolio weighting, then back to log returns for risk metrics.

**Audit Status:** PASS