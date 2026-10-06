import os
import shutil
import pandas as pd

def build():
    print("Building static dashboard...")
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    public_dir = os.path.join(os.path.dirname(project_root), "public")
    
    os.makedirs(public_dir, exist_ok=True)
    os.makedirs(os.path.join(public_dir, "assets"), exist_ok=True)
    
    # 1. Copy images
    fig_dir = os.path.join(project_root, "outputs", "figures")
    for f in os.listdir(fig_dir):
        if f.endswith('.png'):
            shutil.copy(os.path.join(fig_dir, f), os.path.join(public_dir, "assets", f))
            
    # 2. Read tables
    tables = {}
    tab_dir = os.path.join(project_root, "outputs", "tables")
    for f in os.listdir(tab_dir):
        if f.endswith('.csv'):
            name = f.replace('.csv', '')
            df = pd.read_csv(os.path.join(tab_dir, f))
            tables[name] = df.to_html(classes="table table-striped table-bordered", index=False)
            
    # 3. Create HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SAIFA Quant Edge 1.0 Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; }}
            .card {{ margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            .header {{ background-color: #2c3e50; color: white; padding: 20px 0; text-align: center; margin-bottom: 30px; }}
            img {{ max-width: 100%; height: auto; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>SAIFA Quant Edge 1.0 - Risk Model Validation</h1>
            <p>Wavelet-Copula Portfolio Risk Analysis</p>
        </div>
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <div class="card">
                        <div class="card-header"><h4>Executive Summary & Recommendation</h4></div>
                        <div class="card-body">
                            <p><strong>Key Insight:</strong> The Wavelet-Copula model yields a significantly less conservative VaR estimate compared to the naive Historical benchmark, and it experiences an unacceptable number of out-of-sample violations.</p>
                            <p><strong>Reasoning:</strong> By simulating wavelet horizons independently, the model assumes extreme shocks at different frequencies are uncorrelated. In reality, market crashes exhibit simultaneous extremes across all horizons (volatility clustering). Independent simulation mathematically destroys this cross-horizon dependence, underestimating risk.</p>
                            <p><strong>Actionable Advice:</strong> Risk managers must not treat different investment horizons as independent signals when simulating portfolio risk. A robust model must explicitly model the dependency across horizons (e.g., using a meta-copula).</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header"><h4>Cumulative Performance</h4></div>
                        <div class="card-body"><img src="assets/fig1_cumulative_performance.png" alt="Performance"></div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header"><h4>Wavelet Decomposition (SPY)</h4></div>
                        <div class="card-body"><img src="assets/fig3_wavelet_decomposition.png" alt="Wavelet"></div>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header"><h4>Risk Comparison (99%)</h4></div>
                        <div class="card-body">{tables.get('risk_comparison', 'N/A')}</div>
                    </div>
                    <div class="card">
                        <div class="card-header"><h4>VaR & ES Comparison</h4></div>
                        <div class="card-body"><img src="assets/fig5_var_es_comparison.png" alt="VaR ES"></div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header"><h4>Out-of-Sample Backtest</h4></div>
                        <div class="card-body">{tables.get('backtest_results', 'N/A')}</div>
                    </div>
                    <div class="card">
                        <div class="card-header"><h4>OOS Violations</h4></div>
                        <div class="card-body"><img src="assets/fig6_oos_violations.png" alt="OOS Violations"></div>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-12">
                    <div class="card">
                        <div class="card-header"><h4>Tail Dependence by Horizon</h4></div>
                        <div class="card-body">
                            {tables.get('tail_dependence', 'N/A')}
                            <img src="assets/fig4_tail_dependence.png" alt="Tail Dependence" class="mt-3">
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(os.path.join(public_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print("Dashboard built at", public_dir)

if __name__ == "__main__":
    build()
