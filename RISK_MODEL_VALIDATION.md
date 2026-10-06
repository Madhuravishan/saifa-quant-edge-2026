# Risk Model Validation: Understanding "Accuracy"

When building a standard machine learning model (e.g., predicting whether a stock goes up or down), we measure success using "Accuracy" (e.g., 85% correct predictions). 

**Risk forecasting (VaR and ES) is fundamentally different.** 

We are not trying to predict the exact return of the portfolio tomorrow. We are trying to predict the *boundary* of extreme losses.

If a team member asks, *"Is our 99% VaR model 99% accurate?"*, the answer requires defining what accuracy means in risk management.

## 1. Coverage (The Kupiec POF Test)
For a 99% VaR model, we *expect* the portfolio to lose more than the VaR threshold exactly 1% of the time. 

- If we have 692 days of out-of-sample test data, we expect: `692 * 0.01 = 6.92` violations.
- **Historical Benchmark:** Had 5 violations. This is very close to 6.92. The Kupiec test p-value is 0.44 (values > 0.05 mean we cannot reject the model). This model is "accurate" in terms of coverage.
- **Wavelet-Copula Model:** Had 28 violations. This is a massive failure. The p-value is 1.3e-09. 

A model with 0 violations is also a bad model—it means the VaR is far too conservative and is forcing the firm to hold too much capital. "Accuracy" means hitting the 1% target as closely as possible.

## 2. Expected Shortfall (ES) Severity
VaR only tells us the boundary. Expected Shortfall tells us the average severity of the losses *when a violation occurs*.

If our ES forecast is -2.0%, but the average actual loss during violations is -4.0%, our model is failing to capture tail severity, even if the VaR violation count is correct. In our backtest, we use an ES Score (Actual average shortfall minus Forecasted shortfall) to diagnose this.

## 3. Independence (Clustering)
Though not formally tested via Christoffersen in our pipeline, a truly "accurate" risk model should have independent violations. If our expected 7 violations all happen in the same week during a market crash, the model is slow to react to changing volatility regimes. 

## The Team Takeaway
Do not hide the fact that the Wavelet-Copula model had 28 violations. This "failure" is the core empirical finding of the project: it proves that assuming independence across time horizons mathematically destroys the cross-horizon dependence needed to accurately forecast portfolio risk. The historical benchmark's success serves as the control group proving this point.
