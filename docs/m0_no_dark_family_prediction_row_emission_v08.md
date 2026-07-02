# M0 No-Dark Family Prediction Row Emission v08

**Doc class:** family-prediction row emission gate
**Status:** M0 no-dark rows emitted; scoring blocked

Script:

```text
scripts/build_m0_no_dark_family_prediction_row_emission.py
```

Derived outputs:

```text
data/derived/m0_no_dark_family_prediction_row_emission_v08.csv
data/derived/m0_no_dark_family_prediction_row_emission_summary_v08.csv
data/derived/family_prediction_tables_v08.csv
data/derived/family_prediction_tables_summary_v08.csv
```

This artifact materializes the frozen M0 no-dark row values into the family
prediction table shape. It writes `v_pred_km_s` rows for the M0 no-dark
readout slot only.

## Current Result

The expected status is:

```text
M0_NO_DARK_FAMILY_PREDICTION_ROWS_EMITTED_SCORING_BLOCKED
```

The next required artifact is:

```text
m0_label_rule_table_v06
```

## Claim Boundary

This gate writes M0 no-dark family-prediction rows only. It does not compute endpoint scores,
does not compare M0/M1/M2, does not validate the no-dark
model, and does not decide whether a dark-sector component is required.
