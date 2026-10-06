# Train / Test Methodology

## Timeline Split

The dataset is strictly split in time to prevent look-ahead bias and ensure the model is evaluated on genuinely unseen market conditions.

```text
2012-01-01                   2023-12-31 | 2024-01-01                    2026-10-06
|---------------------------------------|----------------------------------------|
                TRAIN                   |                  TEST
        (3,017 observations)            |           (692 observations)
                                        |
      No leakage of future data         |       Fixed OOS Backtesting
```

## Training Design (2012–2023)
All model parameters and thresholds are estimated exclusively on the training period:
- **Marginal ECDFs**: Formed using only 2012–2023 returns.
- **Wavelet Decomposition**: The SWT is applied only to the training set. (While SWT is a global transform, separating it prevents future information from altering historical detail coefficients).
- **Copula Parameters**: Correlation matrices and degrees-of-freedom for Gaussian/Student-t copulas are fitted via Maximum Likelihood on the training pseudo-uniforms.
- **Tail Dependence**: The 5% thresholds and empirical probabilities are measured solely on training data.
- **VaR / ES Calculation**: The final 99% VaR and ES thresholds are derived from 10,000 Monte Carlo simulations based entirely on the trained copulas and ECDFs.

## Testing Design (2024–2026)
The out-of-sample (OOS) period evaluates the predictive validity of the fixed thresholds:
- The exact portfolio weights (60/30/10) are applied to the realized OOS asset returns.
- The fixed 99% VaR and ES thresholds from the training period are applied to the OOS portfolio returns.
- **Violations**: A violation occurs when the realized OOS portfolio return falls below the predicted VaR.
- **Statistical Testing**: The Kupiec POF test evaluates whether the observed violation rate (28 violations out of 692 days for the Wavelet-Copula model) statistically aligns with the expected 1% rate (~6.92 violations). 

No rolling estimation was used for the OOS test; the parameters are completely fixed at the 2023-12-31 cutoff, providing a strict test of model calibration and structural stability.
