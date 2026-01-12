# On-Premise Key Accounts Analytics (SQL + Python + DuckDB)

## Overview
This project simulates a CPG on-premise analytics workflow: monthly scorecards, driver/detractor attribution, distribution (active location) tracking, and data quality checks. The goal is to produce repeatable reporting outputs that support monthly business reviews and stakeholder updates.

The analysis mirrors common on-premise reporting needs:
- Refresh monthly scorecards and “state of the business” updates
- Explain month-over-month changes via drivers and detractors
- Track distribution via gained/lost active locations
- Maintain clean reporting via data quality checks

## Data
Source: Iowa Liquor Sales (public data) extracted to a local CSV for analysis.  
The logic is designed to generalize to CPG on-premise account reporting datasets.

Key fields used:
- Date (sale_date, sale_month)
- Location/store (store_id, store_name, city, county)
- Product (category_name, item_description)
- Measures (volume_liters, sale_dollars, bottles_sold)

## Tech Stack
- DuckDB (SQL execution engine)
- Python (pandas for loading CSV, DuckDB connection)
- Jupyter Notebook (build/export pipeline)

## How to Run
1. Place the extracted CSV in `data/iowa_extract.csv`
2. Open `notebooks/00_build_and_export_outputs.ipynb`
3. Run all cells to:
   - Create canonical views in DuckDB
   - Export portfolio deliverables into `outputs/`

## Project Structure
- `data/` raw input CSV
- `sql/` reusable SQL view definitions
- `notebooks/` build pipeline notebook
- `outputs/` exported deliverables (CSV)
- `README.md` project overview + run instructions
- `EXECUTIVE_SUMMARY.md` example monthly business narrative

## Key Outputs (in /outputs)
- `scorecard_latest_12mo.csv`
  - Monthly KPIs by “account” (county proxy): volume, sales, active locations, MoM/YoY metrics
- `drivers_latest_month.csv`
  - Top drivers/detractors of month-over-month volume change by category, item, and store
- `distribution_changes_latest_12mo.csv`
  - Gained/lost active locations month-over-month (distribution proxy)
- `dq_issues.csv`
  - Data quality exceptions (nulls, duplicates, outliers)

## Core SQL Views (in /sql)
- `v_sales_clean`: typed/standardized base view used by all downstream reporting
- `v_monthly_scorecard`: account-month KPIs
- `v_monthly_trends`: MoM/YoY deltas + rolling metrics
- `v_drivers_detractors`: driver attribution for latest month
- `v_distribution_changes`: gained/lost locations by month
- `v_data_quality_issues`: exception reporting for clean reporting

## Notes
“Key Account” is represented using `county` as a proxy in this public dataset. In a company setting, this would map to customer/account hierarchies and customer lists.
