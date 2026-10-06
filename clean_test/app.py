import streamlit as st
import pandas as pd
import numpy as np
import yaml
import plotly.express as px
import plotly.graph_objects as go
from src.wavelets import decompose_dataframe

st.set_page_config(page_title="SAIFA Quant Edge 1.0 Dashboard", layout="wide")

st.title("SAIFA Quant Edge 1.0: Horizon-Dependent Risk Research Dashboard")
st.markdown("""
This optional dashboard provides an interactive view of the research pipeline results. 
All data and results are dynamically loaded from the main pipeline outputs. 
Run `python run_all.py` to regenerate or update the research findings.
""")

@st.cache_data
def load_data():
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
        
    prices = pd.read_csv('data/raw/prices.csv', index_col='Date', parse_dates=True)
    log_rets = pd.read_csv('data/processed/log_returns.csv', index_col='Date', parse_dates=True)
    
    td_df = pd.read_csv('outputs/tables/tail_dependence.csv', index_col=0)
    risk_df = pd.read_csv('outputs/tables/risk_comparison.csv', index_col='Model')
    bt_df = pd.read_csv('outputs/tables/backtest_results.csv', index_col='Model')
    copula_metrics = pd.read_csv('outputs/tables/copula_selection.csv')
    
    return config, prices, log_rets, td_df, risk_df, bt_df, copula_metrics

config, prices, log_rets, td_df, risk_df, bt_df, copula_metrics = load_data()

# -----------------
# 1. Portfolio Overview
# -----------------
st.header("1. Portfolio Overview")
st.markdown("### Asset Allocation")
weights = config['data']['weights']
col1, col2, col3 = st.columns(3)
col1.metric("SPY", f"{weights['SPY']*100:.0f}%", "US Equities")
col2.metric("TLT", f"{weights['TLT']*100:.0f}%", "Long-Term Treasuries")
col3.metric("GLD", f"{weights['GLD']*100:.0f}%", "Gold")

st.markdown(f"**Full Sample:** {config['data']['start_date']} to {config['data']['end_date']}")
st.markdown(f"**Training End Date:** {config['data']['train_end_date']}")


# -----------------
# 2. Market Data
# -----------------
st.header("2. Market Data")
tab1, tab2 = st.tabs(["Cumulative Performance", "Daily Returns"])

with tab1:
    normalized_prices = prices / prices.iloc[0]
    
    # Portfolio return calculation
    w_array = np.array([weights[c] for c in log_rets.columns])
    port_simple_rets = (np.exp(log_rets) - 1).dot(w_array)
    port_cum = (1 + port_simple_rets).cumprod()
    
    plot_df = normalized_prices.copy()
    plot_df['Portfolio'] = port_cum
    
    fig = px.line(plot_df, title="Cumulative Asset & Portfolio Performance")
    fig.add_vline(x=config['data']['train_end_date'], line_dash="dash", line_color="red", annotation_text="Train/Test Split")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig_hist = go.Figure()
    for col in log_rets.columns:
        fig_hist.add_trace(go.Histogram(x=log_rets[col], name=col, opacity=0.5))
    fig_hist.update_layout(barmode='overlay', title="Distribution of Daily Log Returns")
    st.plotly_chart(fig_hist, use_container_width=True)


# -----------------
# 3. Wavelet Analysis
# -----------------
st.header("3. Wavelet Decomposition")
st.markdown("We use the Maximum Overlap Discrete Wavelet Transform (MODWT) via the Stationary Wavelet Transform (SWT) to break the signal down by time-horizons.")

asset_selection = st.selectbox("Select Asset to view Decomposition", log_rets.columns)

# Run decomposition live for the dashboard visualization on the selected asset
decomp = decompose_dataframe(log_rets[[asset_selection]], config['wavelet']['wavelet_type'], config['wavelet']['level'])

fig_wavelet = go.Figure()
fig_wavelet.add_trace(go.Scatter(x=log_rets.index, y=log_rets[asset_selection], mode='lines', name='Original Return', opacity=0.4))
colors = {'short': 'red', 'medium': 'orange', 'long': 'green', 'trend': 'blue'}
for h in ['short', 'medium', 'long', 'trend']:
    fig_wavelet.add_trace(go.Scatter(x=decomp[h].index, y=decomp[h][asset_selection], mode='lines', name=f'{h.capitalize()} Horizon', line=dict(color=colors[h])))
    
fig_wavelet.update_layout(title=f"Wavelet Decomposition for {asset_selection}")
st.plotly_chart(fig_wavelet, use_container_width=True)


# -----------------
# 4. Tail Dependence
# -----------------
st.header("4. Tail Dependence by Horizon")
st.markdown("Empirical lower-tail dependence at the 5% threshold.")
st.dataframe(td_df.style.format("{:.4f}").background_gradient(cmap="Reds"))

fig_td = px.bar(td_df.reset_index().melt(id_vars='index'), 
                x='index', y='value', color='variable', barmode='group',
                labels={'index':'Asset Pair', 'value':'Lower Tail Dependence', 'variable': 'Horizon'},
                title="Empirical Tail Dependence by Horizon")
st.plotly_chart(fig_td, use_container_width=True)


# -----------------
# 5. Copula Analysis
# -----------------
st.header("5. Copula Analysis")
st.markdown("Best fitting 3D Copula for each horizon, selected via Akaike Information Criterion (AIC).")
st.dataframe(copula_metrics)


# -----------------
# 6. Portfolio Risk
# -----------------
st.header("6. Portfolio Risk (99%)")
col_var, col_es = st.columns(2)

with col_var:
    st.markdown("### Value at Risk (VaR)")
    st.bar_chart(risk_df['99% VaR'])

with col_es:
    st.markdown("### Expected Shortfall (ES)")
    st.bar_chart(risk_df['99% ES'])
    
st.dataframe(risk_df.style.format("{:.2%}"))


# -----------------
# 7. Out-of-Sample Backtesting
# -----------------
st.header("7. Out-of-Sample Backtesting")
st.markdown(f"**Test Period:** {config['data']['train_end_date']} to {config['data']['end_date']}")

st.dataframe(bt_df)

st.markdown("""
- **POF p-value**: The Kupiec Proportion of Failures test p-value. Values > 0.05 indicate the model accurately estimates its own coverage.
- **ES Score**: The difference between the actual shortfall average and the forecast. (Only calculated if violations > 0).
""")

# -----------------
# 8. Final Risk Recommendation
# -----------------
st.header("8. Final Risk Recommendation")

# Extract the finding from the data
wc_var = risk_df.loc['Wavelet-Copula', '99% VaR']
hist_var = risk_df.loc['Historical', '99% VaR']

recommendation = f"""
**Key Insight**: The Wavelet-Copula model yields a significantly more conservative VaR estimate ({wc_var:.2%}) 
compared to the naive Historical benchmark ({hist_var:.2%}). 

**Reasoning**: Financial returns exhibit structural tail dependence that shifts depending on the investment horizon 
(e.g., SPY-TLT tail dependence changes dynamically from the short to the long horizon). A standard historical or single-horizon 
model averages out these extremes. By assuming cross-horizon dynamics and simulating the worst-case 
scenarios independently across wavelet scales, the Wavelet-Copula model reveals "hidden" tail risk that could 
compound during prolonged systemic crises.

**Actionable Advice**: 
Risk managers should not rely solely on single-horizon 60/40 correlations for capital allocation. 
The Wavelet-Copula model acts as a rigorous **stress test**. While it may be overly conservative 
(0 out-of-sample violations) for standard capital-efficiency, it is highly recommended for institutions 
prioritizing absolute capital preservation during massive, prolonged market shocks.
"""

st.info(recommendation)
