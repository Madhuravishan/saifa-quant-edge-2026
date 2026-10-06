# OOS BACKTEST AUDIT

- **Test Period**: 2024-01-01 to End of available data.
- **Independence**: The models are entirely calibrated on the train split. No parameters are refit on the test set.
- **VaR/ES thresholds**: Utilized fixed thresholds calibrated from the training set.
- **Methodology**:
  - Kupiec Proportion of Failures (POF) test
  - Expected Shortfall Severity Score
- **Results**: The backtest highlights the Wavelet-Copula model yields much more conservative risk metrics than historical measures.