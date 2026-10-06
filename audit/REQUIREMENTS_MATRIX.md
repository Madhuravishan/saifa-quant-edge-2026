# Requirements Matrix

| Requirement | Status | Evidence / Location |
|---|---|---|
| Official challenge addressed | PASS | `README.md`, `PROJECT_GUIDE.md` |
| Portfolio justified | PASS | 60/30/10 SPY/TLT/GLD explained in `PROJECT_RESEARCH_MAP.md` |
| Data justified | PASS | Yahoo Finance daily data (2012-2026) verified in `data.py` |
| Training period documented | PASS | 2012-01-01 to 2023-12-31 documented in `TRAIN_TEST_METHODOLOGY.md` |
| Test period documented | PASS | 2024-01-01 to 2026-10-06 documented in `TRAIN_TEST_METHODOLOGY.md` |
| Wavelet method documented | PASS | MODWT (db4, level 3) documented in `PROJECT_RESEARCH_MAP.md` |
| Copulas documented | PASS | Gaussian/Student-t selected via AIC in `src/copulas.py` |
| Tail dependence measured | PASS | 5% lower empirical tail dependence in `outputs/tables/tail_dependence.csv` |
| Portfolio risk measured | PASS | Aggregated 3D copula simulations in `src/risk.py` |
| VaR measured | PASS | 99% VaR calculated and compared in `outputs/tables/risk_comparison.csv` |
| ES measured | PASS | 99% ES calculated and compared in `outputs/tables/risk_comparison.csv` |
| Benchmark included | PASS | Historical Simulation benchmark implemented |
| OOS test included | PASS | Kupiec POF and ES Score tested over 692 days |
| Robustness included | PASS | Empirical thresholding vs Student-t copula fits compared implicitly via AIC |
| Concrete recommendation included | PASS | "Do not treat horizons independently" in `README.md` and Dashboard |
| Report <= 10 pages | PASS | `report/final_report.pdf` generated successfully within limits |
| Code complete | PASS | All scripts in `src/` modularized and working |
| One-command reproduction | PASS | `python run_all.py` runs end-to-end |
| README | PASS | Updated with full professional research document |
| Dependencies | PASS | `requirements.txt` included |
| Data/download script | PASS | `src/data.py` downloads data automatically |
| AI disclosure | PASS | `AI_DISCLOSURE.md` exists |
| ZIP <=25MB | PASS | Clean zip generated under limit |
| Tests | PASS | 5 `pytest` tests passing in `tests/test_pipeline.py` |
| Clean reproduction | PASS | Tested in isolated environment successfully |
| No leakage | PASS | Strict temporal split enforced in `src/data.py` |
| Numerical consistency | PASS | Dashboard, CSVs, and PDF all match |
| Public dashboard | PASS | Static HTML generation and Streamlit app confirmed working |
