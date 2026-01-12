"""
preprocessing.py

Portfolio-friendly preprocessing utilities for the "Australian Rain" dataset.

This script is based on the workflow in your exported notebook HTML:
- load CSV
- one-hot encode selected categorical columns via pandas.get_dummies
- map Yes/No -> 1/0
- split into train/test
- (optional) StandardScaler for models that benefit from scaling (e.g., Logistic Regression, SVM)

Usage (example):
  python -m src.preprocessing --output_dir results --test_size 0.2 --random_state 10
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


DEFAULT_DATA_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMDeveloperSkillsNetwork-ML0101EN-SkillUp/labs/ML-FinalAssignment/Weather_Data.csv"
)

DEFAULT_DUMMY_COLS = ["RainToday", "WindGustDir", "WindDir9am", "WindDir3pm"]
TARGET_COL = "RainTomorrow"


@dataclass
class SplitData:
    X_train: np.ndarray
    X_test: np.ndarray
    y_train: np.ndarray
    y_test: np.ndarray
    feature_names: list[str]
    scaler: Optional[StandardScaler] = None


def load_data(path_or_url: str = DEFAULT_DATA_URL) -> pd.DataFrame:
    """Load the weather dataset from a local path or a URL."""
    return pd.read_csv(path_or_url)


def make_features(
    df: pd.DataFrame,
    dummy_cols: list[str] = DEFAULT_DUMMY_COLS,
    target_col: str = TARGET_COL,
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Create model-ready features.

    Notebook-derived steps:
    - pd.get_dummies on key categorical columns
    - replace 'No'/'Yes' with 0/1
    - split X and y by dropping target column
    """
    df_proc = pd.get_dummies(data=df, columns=dummy_cols)
    df_proc.replace(["No", "Yes"], [0, 1], inplace=True)

    if target_col not in df_proc.columns:
        raise ValueError(f"Target column '{target_col}' not found after preprocessing.")

    X = df_proc.drop(columns=target_col, axis=1)
    y = df_proc[target_col]
    return X, y


def split_data(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = 10,
    scale: bool = False,
) -> SplitData:
    """
    Split into train/test. Optionally scale features using StandardScaler.
    """
    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    scaler = None
    if scale:
        scaler = StandardScaler()
        x_train = scaler.fit_transform(x_train)
        x_test = scaler.transform(x_test)
    else:
        x_train = x_train.to_numpy()
        x_test = x_test.to_numpy()

    return SplitData(
        X_train=x_train,
        X_test=x_test,
        y_train=np.asarray(y_train),
        y_test=np.asarray(y_test),
        feature_names=list(X.columns),
        scaler=scaler,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Preprocess Australian Rain dataset.")
    parser.add_argument("--data", default=DEFAULT_DATA_URL, help="Local path or URL to CSV.")
    parser.add_argument("--test_size", type=float, default=0.2)
    parser.add_argument("--random_state", type=int, default=10)
    parser.add_argument("--scale", action="store_true", help="Apply StandardScaler.")
    parser.add_argument("--output_dir", default="results", help="Directory to write outputs.")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = load_data(args.data)
    X, y = make_features(df)

    split = split_data(X, y, test_size=args.test_size, random_state=args.random_state, scale=args.scale)

    # Save a lightweight artifact for reproducibility (feature list)
    (out_dir / "feature_names.txt").write_text("\n".join(split.feature_names), encoding="utf-8")
    print(f"Wrote feature_names.txt with {len(split.feature_names)} features to {out_dir.resolve()}")

    # Note: we don't save arrays by default; the training script will run end-to-end from raw data.


if __name__ == "__main__":
    main()
