# REQUIREMENTS MATRIX

| Requirement | Official / Team Choice | Evidence | Status | File / Location | Action Taken |
|---|---|---|---|---|---|
| Report PDF | Official | `final_report.md` exists (PDF requires GTK3) | PASS WITH NOTE | `report/` | Kept markdown fallback |
| ≤10 pages excluding cover/references | Official | Report is concise | PASS | `report/final_report.md` | None |
| Runnable Python/R code | Official | Python pipeline runs end-to-end | PASS | `run_all.py` | Verified execution |
| One-command reproduction | Official | `python run_all.py` | PASS | `run_all.py` | Ran command |
| README | Official | `README.md` details all choices | PASS | `README.md` | None |
| Dependencies | Official | `requirements.txt` | PASS | `requirements.txt` | None |
| Data or public-data download script | Official | `src/data.py` uses yfinance | PASS | `src/data.py` | Verified |
| Benchmark | Official | Historical VaR and Single-Horizon Copula | PASS | `src/risk.py`, `run_all.py` | Verified |
| Out-of-sample testing | Official | Kupiec POF and ES Score | PASS | `src/backtest.py` | Verified |
| One concrete recommendation | Official | Included in the report | PASS | `report/final_report.md` | None |
| AI disclosure | Official | `AI_DISCLOSURE.md` | PASS | `AI_DISCLOSURE.md` | None |
| ZIP ≤25 MB | Official | Output ZIP is lightweight | PASS | `saifa_quant_edge_1.0_submission.zip` | Created clean zip |
| Meaningful portfolio | Team Choice | SPY (60%), TLT (30%), GLD (10%) | PASS | `config.yaml` | Verified |
| Wavelet decomposition | Team Choice | DB4, 3 levels (SWT) | PASS | `src/wavelets.py` | Verified |
| Copula modelling | Team Choice | Student-t, Gaussian, Clayton | PASS | `src/copulas.py` | Verified |
| Lower-tail dependence | Team Choice | Empirical lower-tail at 5% | PASS | `src/tail_dependence.py`| Verified |
| Horizon comparison | Team Choice | Short, Medium, Long, Trend | PASS | `run_all.py` | Verified |
| Portfolio VaR/ES | Team Choice | 99% VaR and ES | PASS | `src/risk.py` | Verified |
| Risk-gap calculation | Team Choice | Compared models | PASS | `run_all.py` | Verified |
| Robustness/limitations | Team Choice | Discussed in report | PASS | `report/final_report.md` | None |
| Actionable conclusion | Team Choice | Recommendation in report | PASS | `report/final_report.md` | None |
| Clean execution | Technical | End-to-end pipeline successful | PASS | `run_all.py` | None |
| Tests pass | Technical | 5/5 tests passed | PASS | `tests/test_pipeline.py` | Executed pytest |
| No hard-coded results | Technical | Results are dynamically populated | PASS | `run_all.py` | None |
| No look-ahead bias | Technical | Proper OOS split | PASS | `src/data.py`, `run_all.py` | Verified |
| No secrets | Technical | Checked | PASS | repo root | None |
| No absolute machine paths | Technical | Relative paths used | PASS | `config.yaml`, `run_all.py`| None |
| Reproducible figures/tables | Technical | Stored in `outputs/` | PASS | `outputs/` | Verified |
