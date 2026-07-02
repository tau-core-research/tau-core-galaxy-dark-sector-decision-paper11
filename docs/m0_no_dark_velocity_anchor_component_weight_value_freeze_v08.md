# M0 No-Dark Velocity-Anchor Component Weight Value Freeze v08

**Doc class:** velocity-anchor component-weight value-freeze gate
**Status:** symbolic weight-value slots frozen; combined-anchor rule missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_anchor_component_weight_value_freeze.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_anchor_component_weight_value_freeze_v08.csv
data/derived/m0_no_dark_velocity_anchor_component_weight_value_freeze_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_anchor_component_weight_value_freeze_v08`
presence blocker by freezing the allowed symbolic slots for the source-side
component weights, signs, and normalization:

```text
w_gas;w_disk;w_bulge;s_gas;s_disk;s_bulge;n_anchor
```

The freeze is symbolic and pre-scoring. It writes no numeric weight values and
does not choose signs or normalization from observed velocities, endpoint
residuals, heldout scores, family winners, best-fit curves, or posthoc fit
quality.

The gate does not specify how the frozen symbolic slots are combined into an
anchor expression. That requires a later pre-scoring combined-anchor rule.

## Current Result

The expected status is:

```text
M0_NO_DARK_ANCHOR_COMPONENT_WEIGHT_VALUE_FREEZE_PRESENT_BLOCKED_COMBINED_ANCHOR_RULE_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_anchor_combined_anchor_rule_v08
```

## Claim Boundary

This gate freezes only symbolic source-side component-weight slots. It does not
write numeric weight values, does not compute combined anchor values, does not
write a velocity formula, does not write prediction rows, does not run endpoint
scoring, and does not decide whether a dark-sector component is required.
