# M0 No-Dark Velocity Readout Formula v08

**Doc class:** velocity-readout formula gate
**Status:** formula gate present; equation body missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_readout_formula.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_readout_formula_v08.csv
data/derived/m0_no_dark_velocity_readout_formula_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_readout_formula_v08` presence
blocker without writing a velocity formula. It records that the ready formula
body, dimensional-audit, and machine-form contracts still need a concrete
source-to-rotation equation body before `v_pred_km_s` rows can be emitted.

## Current Result

The expected status is:

```text
M0_NO_DARK_VELOCITY_FORMULA_PRESENT_BLOCKED_EQUATION_BODY_MISSING
```

The next required artifact is:

```text
m0_no_dark_source_to_rotation_equation_body_v08
```

## Claim Boundary

This gate does not define the equation body, does not assign coefficients,
does not write prediction rows, does not run endpoint scoring, and does not
decide the dark-sector question. It only narrows the scoring blocker from a
missing velocity formula to the missing source-to-rotation equation body.
