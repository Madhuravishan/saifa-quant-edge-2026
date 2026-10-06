# Data Audit

## Data Source
- **Provider**: Yahoo Finance via `yfinance` Python package.
- **Tickers**: SPY (S&P 500 ETF), TLT (20+ Year Treasury Bond ETF), GLD (SPDR Gold Trust).

## Period & Completeness
- **Start Date**: 2012-01-01
- **End Date**: 2026-10-06 (latest available at time of run)
- **Missing Values**: Forward-filled and backward-filled appropriately in `src/data.py` to handle minor holiday misalignments across asset classes.
- **Returns**: Log returns calculated as `ln(P_t / P_{t-1})` from Adjusted Close prices (to account for dividends and splits).

## Train/Test Separation
- **Training End Date**: 2023-12-31
- **Training Observations**: 3,017
- **Testing Observations**: 692
- **Integrity**: Verified 0 overlap between `train_rets` and `test_rets` in the `split_data` function.

**Audit Status:** PASS