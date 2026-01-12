# Weather Forecasting as a Decision Support System (Decision Science Case Study)

## Problem
Weather-sensitive decisions (planning, staffing, routing, inventory buffers) are impacted by next-day rainfall risk.  
The goal is to **support decisions under uncertainty**, not just maximize a single accuracy number.

## Objective
Evaluate multiple modeling approaches for *RainTomorrow* and compare them using decision-relevant metrics, prioritizing:
- Interpretability and risk transparency
- Stable performance across metrics
- Clear misclassification tradeoffs (false negatives vs false positives)

## Methodology (Notebook → Modular Repo)
This repo follows the same flow as the notebook export:
1. Load dataset
2. One-hot encode key categorical variables (`RainToday`, wind direction fields)
3. Map Yes/No to 1/0
4. Train-test split
5. Train multiple models
6. Evaluate with accuracy, F1, Jaccard, and confusion matrices
7. Make an interpretability-first model recommendation

## Models Evaluated
- Linear Regression (baseline, regression framing)
- KNN Classifier (benchmark)
- Decision Tree Regressor (baseline / rule exploration)
- Logistic Regression (**preferred**)
- SVM (comparison model; lower explainability)

## Decision Recommendation (Interpretability First)
**Preferred model: Logistic Regression**
- Interpretable coefficients
- Probability outputs support threshold-based risk policies
- Works well as a decision-support layer (not just a “prediction”)

## Outputs
After running training:
- `results/metrics_comparison.csv` — model comparison table
- `results/confusion_matrix_*.csv` — confusion matrices per classifier
- (optional) `results/confusion_matrix_*.png` — plotted matrices

## How to Run (Windows-friendly)
From repo root:

```bash
python -m src.train_models --output_dir results
python -m src.evaluation --results_dir results
```
