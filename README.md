# SAIFA Quant Edge 1.0
## Risk Across Tails and Timescales

> **Wavelet–Copula Market Risk Framework for Horizon-Dependent Tail Dependence**

---

## Overview

This project was developed for the **SAIFA Quant Edge 1.0 — Round 1 Initial Screening Challenge**.

The central research question is:

> **Does tail dependence change with the investment horizon, and what does ignoring this do to a portfolio's measured risk?**

Financial assets may exhibit relatively moderate dependence during ordinary market conditions while becoming strongly connected during periods of extreme losses. Furthermore, the dependence observed over very short horizons may differ from the dependence observed over longer investment horizons.

This project combines:

- **Wavelet decomposition** to separate return movements by investment horizon;
- **Copula models** to capture dependence beyond ordinary linear correlation;
- **Lower-tail dependence analysis** to study joint extreme losses;
- **99% VaR and Expected Shortfall** to quantify portfolio tail risk;
- **Out-of-sample backtesting** to evaluate the model on unseen data;
- **A simple benchmark model** to determine whether the additional modelling complexity produces a meaningful risk-management benefit.

The objective is not simply to build a more complicated model.

The objective is to determine whether **horizon-dependent tail dependence materially changes measured portfolio risk** and whether that information improves risk measurement.

---

# Interactive Project Walkthrough

The central methodology, code, and conclusions of this project are documented in an interactive Jupyter Notebook. This is the **primary** way to evaluate the model logic step-by-step:

[**SAIFA_Quant_Edge_1_0_Research.ipynb**](notebooks/SAIFA_Quant_Edge_1_0_Research.ipynb)

---

# 1. Research Question

The project addresses five connected questions:

1. What portfolio are we studying and why is it economically meaningful?
2. Does lower-tail dependence change across investment horizons?
3. How much portfolio tail risk is missed when horizon-dependent dependence is ignored?
4. Does the proposed framework perform adequately against a simple benchmark on unseen data?
5. What practical action should a risk manager take based on the empirical findings?

---

# 2. Portfolio

The current portfolio consists of:

| Asset | Weight | Role |
|---|---:|---|
| SPY | 60% | Equity exposure |
| TLT | 30% | Long-duration Treasury exposure |
| GLD | 10% | Gold / alternative macro exposure |

### Important

These portfolio choices are **team methodological decisions**.

They are not prescribed by the SAIFA competition.

The portfolio was selected to create an economically interpretable multi-asset
risk problem in which diversification relationships can be studied across
different market horizons.

Portfolio weights:

\[
w_{SPY}=0.60,\qquad
w_{TLT}=0.30,\qquad
w_{GLD}=0.10
\]

and therefore:

\[
\sum_i w_i = 1.
\]

---

# 3. Data

## Data Source

Public market data are obtained from:

**Yahoo Finance**

using the Python `yfinance` package.

The project does not rely on a proprietary dataset.

The repository includes the required data-access/retrieval mechanism so that the
analysis can be reproduced.

## Sample Design

The intended research design is:

| Period | Purpose |
|---|---|
| 2012–2023 | Model training / estimation |
| 2024–latest complete available date | Out-of-sample evaluation |

These dates are **team methodological choices**, not competition requirements.

The exact effective dates used in the final run are documented in the generated
outputs and audit files.

## Data Processing

The preprocessing pipeline:

1. Downloads the selected market data.
2. Records the retrieval period.
3. Aligns asset observations by date.
4. Handles missing observations consistently.
5. Constructs return series.
6. Calculates log returns where appropriate.
7. Separates training and test periods.
8. Prevents test-period information from entering model estimation.

---

# 4. Methodology

The research framework follows four main stages.

```text
Market Prices
      │
      ▼
Data Cleaning & Log Returns
      │
      ▼
Train / Test Split
      │
      ▼
Wavelet Decomposition
      │
      ├──────── Short Horizon
      ├──────── Medium Horizon
      └──────── Long Horizon
                  │
                  ▼
            Copula Modelling
                  │
                  ▼
        Lower-Tail Dependence
                  │
                  ▼
       Joint Portfolio Simulation
                  │
                  ▼
             VaR / ES
                  │
                  ▼
        Benchmark Comparison
                  │
                  ▼
       Out-of-Sample Backtest
                  │
                  ▼
       Risk-Manager Recommendation

---

# 5. Deployment and GitHub Pages

## GitHub Pages Deployment
A static landing page has been set up for deployment via **GitHub Pages**.

- **Deployed URL:** [https://madhuravishan.github.io/saifa-quant-edge-2026/](https://madhuravishan.github.io/saifa-quant-edge-2026/)
- **Workflow:** The deployment uses the GitHub Actions workflow located at `.github/workflows/deploy-pages.yml`. It runs automatically on pushes to the `main` or `master` branch.
- **How to enable GitHub Pages:**
  1. Go to your repository settings on GitHub.
  2. Navigate to the **Pages** section on the left sidebar.
  3. Under **Build and deployment**, set the Source to **GitHub Actions**.

## Backend Hosting Requirements
This repository features a **Streamlit** Python dashboard (`app.py`). 
**Note:** GitHub Pages can only host static files (HTML, CSS, JavaScript). It cannot run the Python server needed for Streamlit. 

Therefore, the full interactive Streamlit dashboard requires a separate backend hosting service such as **Streamlit Community Cloud**, **Heroku**, or **Render**. The GitHub Pages deployment only serves a static landing page directing users to the backend or explaining local deployment.

## Local Testing Instructions
To test the interactive dashboard locally:
1. Clone the repository: `git clone https://github.com/Madhuravishan/saifa-quant-edge-2026.git`
2. Navigate into the project directory: `cd saifa-quant-edge-2026/quant_edge_project`
3. Install the dependencies: `pip install -r requirements.txt`
4. Run the Streamlit app: `streamlit run app.py`

## Environment Variables
This application uses public Yahoo Finance data via the `yfinance` package and does not currently require any API keys, secrets, or environment variables to run the local dashboard or to deploy the static GitHub Pages landing page. (If backend deployment requires them in the future, configure them as repository secrets.)