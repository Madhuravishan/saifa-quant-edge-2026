# SAIFA Quant Edge 1.0: Elevator Pitches

## The 30-Second Pitch
We investigated whether tail dependence—how assets crash together—changes across different investment horizons, and whether ignoring this affects portfolio risk. By decomposing a 60/30/10 SPY/TLT/GLD portfolio using wavelets and modeling each horizon with copulas, we found that tail dependence does materially shift over time; for instance, SPY and GLD become twice as connected over longer horizons. However, we also discovered a critical danger: if a risk model treats these time horizons as independent signals, it mathematically erases the reality that market crashes happen across all horizons simultaneously. Doing this caused our model to severely underestimate 99% VaR, leading to massive out-of-sample failures compared to a simple historical benchmark. The takeaway for risk managers is clear: horizon-specific behavior exists, but it must be modeled jointly across time to avoid dangerous capital shortfalls.

## The 60-Second Pitch
Our project for the SAIFA Quant Edge challenge asks a fundamental risk management question: Does the diversification between equities, bonds, and gold change depending on the time horizon, and what happens to our Value at Risk if we model this incorrectly?

We took 12 years of daily data for SPY, TLT, and GLD and split it into a strict train/test set. Using the Maximum Overlap Discrete Wavelet Transform (MODWT), we separated the returns into short, medium, and long-term frequencies. We then applied copula models to measure the 5% lower-tail dependence at each horizon.

We found strong evidence that tail dependence is not constant. The likelihood of gold and equities crashing together increases significantly over longer horizons. However, our out-of-sample backtest revealed a crucial structural limitation. When we simulated portfolio risk by aggregating these horizons independently, the model forecasted a 99% VaR of -1.16%, vastly underestimating the historical benchmark of -1.80%. In our out-of-sample test of 692 days, the wavelet-copula model suffered 28 VaR violations—far above the expected 7. 

Our conclusion is a direct warning to risk managers: While assets behave differently across horizons, extreme market shocks cascade across all frequencies simultaneously. A model that isolates horizons without linking them via a meta-copula will fatally underestimate portfolio tail risk.
