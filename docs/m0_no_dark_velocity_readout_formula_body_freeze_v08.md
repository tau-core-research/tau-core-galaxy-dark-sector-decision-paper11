# M0 No-Dark Velocity Readout Formula Body Freeze v08

**Doc class:** velocity-readout formula body-freeze gate
**Status:** formula body frozen; prediction row values missing; no scoring

Script:

```text
scripts/build_m0_no_dark_velocity_readout_formula_body_freeze.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_readout_formula_body_freeze_v08.csv
data/derived/m0_no_dark_velocity_readout_formula_body_freeze_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_readout_formula_body_freeze_v08`
presence blocker by freezing the M0 no-dark velocity readout formula body:

```text
v_body_km_s(R) := v_anchor_km_s(R)
```

The formula body uses the frozen source-side baryonic anchor values from:

```text
data/derived/m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08.csv
```

It adds no dark-sector response term, no residual-selected correction, and no
posthoc rescaling. It is a formula-body freeze only: it does not emit
`v_pred_km_s` rows and does not activate endpoint scoring.

## Current Result

The expected status is:

```text
M0_NO_DARK_VELOCITY_FORMULA_BODY_FROZEN_BLOCKED_PREDICTION_ROW_VALUE_FREEZE_MISSING
```

The next required artifact is:

```text
m0_no_dark_prediction_row_value_freeze_v08
```

## Claim Boundary

This gate freezes the source-side no-dark velocity formula body only. It does
not write family prediction rows, does not compute scores, does not compare
M0/M1/M2, and does not decide whether a dark-sector component is required.
