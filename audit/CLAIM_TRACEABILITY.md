# Claim Traceability

This document maps the scientific claims made in the report to the exact lines of code and data outputs that generate them.

| Claim in Report | Traceability (Code / Output) |
|---|---|
| "Tail dependence changes with horizon" | Derived from `src/tail_dependence.py`. Results found in `outputs/tables/tail_dependence.csv`. |
| "Wavelet-Copula underestimates VaR" | Derived from `src/risk.py` aggregating simulated horizons. Found in `outputs/tables/risk_comparison.csv`. |
| "Wavelet-Copula model fails out-of-sample" | Derived from `src/backtest.py` Kupiec POF test. Found in `outputs/tables/backtest_results.csv` (28 violations). |
| "Historical Benchmark VaR provides adequate coverage" | Derived from `src/backtest.py`. Found in `outputs/tables/backtest_results.csv` (5 violations). |

**Audit Status:** PASS (No fabricated claims detected).
