# Project Guide: SAIFA Quant Edge 1.0

This document is the comprehensive narrative guide for the team to understand the entire project end-to-end.

## 1. The Problem
Standard risk models (like historical simulation or basic Gaussian copulas) look at daily returns and assume that the relationships between assets are static. But what if the relationship between Stocks (SPY) and Gold (GLD) is different during a 2-day flash crash compared to a 16-day structural market shift? If dependence changes based on the "horizon", standard models might miscalculate the true risk of a portfolio.

## 2. The Intuition
Imagine listening to a symphony. A standard correlation matrix just measures the overall volume. Wavelets allow us to separate the music into bass, mid, and treble frequencies. We can then measure how the instruments interact specifically in the bass frequencies (long-term trends) versus the treble frequencies (short-term noise).

## 3. Data & Portfolio
We use a 60/30/10 portfolio of SPY (Equities), TLT (Bonds), and GLD (Gold) using daily data from 2012 to 2026. We train all models on 2012-2023, and test strictly out-of-sample on 2024-2026.

## 4. Wavelets
We use the Maximum Overlap Discrete Wavelet Transform (MODWT). It breaks the daily return time series into additive components:
- **Short**: 2-4 day dynamics
- **Medium**: 4-8 day dynamics
- **Long**: 8-16 day dynamics
Because it's a linear transform, if you add the components back together, you get the original daily returns.

## 5. Copulas & Tail Dependence
For each horizon, we fit a 3D Copula (Student-t or Gaussian). We also measure empirical lower tail dependence (the probability that Asset B crashes given Asset A crashes at the 5% worst level).
**Finding:** Tail dependence changes! SPY and GLD are twice as likely to crash together over long horizons compared to short horizons.

## 6. Portfolio Simulation & Risk (VaR/ES)
We simulate 10,000 paths for each horizon using the fitted copulas. We add the simulated horizons together to create a simulated daily portfolio return. From this, we calculate the 99% Value at Risk (VaR) and Expected Shortfall (ES).

## 7. The Benchmark & Results
We compare our complex Wavelet-Copula model to a simple Historical Benchmark.
- **Historical 99% VaR**: -1.80%
- **Wavelet-Copula 99% VaR**: -1.16% (Severely underestimates risk)

## 8. Out-of-Sample Backtesting
We test these thresholds on the unseen 2024-2026 data. We expect ~7 violations (1% of 692 days).
- **Historical Benchmark**: 5 violations (Excellent).
- **Wavelet-Copula**: 28 violations (Massive failure).

## 9. Conclusion & Recommendation
The complex model failed because it assumed the wavelet horizons were independent. When a real crash happens, it hits all frequencies at once. By simulating them independently, the model "diversified away" the crashes. 

**Recommendation:** Risk managers must acknowledge horizon-dependent relationships, but they cannot aggregate risk by treating time horizons independently. Doing so leads to a catastrophic underestimation of capital requirements.
