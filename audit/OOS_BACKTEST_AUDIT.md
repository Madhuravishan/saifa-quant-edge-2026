# Out-of-Sample Backtest Audit

## Data Integrity
- **Test Set:** 2024-01-01 to 2026-10-06 (692 Observations).
- **Leakage Check:** 0 overlapping days with training data.
- **Parameter Fixing:** VaR and ES thresholds (-1.167% and -1.779%) were passed as static scalar values to the testing function. No rolling recalculation was performed.

## Metric Validation
- **Expected Violations:** 6.92 (1% of 692)
- **Historical Benchmark Actual Violations:** 5
- **Historical Benchmark Kupiec POF p-value:** 0.440 (Pass)
- **Wavelet-Copula Actual Violations:** 28
- **Wavelet-Copula Kupiec POF p-value:** 1.328e-09 (Fail)

## Conclusion
The OOS backtest code in `src/backtest.py` correctly implements the Kupiec Proportion of Failures test and properly counts violations based on fixed thresholds. The results are genuine and have not been manipulated to make the proposed model appear superior. The failure of the proposed model is fully documented and serves as the primary empirical evidence for the project's risk-management recommendation.