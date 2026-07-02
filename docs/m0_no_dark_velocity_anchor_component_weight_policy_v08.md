# M0 No-Dark Velocity-Anchor Component Weight Policy v08

**Doc class:** velocity-anchor component-weight policy gate
**Status:** component-weight policy present; weight-value freeze missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_anchor_component_weight_policy.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_anchor_component_weight_policy_v08.csv
data/derived/m0_no_dark_velocity_anchor_component_weight_policy_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_anchor_component_weight_policy_v08`
presence blocker by declaring the admissible policy class for weights, signs,
and normalization on the frozen source-side components:

```text
v_gas_km_s;v_disk_km_s;v_bulge_km_s
```

The policy is deliberately non-numeric. It requires any later weights, signs,
or normalization to be fixed before scoring, dimensionless where they modify
velocity components, and independent of observed velocities, endpoint
residuals, heldout scores, family winners, best-fit curves, or posthoc fit
quality.

The gate does not freeze component-weight values, does not compute combined
anchor values, and does not produce a velocity formula. Those choices require a
later pre-scoring component-weight value-freeze artifact.

## Current Result

The expected status is:

```text
M0_NO_DARK_ANCHOR_COMPONENT_WEIGHT_POLICY_PRESENT_BLOCKED_WEIGHT_VALUE_FREEZE_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_anchor_component_weight_value_freeze_v08
```

## Claim Boundary

This gate declares only an admissible source-side component-weight policy
class. It does not freeze actual weight values, does not compute combined
anchor values, does not write a velocity formula, does not write prediction
rows, does not run endpoint scoring, and does not decide whether a dark-sector
component is required.
