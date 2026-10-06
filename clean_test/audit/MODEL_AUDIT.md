# MODEL AUDIT

## Wavelets
- **Method**: Stationary Wavelet Transform (SWT / MODWT).
- **Implementation**: `PyWavelets` package.
- **Type**: Daubechies 4 (`db4`), Level 3.
- **Horizons**: 
  - Short (D1, ~2-4 days)
  - Medium (D2, ~4-8 days)
  - Long (D3, ~8-16 days)
  - Trend (A3, Remaining low frequencies)

## Copulas
- **Families**: Gaussian, Student-t (Clayton evaluated in 2D).
- **Fitting**: Log-likelihood minimization.
- **Selection**: Akaike Information Criterion (AIC).
- **Portfolio Construction**: 3D Copula aggregation using empirical marginal distributions across asset returns per horizon.

## Tail Dependence
- **Calculation**: Empirical lower-tail dependence at 5% threshold.
- **Output**: Horizon-specific values correctly generated.