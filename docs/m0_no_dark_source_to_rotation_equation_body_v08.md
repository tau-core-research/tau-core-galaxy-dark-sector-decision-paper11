# M0 No-Dark Source-to-Rotation Equation Body v08

**Doc class:** source-to-rotation equation-body gate
**Status:** equation-body gate present; coupling rule missing; no predictions

Script:

```text
scripts/build_m0_no_dark_source_to_rotation_equation_body.py
```

Derived outputs:

```text
data/derived/m0_no_dark_source_to_rotation_equation_body_v08.csv
data/derived/m0_no_dark_source_to_rotation_equation_body_summary_v08.csv
```

This artifact closes the `m0_no_dark_source_to_rotation_equation_body_v08`
presence blocker without writing the equation body. It records that the M0
no-dark path still needs an explicit source-to-velocity coupling rule before
source/morphology/readout markers can lawfully enter a velocity-dimensional
formula.

## Current Result

The expected status is:

```text
M0_NO_DARK_EQUATION_BODY_PRESENT_BLOCKED_SOURCE_TO_VELOCITY_COUPLING_RULE_MISSING
```

The next required artifact is:

```text
m0_no_dark_source_to_velocity_coupling_rule_v08
```

## Claim Boundary

This gate does not define the equation body, does not choose a coupling law,
does not assign coefficients or scales, does not write prediction rows, does
not run endpoint scoring, and does not decide the dark-sector question. It only
narrows the scoring blocker to the missing source-to-velocity coupling rule.
