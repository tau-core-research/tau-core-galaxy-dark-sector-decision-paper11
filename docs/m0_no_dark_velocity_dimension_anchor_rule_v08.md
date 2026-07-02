# M0 No-Dark Velocity-Dimension Anchor Rule v08

**Doc class:** velocity-dimension anchor gate
**Status:** dimension-anchor gate present; anchor source law missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_dimension_anchor_rule.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_dimension_anchor_rule_v08.csv
data/derived/m0_no_dark_velocity_dimension_anchor_rule_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_dimension_anchor_rule_v08`
presence blocker without declaring the anchor source law. It records that the
no-dark route still needs a source-independent rule for which physical source
may carry the velocity dimension before unit-free morphology/readout terms can
lawfully contribute to a `v_pred_km_s` formula.

## Current Result

The expected status is:

```text
M0_NO_DARK_DIMENSION_ANCHOR_PRESENT_BLOCKED_ANCHOR_SOURCE_LAW_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_anchor_source_law_v08
```

## Claim Boundary

This gate does not declare the anchor source law, does not choose a coupling
normalization, does not assign coefficients or scales, does not write a velocity
formula, does not write prediction rows, does not run endpoint scoring, and does
not decide the dark-sector question. It only narrows the scoring blocker to the
missing velocity-anchor source law.
