# M0 No-Dark Velocity-Anchor Unit Normalization v08

**Doc class:** velocity-anchor unit-normalization gate
**Status:** unit normalization present; component-combination rule missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_anchor_unit_normalization.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_anchor_unit_normalization_v08.csv
data/derived/m0_no_dark_velocity_anchor_unit_normalization_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_anchor_unit_normalization_v08`
presence blocker by declaring that the frozen SPARC source columns
`v_gas_km_s`, `v_disk_km_s`, and `v_bulge_km_s` are already source-side
velocity components in `km/s`. No posthoc unit rescale is introduced.

The gate does not combine components, does not square components, does not
choose signs or weights, and does not produce a velocity formula. It only
normalizes the source-unit layer before a later component-combination rule.

## Current Result

The expected status is:

```text
M0_NO_DARK_ANCHOR_UNIT_NORMALIZATION_PRESENT_BLOCKED_COMPONENT_COMBINATION_RULE_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_anchor_component_combination_rule_v08
```

## Claim Boundary

This gate declares only source-unit normalization. It does not combine source components, does not compute an anchor value, does not assign coupling normalization, does not write a velocity formula, does not write prediction rows, does not run endpoint scoring, and does not decide whether a dark-sector component is required.
