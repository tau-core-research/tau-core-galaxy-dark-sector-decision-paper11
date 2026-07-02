# M0 No-Dark Velocity-Anchor Combined Anchor Value Freeze v08

**Doc class:** velocity-anchor combined-anchor value-freeze gate
**Status:** combined-anchor values frozen; velocity formula body missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_anchor_combined_anchor_value_freeze.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08.csv
data/derived/m0_no_dark_velocity_anchor_combined_anchor_value_freeze_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08`
presence blocker by evaluating the frozen source-side combined-anchor expression
on the imported SPARC baryonic velocity components:

```text
v_anchor_sq_km2_s2 = (s_gas*w_gas*v_gas_km_s^2 + s_disk*w_disk*v_disk_km_s^2 + s_bulge*w_bulge*v_bulge_km_s^2) / n_anchor
```

The value freeze uses the canonical no-dark identity carrier:

```text
s_gas = s_disk = s_bulge = +1
w_gas = w_disk = w_bulge = 1
n_anchor = 1
```

This gives:

```text
v_anchor_sq_km2_s2 = v_gas_km_s^2 + v_disk_km_s^2 + v_bulge_km_s^2
v_anchor_km_s = sqrt(v_anchor_sq_km2_s2)
```

These are frozen anchor values, not `v_pred_km_s` family-prediction rows. The
route does not use observed velocities, endpoint residuals, heldout scores,
family winners, best-fit curves, posthoc fit quality, or any score-derived
normalization.

## Current Result

The expected status is:

```text
M0_NO_DARK_ANCHOR_COMBINED_ANCHOR_VALUES_FROZEN_BLOCKED_VELOCITY_FORMULA_BODY_FREEZE_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_readout_formula_body_freeze_v08
```

## Claim Boundary

This gate freezes source-side combined-anchor values only. It does not write a
velocity formula, does not emit `v_pred_km_s` rows, does not run endpoint
scoring, and does not decide whether a dark-sector component is required.
