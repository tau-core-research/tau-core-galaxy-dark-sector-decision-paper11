# Numeric Decision Thresholds v08

**Doc class:** numeric decision-threshold freeze
**Status:** numeric threshold rules frozen; no endpoint scores or verdicts
**Canonical parent:** Decision threshold v01

Script:

```text
scripts/build_numeric_decision_thresholds.py
```

Derived outputs:

```text
data/derived/numeric_decision_thresholds_v08.csv
data/derived/numeric_decision_thresholds_summary_v08.csv
```

This artifact freezes the numerical decision-threshold policy before endpoint
scores are evaluated. It does not evaluate any family, galaxy, control, or
held-out score.

The frozen policy is deliberately minimal:

```text
rank_required = 1 for M0/M1/M2 family-favoring labels
minimum_heldout_margin = 0
maximum_control_failures = 0
stability_required = true
UNRESOLVED is the only fallback label
```

The next required artifact is:

```text
scoring_preflight_v07.csv
```

## Claim Boundary

This artifact writes threshold rules only. It computes no endpoint scores,
evaluates no held-out ranking, runs no controls, writes no verdict labels, and
makes no dark-sector decision.

Claim boundary:

```text
numeric_decision_thresholds_v08_threshold_freeze_only_no_scores_no_verdict
```
