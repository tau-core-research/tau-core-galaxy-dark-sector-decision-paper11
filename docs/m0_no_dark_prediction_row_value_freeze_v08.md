# M0 No-Dark Prediction Row Value Freeze v08

**Doc class:** prediction-row value-freeze gate
**Status:** M0 no-dark row values frozen; family table row emission missing; no scoring

Script:

```text
scripts/build_m0_no_dark_prediction_row_value_freeze.py
```

Derived outputs:

```text
data/derived/m0_no_dark_prediction_row_value_freeze_v08.csv
data/derived/m0_no_dark_prediction_row_value_freeze_summary_v08.csv
```

This artifact closes the `m0_no_dark_prediction_row_value_freeze_v08` blocker
by freezing M0 no-dark numeric row values from the already frozen formula body:

```text
v_body_km_s(R) := v_anchor_km_s(R)
```

For each source-side anchor row, the frozen row value is:

```text
frozen_prediction_value_km_s := v_anchor_km_s
```

The artifact deliberately does not write rows into
`family_prediction_tables_v08.csv`. It freezes values for a later row-emission
gate only.

## Current Result

The expected status is:

```text
M0_NO_DARK_PREDICTION_ROW_VALUES_FROZEN_BLOCKED_FAMILY_ROW_EMISSION_MISSING
```

The next required artifact is:

```text
m0_no_dark_family_prediction_row_emission_v08
```

## Claim Boundary

This gate freezes M0 no-dark row values only. It does not write family
prediction table rows, does not compute endpoint scores, does not compare
M0/M1/M2, and does not decide whether a dark-sector component is required.
