# SAIFA Quant Edge 1.0 Round 1: Research Project

## 1. Abstract
This report investigates whether extreme lower-tail dependence changes with the investment horizon and assesses the impact of ignoring horizon-dependent dependence on portfolio tail risk measurement. Using Maximum Overlap Discrete Wavelet Transform (MODWT) via Stationary Wavelet Transform and Copula functions, we separate financial returns into short, medium, and long horizons, modelling dependence explicitly at each scale.

## 2. Research Question and Motivation
"Does tail dependence change with the investment horizon, and what does ignoring this do to a portfolio's measured risk?"
Diversification is the cornerstone of risk management, but it often breaks down during severe market stress (tail dependence). If this dependence varies across investment horizons, static single-horizon risk models may systematically under- or over-estimate risk.

## 3. Portfolio and Data
- **Assets**: SPY (60%, Primary risk), TLT (30%, Defensive/Duration), GLD (10%, Safe Haven).
- **Period**: 2012-01-01 to 2026-10-06.
- **Train/Test**: Train (2012-01-01 to 2023-12-31), Test (2023-12-31 onwards).
- Data sourced from Yahoo Finance (adjusted close, converted to daily log returns).

## 4. Methodology
- **Wavelets**: Daubechies-4 (db4) at 3 levels.
  - Short: ~2-4 days
  - Medium: ~4-8 days
  - Long: ~8-16 days
  - Trend: Remaining low-frequency component.
- **Marginals**: Pseudo-uniform transformation via Empirical CDF.
- **Copulas**: Evaluated Gaussian and Student-T for 3D portfolio risk, and empirical tail dependence for bivariate relations to capture extreme co-movements robustly.
- **Risk Metrics**: 99% VaR and 99% Expected Shortfall (ES).

## 5. Experimental Design
- **Benchmark**: Historical VaR/ES and a Single-Horizon Copula.
- **Proposed Model**: Wavelet-Copula (aggregating simulated horizon-specific returns).
- **Backtesting**: Kupiec POF test and ES severity scoring on the hold-out test set using a fixed-training approach for computational efficiency.

## 6. Results

### Tail Dependence by Horizon
Empirical lower-tail dependence (5% threshold) by asset pair:
```
|                |     short |    medium |   long |
|:---------------|----------:|----------:|-------:|
| ('SPY', 'TLT') | 0.0533333 | 0.0333333 |   0.06 |
| ('SPY', 'GLD') | 0.0866667 | 0.0933333 |   0.18 |
| ('TLT', 'GLD') | 0.2       | 0.173333  |   0.26 |
```
*H1 Support*: Supported. Tail dependence is not constant. For example, SPY-TLT dependence exhibits distinct behavior across horizons, highlighting that bond-equity diversification properties change depending on whether the shock is transient or persistent.

### Portfolio Risk Comparison (99%)
```
| Model                 |    99% VaR |     99% ES |
|:----------------------|-----------:|-----------:|
| Historical            | -0.0180596 | -0.026727  |
| Single-Horizon Copula | -0.0180152 | -0.0262087 |
| Wavelet-Copula        | -0.0116731 | -0.0177885 |
```
*H2 Support*: Supported, but in the opposite direction of conventional wisdom. The Wavelet-Copula model produces a much lower risk estimate (VaR closer to zero) than the historical benchmark. This occurs because modeling horizons independently assumes extreme shocks at different frequencies are uncorrelated. In reality, market crashes exhibit simultaneous extremes across all horizons (volatility clustering).

### Out-of-Sample Performance
```
| Model                |   Violations |   Expected Violations |   POF p-value |   ES Score (Actual - Forecast) |
|:---------------------|-------------:|----------------------:|--------------:|-------------------------------:|
| Historical Benchmark |            5 |                  6.92 |   0.440263    |                   -0.00155209  |
| Wavelet-Copula       |           28 |                  6.92 |   1.32814e-09 |                    0.000973859 |
```
*H3 Support*: The Wavelet-Copula model experiences an unacceptable number of VaR violations (far exceeding the expected 1%). This confirms that independent horizon aggregation severely underestimates portfolio risk.

## 7. Robustness Checks
- **Tail Thresholds**: Analyzed at the 5% threshold empirically, which balances robustness and extreme emphasis.
- **Model Choice**: Relied on Student-T and Gaussian selection via AIC to avoid forcing ill-fitting Archimedean copulas onto 3D data.

## 8. Risk-Management Implication
**Recommendation**: Risk managers must not treat different investment horizons as independent independent signals when simulating portfolio risk. While tail dependence does vary by horizon, simulating these horizons independently destroys the cross-horizon dependence (simultaneous extremes). A robust model must explicitly model the dependency *across* horizons, otherwise it will dangerously underestimate capital requirements.

## 9. Conclusion
Integrating wavelets and copulas reveals that tail risk and asset correlations are highly horizon-dependent. However, a naive aggregation that assumes independence between short, medium, and long horizons leads to a severe underestimation of Expected Shortfall. Future research must incorporate a meta-copula linking the horizons themselves.

## 10. References
- McNeil, A. J., & Frey, R. (2000). Estimation of tail-related risk measures for heteroscedastic financial time series.
- Kupiec, P. H. (1995). Techniques for verifying the accuracy of risk measurement models.
