# SAIFA Quant Edge 1.0 - Project Research Map

## What is the research question?
Does tail dependence change with the investment horizon, and what does ignoring this do to measured portfolio risk?

## What is the portfolio?
A 3-asset allocation: SPY (60%), TLT (30%), GLD (10%).

## Why SPY/TLT/GLD?
These assets represent distinct risk and economic roles:
- **SPY (US Equities)**: The primary growth and risk engine.
- **TLT (Long-Term Treasuries)**: A defensive asset sensitive to duration and interest rates, historically negatively correlated with equities during stress.
- **GLD (Gold)**: A safe-haven and inflation-hedge asset, providing an alternative macroeconomic exposure.
This combination allows us to study whether the supposed diversification benefits between equities, bonds, and gold change across different market horizons (e.g., short-term crashes vs. long-term structural shifts).

## What are the weights?
- w_SPY = 60%
- w_TLT = 30%
- w_GLD = 10%

## What is the data source?
Yahoo Finance (yfinance API). Adjusted Close prices are converted to daily log returns.

## What exact dates are available?
The downloaded data ranges from 2012-01-01 to 2026-10-06.

## What is the training period?
2012-01-01 to 2023-12-31 (3,017 observations).

## What is the test period?
2024-01-01 to 2026-10-06 (692 observations).

## What is the return definition?
Log returns: r_t = log(P_t / P_{t-1}).

## What is the wavelet methodology?
We use the Maximum Overlap Discrete Wavelet Transform (MODWT) via the Stationary Wavelet Transform (SWT).
- **Family**: Daubechies 4 (db4).
- **Levels**: 3 levels of decomposition.

## What are the selected horizons?
1. **Short**: Level 1 Details (approx. 2-4 days)
2. **Medium**: Level 2 Details (approx. 4-8 days)
3. **Long**: Level 3 Details (approx. 8-16 days)
4. **Trend**: Level 3 Approximations (the remaining low-frequency component)

## What are the copula models?
For 3D joint portfolio simulation, we fit both Gaussian and Student-t copulas to the pseudo-uniform margins of each horizon's returns, selecting the best fit using Akaike Information Criterion (AIC). For 2D tail dependence analysis, we evaluate empirical tail dependence.

## How are marginals modeled?
Marginals are transformed to pseudo-uniform observations using the empirical cumulative distribution function (ECDF) based on ranks.

## How is dependence modeled?
We model dependence independently for each wavelet horizon using the selected 3D copula.

## How is tail dependence estimated?
We estimate empirical lower-tail dependence at the 5% threshold: P(U2 < 0.05 | U1 < 0.05).

## How is portfolio risk simulated?
1. Simulate pseudo-uniform observations from the fitted copula for each horizon.
2. Apply the inverse ECDF of the training data to map back to return space.
3. Sum the simulated log returns across all horizons (taking advantage of SWT's additive reconstruction).
4. Convert back to simple returns, apply portfolio weights, and calculate final simulated log portfolio returns.

## What are the VaR and ES definitions?
- **99% VaR**: The 1st percentile of the simulated portfolio return distribution.
- **99% ES**: The mean of the simulated returns that fall below the 99% VaR threshold.

## What is the benchmark?
A historical simulation VaR/ES and a single-horizon Student-t copula model.

## How is OOS performance tested?
Using the fixed VaR and ES thresholds estimated from the training data, we count the number of violations in the out-of-sample (OOS) period (2024-01-01 to 2026-10-06). We apply the Kupiec Proportion of Failures (POF) test and calculate the ES Score (difference between actual average shortfall and forecast).

## What are the main results?
1. **Tail dependence changes by horizon**: For example, SPY-GLD tail dependence increases from 0.086 at the short horizon to 0.180 at the long horizon.
2. **Ignoring cross-horizon dependence severely underestimates risk**: The Wavelet-Copula model (which simulates horizons independently) forecasted a 99% VaR of -1.16%, significantly less conservative than the Historical benchmark's -1.80%. 
3. **OOS Failure**: The Wavelet-Copula model suffered 28 violations out-of-sample (expected: ~6.92), proving that assuming independence across time horizons is mathematically dangerous for risk aggregation.

## What are the limitations?
Simulating individual wavelet horizons independently destroys the cross-horizon dependence. Extreme market crashes exhibit volatility clustering across all frequencies simultaneously. The lack of a meta-copula linking the horizons limits the model's absolute predictive power, even as it successfully answers the research question regarding the nature of horizon dependence.

## What is the risk-manager recommendation?
Do not treat different investment horizons as independent signals when aggregating portfolio risk. While dependence varies by horizon, explicitly modeling the joint dependence *across* horizons is strictly required to prevent catastrophic underestimation of capital requirements.
