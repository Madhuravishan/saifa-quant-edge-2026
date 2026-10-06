# Technical Pitch (3 Minutes)

"Good morning, Judges. Our project investigates a critical vulnerability in standard risk models: the assumption that asset dependence, particularly during market crashes, is uniform across time horizons. 

We constructed a 60/30/10 portfolio of SPY, TLT, and GLD using 12 years of daily data. We established a strict out-of-sample cutoff at the end of 2023 to prevent look-ahead bias.

To analyze horizon dependence, we applied the Maximum Overlap Discrete Wavelet Transform (MODWT) using a Daubechies 4 wavelet. This allowed us to decompose our daily log returns into additive frequency bands representing short (2-4 day), medium (4-8 day), and long (8-16 day) market dynamics, without losing temporal alignment. 

Within each horizon, we mapped the marginal distributions to pseudo-uniforms via empirical CDFs and fitted 3D Student-t and Gaussian copulas using Maximum Likelihood, selecting the best fit via AIC. We also measured empirical lower-tail dependence at the 5% threshold.

Our first finding confirms our hypothesis: tail dependence is heavily horizon-dependent. For example, the tail dependence between US Equities and Gold doubles from 0.086 at the short horizon to 0.180 at the long horizon. Diversification properties fundamentally change depending on the persistence of the market shock.

However, our second finding is a critical warning about risk aggregation. To calculate a portfolio-level 99% VaR and Expected Shortfall, we simulated 10,000 paths from the fitted copula at each horizon, transformed them back via inverse ECDFs, and summed them taking advantage of the wavelet's linear reconstruction property. 

This Wavelet-Copula model forecasted a 99% VaR of -1.16%, which was significantly less conservative than our Historical Simulation benchmark of -1.80%. 

When we ran our out-of-sample backtest over the 692 days from 2024 to present, the benchmark performed perfectly with 5 violations against an expected 6.9. Our Wavelet-Copula model suffered 28 violations, decisively failing the Kupiec POF test.

Why did this happen? Because by simulating the horizons independently, our model assumed that high-frequency shocks and low-frequency shocks are uncorrelated. In real financial markets, extreme crashes exhibit volatility clustering across all frequencies simultaneously. 

Therefore, our recommendation to risk managers is clear: You must account for the fact that tail dependence changes across horizons. But if you model those horizons independently without a meta-copula to capture cross-horizon dependence, you will mathematically diversify away the very crashes you are trying to protect against, leading to a catastrophic undercapitalization."
