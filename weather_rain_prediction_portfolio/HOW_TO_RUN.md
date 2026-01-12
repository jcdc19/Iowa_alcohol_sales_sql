# HOW_TO_RUN

This repo is designed to be easy to run locally on Windows.

## 1) Create/activate an environment (recommended)

### Option A — conda
```bash
conda create -n rain_portfolio python=3.11 -y
conda activate rain_portfolio
```

### Option B — venv
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

## 2) Install dependencies
```bash
pip install -U pip
pip install pandas numpy scikit-learn matplotlib
```

## 3) Run the full pipeline

From the **repo root**:

```bash
python -m src.train_models --output_dir results
python -m src.evaluation --results_dir results
```

### Expected outputs
After `train_models`:
- `results/metrics_comparison.csv`
- `results/confusion_matrix_knn.csv`
- `results/confusion_matrix_logisticregression.csv`
- `results/confusion_matrix_svm.csv`

After `evaluation`:
- `results/confusion_matrix_*.png` (one per confusion matrix)

## 4) If you cannot access the dataset URL (offline / restricted network)

Download the dataset CSV once (or use your existing file), then run:

```bash
python -m src.train_models --data "C:\path\to\Weather_Data.csv" --output_dir results
```

## Notes
- This portfolio is **interpretability-first**. Logistic Regression is positioned as the preferred model because it produces probabilities and is easy to explain to stakeholders.
- The `results/confusion_matrix_*.csv` files included in the repo may be placeholders or extracted from the notebook export; re-running the pipeline regenerates them from the data.
