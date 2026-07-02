# Family Prediction Tables v08

**Doc class:** prediction-table artifact
**Status:** M0 no-dark rows emitted; scoring blocked

Script:

```text
scripts/build_m0_no_dark_family_prediction_row_emission.py
```

Derived outputs:

```text
data/derived/family_prediction_tables_v08.csv
data/derived/family_prediction_tables_summary_v08.csv
```

This artifact closes the broad `family_prediction_tables_v08.csv` presence
blocker by writing the M0 no-dark family-prediction rows created from the
frozen source-side row values. It contains only the M0 no-dark prediction slot.

## Current Result

The expected status is:

```text
FAMILY_PREDICTION_TABLES_M0_NO_DARK_ROWS_EMITTED_SCORING_BLOCKED
```

The next required artifact is:

```text
m0_label_rule_table_v06
```

## Claim Boundary

This table contains M0 no-dark prediction rows only. It does not compute endpoint scores,
does not compare M0/M1/M2, does not validate the no-dark
model, and does not decide whether a dark-sector component is required.
