# M0 No-Dark Velocity-Anchor Combined Anchor Rule v08

**Doc class:** velocity-anchor combined-anchor rule gate
**Status:** combined-anchor rule class present; expression freeze missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_anchor_combined_anchor_rule.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_anchor_combined_anchor_rule_v08.csv
data/derived/m0_no_dark_velocity_anchor_combined_anchor_rule_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_anchor_combined_anchor_rule_v08`
presence blocker by declaring the admissible symbolic rule class for combining
the frozen source-side velocity components with the frozen symbolic slots:

```text
v_gas_km_s;v_disk_km_s;v_bulge_km_s
w_gas;w_disk;w_bulge;s_gas;s_disk;s_bulge;n_anchor
```

The rule is structural and pre-scoring. It permits only source-side symbolic
binding, preserves velocity dimension, and forbids endpoint feedback from
observed velocities, residuals, heldout scores, family winners, best-fit
curves, or posthoc fit quality.

The gate does not freeze the exact symbolic expression, evaluate combined
anchor values, or write a velocity formula. Those choices require a later
combined-anchor expression-freeze artifact.

## Current Result

The expected status is:

```text
M0_NO_DARK_ANCHOR_COMBINED_ANCHOR_RULE_PRESENT_BLOCKED_EXPRESSION_FREEZE_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08
```

## Claim Boundary

This gate declares only the admissible source-side symbolic combined-anchor
rule class. It does not freeze the exact expression, does not compute combined
anchor values, does not write a velocity formula, does not write prediction
rows, does not run endpoint scoring, and does not decide whether a dark-sector
component is required.
