# M0 No-Dark Velocity-Anchor Component Combination Rule v08

**Doc class:** velocity-anchor component-combination rule gate
**Status:** component-combination rule class present; component-weight policy missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_anchor_component_combination_rule.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_anchor_component_combination_rule_v08.csv
data/derived/m0_no_dark_velocity_anchor_component_combination_rule_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_anchor_component_combination_rule_v08`
presence blocker by declaring the allowed source-side combination-rule layer for
the frozen velocity-anchor components:

```text
v_gas_km_s;v_disk_km_s;v_bulge_km_s
```

The rule is deliberately structural. It says the later no-dark anchor may only
combine frozen source-side velocity components, must preserve velocity
dimension, and must not choose its operation from observed velocity, endpoint
residuals, heldout scores, family winners, best-fit curves, or posthoc
component choices.

The gate does not choose component weights, signs, normalization, a combined
anchor value, or a velocity formula. Those choices require a later pre-scoring
component-weight policy.

## Current Result

The expected status is:

```text
M0_NO_DARK_ANCHOR_COMPONENT_COMBINATION_RULE_PRESENT_BLOCKED_COMPONENT_WEIGHT_POLICY_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_anchor_component_weight_policy_v08
```

## Claim Boundary

This gate declares only a source-side structural component-combination rule
class. It does not set weights, signs, or normalization, does not compute
combined anchor values, does not write a velocity formula, does not write
prediction rows, does not run endpoint scoring, and does not decide whether a
dark-sector component is required.
