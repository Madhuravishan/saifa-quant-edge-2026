# REPRODUCIBILITY TEST

## Execution Date
2026-10-06

## Environment
- Python version: 3.14.0
- Required packages installed from `requirements.txt`

## Procedure
1. Ran `venv\Scripts\pytest.exe`. All 5 tests passed successfully.
2. Ran `venv\Scripts\python.exe run_all.py`.
3. Observed successful data download.
4. Observed wavelet decomposition, copula fitting, and risk calculations.
5. Confirmed output CSV files populated in `outputs/tables/`.
6. Confirmed images generated in `outputs/figures/`.
7. Confirmed report generation in `report/final_report.md`.

## Result
**PASS.** The project is fully reproducible with a single command without any manual intervention or hard-coded assumptions.