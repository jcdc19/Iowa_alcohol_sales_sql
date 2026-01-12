# Executive Summary (Example Monthly Update)

## Reporting Period
Latest month in dataset vs prior month (MoM), using county as a proxy for “Key Account.”

## State of the Business (Topline)
Deliverable: `outputs/scorecard_latest_12mo.csv`

Recommended topline cuts:
- Total volume (liters) and sales ($) by account
- Top 10 accounts by volume in latest month
- MoM and YoY changes for key accounts

## Drivers and Detractors (Why Volume Changed)
Deliverable: `outputs/drivers_latest_month.csv`

Interpretation guide:
- **Top drivers** identify categories/items/stores contributing most positively to MoM volume change.
- **Top detractors** identify categories/items/stores contributing most negatively to MoM volume change.
- Use this to prepare stakeholder-ready “what changed and why” highlights.

Suggested talking points:
- “Volume increases were primarily driven by a small number of categories/items/stores…”
- “Volume declines were concentrated in specific categories/items or location losses…”

## Distribution / Active Locations (Coverage)
Deliverable: `outputs/distribution_changes_latest_12mo.csv`

Interpretation guide:
- **Gained locations** = stores active this month but not last month
- **Lost locations** = stores active last month but not this month
- **Net change** helps explain whether volume change is supported by distribution expansion or contraction

Suggested talking points:
- “Distribution expanded in X accounts (net +locations), supporting volume growth…”
- “Distribution contraction in Y accounts (net -locations) may explain volume softness…”

## Data Quality (Clean Reporting)
Deliverable: `outputs/dq_issues.csv`

Interpretation guide:
- Review duplicates, null key fields, and extreme outliers.
- In a business setting, these checks reduce reporting noise and prevent stakeholder confusion.

## Recommended Follow-Ups (Example)
1. Validate whether top detractor stores represent temporary stockouts/ordering changes or sustained declines.
2. For accounts with volume declines + location losses, investigate lost distribution and potential recovery opportunities.
3. Resolve any duplicate store identity issues to ensure clean customer list reporting.
