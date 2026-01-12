"""
evaluation.py

Lightweight plotting utilities (optional) for confusion matrices.

This keeps plotting separate so your repo stays clean: training produces CSVs;
plotting is an optional add-on.

Usage:
  python -m src.evaluation --metrics_csv results/metrics_comparison.csv --results_dir results
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_confusion_matrix(
    cm: np.ndarray,
    classes: Iterable[str],
    title: str,
    normalize: bool = False,
    save_path: Optional[Path] = None,
) -> None:
    """
    Plot a confusion matrix (adapted from your notebook's helper).
    """
    cm_plot = cm.astype(float)
    if normalize:
        denom = cm_plot.sum(axis=1, keepdims=True)
        denom[denom == 0] = 1.0
        cm_plot = cm_plot / denom

    plt.figure()
    plt.imshow(cm_plot, interpolation="nearest")
    plt.title(title)
    plt.colorbar()

    tick_marks = np.arange(len(list(classes)))
    plt.xticks(tick_marks, list(classes), rotation=45)
    plt.yticks(tick_marks, list(classes))

    fmt = ".2f" if normalize else "d"
    thresh = cm_plot.max() / 2.0 if cm_plot.size else 0.0

    for i in range(cm_plot.shape[0]):
        for j in range(cm_plot.shape[1]):
            plt.text(
                j,
                i,
                format(cm_plot[i, j], fmt),
                horizontalalignment="center",
                color="white" if cm_plot[i, j] > thresh else "black",
            )

    plt.ylabel("True label")
    plt.xlabel("Predicted label")
    plt.tight_layout()

    if save_path is not None:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
    else:
        plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot confusion matrices from CSV outputs.")
    parser.add_argument("--results_dir", default="results", help="Directory containing confusion_matrix_*.csv")
    parser.add_argument("--normalize", action="store_true")
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    for cm_csv in sorted(results_dir.glob("confusion_matrix_*.csv")):
        cm = pd.read_csv(cm_csv, index_col=0).to_numpy()
        model_name = cm_csv.stem.replace("confusion_matrix_", "")
        save_path = results_dir / f"confusion_matrix_{model_name}.png"
        plot_confusion_matrix(
            cm,
            classes=["rain_tomorrow=1", "rain_tomorrow=0"],
            title=f"Confusion Matrix: {model_name}",
            normalize=args.normalize,
            save_path=save_path,
        )
        print(f"Wrote {save_path.resolve()}")


if __name__ == "__main__":
    main()
