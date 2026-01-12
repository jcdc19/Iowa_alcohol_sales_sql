"""
train_models.py

Train multiple models for the Australian Rain decision-support portfolio.

This script mirrors the notebook's intent but fixes two portfolio-critical issues:
1) Treat RainTomorrow as a classification target for the final recommendation.
2) Ensure each model is trained/evaluated on the correct split/features.

Outputs:
- results/metrics_comparison.csv
- results/confusion_matrix_logistic.png (optional)
- results/confusion_matrix_knn.png (optional)
- results/confusion_matrix_svm.png (optional)

Usage:
  python -m src.train_models --output_dir results
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    jaccard_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeRegressor

from .preprocessing import DEFAULT_DATA_URL, make_features, load_data, split_data


@dataclass
class ClassifMetrics:
    accuracy: float
    f1: float
    jaccard: float


@dataclass
class RegrMetrics:
    mae: float
    mse: float
    r2: float


def evaluate_classification(y_true: np.ndarray, y_pred: np.ndarray) -> ClassifMetrics:
    return ClassifMetrics(
        accuracy=float(accuracy_score(y_true, y_pred)),
        f1=float(f1_score(y_true, y_pred)),
        jaccard=float(jaccard_score(y_true, y_pred)),
    )


def evaluate_regression(y_true: np.ndarray, y_pred: np.ndarray) -> RegrMetrics:
    return RegrMetrics(
        mae=float(mean_absolute_error(y_true, y_pred)),
        mse=float(mean_squared_error(y_true, y_pred)),
        r2=float(r2_score(y_true, y_pred)),
    )


def train_all(
    data_path_or_url: str = DEFAULT_DATA_URL,
    test_size: float = 0.2,
    random_state: int = 10,
    knn_k: int = 4,
    dt_max_depth: int = 8,
    dt_random_state: int = 35,
    lr_C: float = 0.01,
    svm_kernel: str = "rbf",
) -> Tuple[pd.DataFrame, Dict[str, np.ndarray]]:
    """
    Train models and return:
    - a metrics DataFrame (one row per model)
    - a dict of confusion matrices for classification models
    """
    df = load_data(data_path_or_url)
    X, y = make_features(df)

    # 1) Unscaled split for tree / KNN / linear regression
    split_unscaled = split_data(X, y, test_size=test_size, random_state=random_state, scale=False)

    # 2) Scaled split for logistic regression + SVM (common best practice)
    split_scaled = split_data(X, y, test_size=test_size, random_state=random_state, scale=True)

    rows = []
    confs: Dict[str, np.ndarray] = {}

    # Linear Regression baseline (treat as regression output on a binary target)
    lin = LinearRegression()
    lin.fit(split_unscaled.X_train, split_unscaled.y_train)
    yhat_lin = lin.predict(split_unscaled.X_test)
    met_lin = evaluate_regression(split_unscaled.y_test, yhat_lin)
    rows.append(
        dict(
            model="LinearRegression",
            task="regression_baseline",
            accuracy=np.nan,
            f1=np.nan,
            jaccard=np.nan,
            mae=met_lin.mae,
            mse=met_lin.mse,
            r2=met_lin.r2,
            notes="Baseline regression on binary target; included for comparison only.",
        )
    )

    # KNN (classification)
    knn = KNeighborsClassifier(n_neighbors=knn_k)
    knn.fit(split_unscaled.X_train, split_unscaled.y_train)
    yhat_knn = knn.predict(split_unscaled.X_test)
    met_knn = evaluate_classification(split_unscaled.y_test, yhat_knn)
    confs["KNN"] = confusion_matrix(split_unscaled.y_test, yhat_knn, labels=[1, 0])
    rows.append(
        dict(
            model=f"KNN(k={knn_k})",
            task="classification",
            accuracy=met_knn.accuracy,
            f1=met_knn.f1,
            jaccard=met_knn.jaccard,
            mae=np.nan,
            mse=np.nan,
            r2=np.nan,
            notes="Strong benchmark; less interpretable than logistic regression.",
        )
    )

    # Decision Tree Regressor baseline (from notebook)
    dtr = DecisionTreeRegressor(max_depth=dt_max_depth, random_state=dt_random_state)
    dtr.fit(split_unscaled.X_train, split_unscaled.y_train)
    yhat_dtr = dtr.predict(split_unscaled.X_test)
    met_dtr = evaluate_regression(split_unscaled.y_test, yhat_dtr)
    rows.append(
        dict(
            model=f"DecisionTreeRegressor(depth={dt_max_depth})",
            task="regression_baseline",
            accuracy=np.nan,
            f1=np.nan,
            jaccard=np.nan,
            mae=met_dtr.mae,
            mse=met_dtr.mse,
            r2=met_dtr.r2,
            notes="Interpretable rules; shown as regression baseline in notebook.",
        )
    )

    # Logistic Regression (interpretability-first recommendation)
    logr = LogisticRegression(C=lr_C, solver="liblinear")
    logr.fit(split_scaled.X_train, split_scaled.y_train)
    yhat_logr = logr.predict(split_scaled.X_test)
    met_logr = evaluate_classification(split_scaled.y_test, yhat_logr)
    confs["LogisticRegression"] = confusion_matrix(split_scaled.y_test, yhat_logr, labels=[1, 0])
    rows.append(
        dict(
            model=f"LogisticRegression(C={lr_C})",
            task="classification",
            accuracy=met_logr.accuracy,
            f1=met_logr.f1,
            jaccard=met_logr.jaccard,
            mae=np.nan,
            mse=np.nan,
            r2=np.nan,
            notes="Preferred: interpretable coefficients + probability outputs.",
        )
    )

    # SVM (classification, opaque; included for comparison)
    svm = SVC(kernel=svm_kernel)
    svm.fit(split_scaled.X_train, split_scaled.y_train)
    yhat_svm = svm.predict(split_scaled.X_test)
    met_svm = evaluate_classification(split_scaled.y_test, yhat_svm)
    confs["SVM"] = confusion_matrix(split_scaled.y_test, yhat_svm, labels=[1, 0])
    rows.append(
        dict(
            model=f"SVM(kernel={svm_kernel})",
            task="classification",
            accuracy=met_svm.accuracy,
            f1=met_svm.f1,
            jaccard=met_svm.jaccard,
            mae=np.nan,
            mse=np.nan,
            r2=np.nan,
            notes="Lower interpretability; useful as a comparison point.",
        )
    )

    metrics_df = pd.DataFrame(rows)
    return metrics_df, confs


def main() -> None:
    parser = argparse.ArgumentParser(description="Train models and export portfolio artifacts.")
    parser.add_argument("--data", default=DEFAULT_DATA_URL, help="Local path or URL to CSV.")
    parser.add_argument("--output_dir", default="results", help="Directory to write outputs.")
    parser.add_argument("--test_size", type=float, default=0.2)
    parser.add_argument("--random_state", type=int, default=10)
    parser.add_argument("--knn_k", type=int, default=4)
    parser.add_argument("--dt_max_depth", type=int, default=8)
    parser.add_argument("--dt_random_state", type=int, default=35)
    parser.add_argument("--lr_C", type=float, default=0.01)
    parser.add_argument("--svm_kernel", default="rbf")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    metrics_df, confs = train_all(
        data_path_or_url=args.data,
        test_size=args.test_size,
        random_state=args.random_state,
        knn_k=args.knn_k,
        dt_max_depth=args.dt_max_depth,
        dt_random_state=args.dt_random_state,
        lr_C=args.lr_C,
        svm_kernel=args.svm_kernel,
    )

    metrics_path = out_dir / "metrics_comparison.csv"
    metrics_df.to_csv(metrics_path, index=False)
    print(f"Wrote {metrics_path.resolve()}")

    # Save confusion matrices as CSV for easy viewing in GitHub
    for name, cm in confs.items():
        cm_path = out_dir / f"confusion_matrix_{name.lower()}.csv"
        pd.DataFrame(cm, index=["actual_1", "actual_0"], columns=["pred_1", "pred_0"]).to_csv(cm_path)
        print(f"Wrote {cm_path.resolve()}")


if __name__ == "__main__":
    main()
