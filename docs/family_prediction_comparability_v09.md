# Family Prediction Comparability v09

**Doc class:** family prediction comparability gate
**Status:** M0 adequacy basis available; full M0/M1/M2 comparison blocked

Script:

```text
scripts/build_family_prediction_comparability.py
```

Derived outputs:

```text
data/derived/family_prediction_comparability_v09.csv
data/derived/family_prediction_comparability_summary_v09.csv
```

This gate checks whether the declared families have numeric prediction rows in
`family_prediction_tables_v08.csv`. It does not create new predictions. It only
separates two scoring modes:

- M0 adequacy diagnostics can be prepared from the existing M0 numeric rows.
- Full M0/M1/M2 family-comparison scoring remains blocked until M1 and M2 have
  numeric prediction rows or a later explicit ineligibility rule is frozen.

## Claim Boundary

This artifact writes no endpoint scores, runs no controls, compares no families,
and makes no dark-sector verdict. It prevents M1/M2 absence from being silently
converted into evidence for M0.
