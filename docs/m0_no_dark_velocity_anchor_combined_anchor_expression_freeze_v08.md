# M0 No-Dark Velocity-Anchor Combined Anchor Expression Freeze v08

**Doc class:** velocity-anchor combined-anchor expression-freeze gate
**Status:** exact symbolic expression frozen; combined-anchor values missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_anchor_combined_anchor_expression_freeze.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08.csv
data/derived/m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08`
presence blocker by freezing the exact symbolic expression used for the
source-side M0 no-dark velocity anchor:

```text
v_anchor_sq_km2_s2 =
    (s_gas*w_gas*v_gas_km_s^2
   + s_disk*w_disk*v_disk_km_s^2
   + s_bulge*w_bulge*v_bulge_km_s^2) / n_anchor
```

The expression is a velocity-squared baryonic carrier. It combines only the
frozen SPARC source-side velocity components:

```text
v_gas_km_s;v_disk_km_s;v_bulge_km_s
```

with the frozen symbolic slots:

```text
w_gas;w_disk;w_bulge;s_gas;s_disk;s_bulge;n_anchor
```

The weight, sign, and normalization slots remain pre-scoring symbolic slots.
No observed velocity, endpoint residual, heldout score, family winner,
best-fit curve, posthoc fit quality, or numeric prediction value is allowed in
the expression-freeze route.

## Current Result

The expected status is:

```text
M0_NO_DARK_ANCHOR_COMBINED_ANCHOR_EXPRESSION_FROZEN_BLOCKED_VALUE_FREEZE_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08
```

## Claim Boundary

This gate freezes only the exact symbolic combined-anchor expression. It does not evaluate combined-anchor values, does not choose numeric weights or signs, does not write a velocity formula, does not write prediction rows, does not run endpoint scoring, and does not decide whether a dark-sector component is required.
