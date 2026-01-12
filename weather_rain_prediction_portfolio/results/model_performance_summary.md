# Model Performance Summary (Decision-Support Lens)

This project evaluates multiple models for next-day rainfall prediction with an interpretability-first philosophy.

## Extracted Results (from notebook output)
- **KNN (k=4)**: Accuracy **0.8183**, F1 **0.5966**, Jaccard **0.4251**
- **Logistic Regression (C=0.01, liblinear)**: Jaccard **0.5426**; confusion matrix printed in notebook output
- **SVM (RBF)**: Classification report indicates the model predicts **no positive class** (rain=1), yielding F1=0 for the positive class and overall accuracy ≈ **0.72**
- **Linear Regression (baseline)**: MAE **0.2563**, MSE **0.1157**, R² **0.4271**
- **Decision Tree Regressor (max_depth=8)**: MAE **0.1712**, MSE **0.2387**, R² **0.1523**

## Decision Recommendation (Interpretability First)
**Preferred: Logistic Regression**
- Produces probabilities (useful for risk-based planning thresholds)
- High interpretability and stakeholder explainability
- Transparent tradeoffs via confusion matrix + thresholding

**Benchmark: KNN**
- Strong baseline performance
- Less interpretable; can be sensitive to scaling and class imbalance

**Not recommended (as-is): SVM**
- In the current run, it fails to identify rain events (no predicted positives)
- Requires class weighting, tuning, and calibrated probabilities to be decision-usable

## Notes on Metric Integrity
- The notebook prints Decision Tree MAE/MSE/R² in a dictionary; a later table appears to swap MAE and MSE due to variable ordering. This summary uses the printed MAE/MSE/R² values.
- A later "SVM" metric table appears to reuse Logistic Regression predictions; therefore, it is not treated as valid SVM evaluation.
