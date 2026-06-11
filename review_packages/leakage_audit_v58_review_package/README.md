# Leakage Audit v58 Review Package

**Status:** review package only; not leakage evidence; no activation; no endpoint scoring.

This package is for reviewing the current Paper 11 leakage frontier before any
row can be considered for scoring activation.

## Reviewer Tasks

1. Review each of the 72 template rows: 18 galaxies times four leakage checks.
2. Verify that source routes and observed-input handling are pre-score.
3. Verify morphology/readout labels are not derived from endpoint residuals,
   family winners, or best-fit score outcomes.
4. Verify benchmark/profile inputs were frozen before family comparison.
5. Only a later ingestion gate may consume a completed response as active
   `data/input/leakage_audit_evidence_v10.csv`.

## Required Checks

```text
LEC10_SOURCE_ROUTE
LEC10_OBSERVED_INPUTS
LEC10_MORPH_LABELS
LEC10_BENCHMARK_INPUTS
```

## Hard Stops

- Do not treat this package as active leakage evidence.
- Do not copy the template into `data/input/leakage_audit_evidence_v10.csv`
  without a separate completed review response and ingestion gate.
- Do not mark leakage rows as passed from template rows.
- Do not activate scoring rows or compute model-family scores from this package.
- Do not use endpoint residuals, family winners, or score outcomes to approve
  leakage evidence.
