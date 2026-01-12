# Weather Forecasting for Planning Under Uncertainty
### Supply Chain & Operations Analytics Framing

## Executive Overview

This project treats rainfall prediction as an **operations planning problem** under uncertainty.

Rather than focusing solely on prediction accuracy, the emphasis is on:

- How forecast errors propagate through operational systems
- How different models expose different risk profiles
- How planners can use forecasts for buffer design, scheduling, and contingency planning

---

## Why This Matters for Operations

Weather uncertainty directly affects:

- Transportation reliability
- Lead times
- Labor scheduling
- Safety stock
- Service-level agreements (SLAs)
- Facility utilization

In these systems, **forecast errors create real costs**.

---

## Problem Framing

The key operational question is not:

> “Can we predict rain?”

It is:

> “How should we plan given uncertainty about rain?”

---

## Modeling Approach

Multiple models were trained to reflect different operational preferences:

| Model | Ops Interpretation |
|------|------------------|
| Linear Regression | Baseline signal |
| KNN | Similar-day matching |
| Decision Tree | Rule-based planning |
| Logistic Regression | Risk probability modeling |
| SVM | Complex nonlinear boundaries |

---

## Evaluation Through an Ops Lens

Operations decisions require understanding failure modes.

Metrics used:

- Accuracy
- F1 Score
- Jaccard Index
- Confusion Matrices

These allow us to quantify:
- Under-preparation risk (false negatives)
- Over-preparation cost (false positives)
- Stability vs sensitivity

---

## Key Operational Insights

- Some models optimize global accuracy at the expense of critical events.
- False negatives are often more costly than false positives.
- Interpretable models improve trust and adoption.
- Confusion matrices provide more value than single-number KPIs.

---

## Real-World Applications

This framework could be extended to:

- Dynamic safety stock sizing
- Weather-aware routing
- Contingency staffing
- Service-level planning
- Scenario-based scheduling

---

## Skills Demonstrated

- Operations-aware modeling
- Risk-based evaluation
- Tradeoff analysis
- Decision framing
- Scenario thinking
- Planning under uncertainty
