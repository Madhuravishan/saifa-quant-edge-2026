# Dashboard Audit

## Local Streamlit Dashboard (`app.py`)
- **Data Loading**: Loads all required data statically from `outputs/tables/` and `data/raw/`. Does not perform expensive model fitting on load.
- **Wavelet Interaction**: The decomposition visualization is interactive and allows the user to select the asset. The `decompose_dataframe` function is called efficiently on just the selected asset.
- **Visuals**: Uses Plotly for high-quality, interactive charting of cumulative performance, histograms, tail dependence, and backtest results.
- **Recommendation**: Clearly states the actionable risk-manager recommendation derived from the research.

**Audit Status:** PASS
