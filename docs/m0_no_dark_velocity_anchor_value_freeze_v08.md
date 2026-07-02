# M0 No-Dark Velocity-Anchor Value Freeze v08

**Doc class:** velocity-anchor value-freeze gate
**Status:** source-value columns frozen; unit normalization missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_anchor_value_freeze.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_anchor_value_freeze_v08.csv
data/derived/m0_no_dark_velocity_anchor_value_freeze_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_anchor_value_freeze_v08`
presence blocker by freezing the source-side value columns allowed for the M0
no-dark velocity anchor. The frozen source is the SPARC
`MassModels_Lelli2016c.mrt` baryonic velocity-component lane:

```text
v_gas_km_s;v_disk_km_s;v_bulge_km_s
```

The gate does not read or use `v_obs_km_s`, endpoint residuals, heldout scores,
family winners, best-fit curves, posthoc rescaling, or fitted coefficient
quality. It does not combine the frozen source columns into a formula. It only
freezes the source columns and per-galaxy source-row coverage before any later
unit-normalization or velocity-formula step.

## Current Result

The expected status is:

```text
M0_NO_DARK_ANCHOR_VALUE_FREEZE_PRESENT_BLOCKED_UNIT_NORMALIZATION_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_anchor_unit_normalization_v08
```

## Claim Boundary

This gate freezes only source-side anchor value columns and provenance coverage. It does not compute a combined anchor value, does not normalize units into a formula-ready carrier, does not assign coupling normalization, does not write a velocity formula, does not write prediction rows, does not run endpoint scoring, and does not decide whether a dark-sector component is required.
