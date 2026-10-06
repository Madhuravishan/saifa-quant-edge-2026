import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os

def plot_cumulative_performance(train_data, test_data, weights, out_path):
    plt.figure(figsize=(10, 6))
    
    # Calculate portfolio cumulative returns for full dataset
    full_data = train_data.copy()
    full_data = pd.concat([train_data, test_data])
    
    w = np.array([weights[c] for c in full_data.columns])
    port_ret = full_data.dot(w)
    cum_ret = (1 + port_ret).cumprod()
    
    plt.plot(cum_ret.index, cum_ret.values, label='Portfolio', color='blue')
    plt.axvline(x=test_data.index[0], color='red', linestyle='--', label='Out-of-Sample Start')
    plt.title('Figure 1: Portfolio Cumulative Performance (2012-2024)')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.grid(True)
    if out_path:
        plt.savefig(os.path.join(out_path, 'fig1_cumulative_performance.png'), dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_return_distributions(returns, out_path):
    plt.figure(figsize=(12, 4))
    for i, col in enumerate(returns.columns):
        plt.subplot(1, 3, i+1)
        sns.histplot(returns[col], bins=50, kde=True)
        plt.title(f'{col} Returns')
    plt.tight_layout()
    if out_path:
        plt.savefig(os.path.join(out_path, 'fig2_return_distributions.png'), dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_wavelet_decomposition(returns, decomp, asset='SPY', out_path=''):
    plt.figure(figsize=(12, 8))
    
    plt.subplot(4, 1, 1)
    plt.plot(returns.index, returns[asset], label='Original', color='black', alpha=0.7)
    plt.title(f'{asset} Original Returns')
    
    colors = ['red', 'green', 'blue', 'orange']
    comps = ['short', 'medium', 'long', 'trend']
    for i, comp in enumerate(comps):
        plt.subplot(4, 1, i+1)
        # Handle index correctly
        comp_data = decomp[comp][asset]
        plt.plot(returns.index[-len(comp_data):], comp_data, label=comp.capitalize(), color=colors[i], alpha=0.8)
        plt.title(f'{asset} {comp.capitalize()} Horizon Component')
        
    plt.tight_layout()
    if out_path:
        plt.savefig(os.path.join(out_path, 'fig3_wavelet_decomposition.png'), dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_tail_dependence(results_df, out_path):
    plt.figure(figsize=(10, 6))
    
    results_df.plot(kind='bar', figsize=(10,6), colormap='viridis')
    plt.title('Figure 4: Empirical Lower Tail Dependence (5% Threshold) by Horizon')
    plt.ylabel('Tail Dependence')
    plt.xticks(rotation=0)
    plt.grid(axis='y')
    
    if out_path:
        plt.savefig(os.path.join(out_path, 'fig4_tail_dependence.png'), dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_var_es_comparison(var_es_df, out_path):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # var_es_df has models as columns if we transpose, or we can just plot original
    # Let's assume var_es_df is the original risk_results (Models as index, VaR/ES as columns)
    
    var_es_df[['99% VaR']].plot(kind='bar', ax=axes[0], color=['blue'])
    axes[0].set_title('99% VaR Comparison')
    axes[0].set_ylabel('VaR')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(axis='y')
    
    var_es_df[['99% ES']].plot(kind='bar', ax=axes[1], color=['red'])
    axes[1].set_title('99% Expected Shortfall Comparison')
    axes[1].set_ylabel('Expected Shortfall')
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].grid(axis='y')
    
    plt.tight_layout()
    if out_path:
        plt.savefig(os.path.join(out_path, 'fig5_var_es_comparison.png'), dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_oos_violations(oos_returns, var_forecast, out_path):
    plt.figure(figsize=(10, 6))
    plt.plot(oos_returns.index, oos_returns, label='Portfolio Return', color='gray', alpha=0.7)
    
    # Plot VaR as a line
    plt.plot(oos_returns.index, var_forecast, color='red', label='99% VaR Forecast')
    
    # Highlight violations
    violations = oos_returns < var_forecast
    plt.scatter(oos_returns.index[violations], oos_returns[violations], color='red', marker='v', label='VaR Violation')
    
    plt.title('Figure 6: Out-of-Sample VaR Violations (Wavelet-Copula)')
    plt.xlabel('Date')
    plt.ylabel('Return')
    plt.legend()
    plt.grid(True)
    if out_path:
        plt.savefig(os.path.join(out_path, 'fig6_oos_violations.png'), dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()
