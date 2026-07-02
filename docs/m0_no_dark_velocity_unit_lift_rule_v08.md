# M0 No-Dark Velocity-Unit Lift Rule v08

**Doc class:** velocity-unit lift gate
**Status:** unit-lift gate present; dimension anchor missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_unit_lift_rule.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_unit_lift_rule_v08.csv
data/derived/m0_no_dark_velocity_unit_lift_rule_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_unit_lift_rule_v08` presence
blocker without declaring a velocity-producing unit lift. It records that the
no-dark route still needs a source-independent velocity-dimension anchor before
unit-free morphology/readout source variables can lawfully contribute to a
`v_pred_km_s` formula.

## Current Result

The expected status is:

```text
M0_NO_DARK_VELOCITY_UNIT_LIFT_PRESENT_BLOCKED_DIMENSION_ANCHOR_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_dimension_anchor_rule_v08
```

## Claim Boundary

This gate does not declare a dimension anchor, does not choose a coupling
normalization, does not assign coefficients or scales, does not write a velocity
formula, does not write prediction rows, does not run endpoint scoring, and does
not decide the dark-sector question. It only narrows the scoring blocker to the
missing velocity-dimension anchor rule.
