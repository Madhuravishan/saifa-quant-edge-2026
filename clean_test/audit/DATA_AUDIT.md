# DATA AUDIT

- **Source**: Yahoo Finance (`yfinance`).
- **Tickers**: SPY, TLT, GLD.
- **Timeframe**: 2012-01-01 to 2026-10-06.
- **Train/Test Split**: Train ends at 2023-12-31.
- **Handling Missing Values**: Forward fill then backward fill.
- **Returns**: Daily simple returns for portfolio aggregation, log returns for modeling.
- **Look-Ahead Bias**: None. The training data does not incorporate any information post-2023-12-31 for copula modeling, wavelet fitting, or threshold computation.