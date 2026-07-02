# M0 No-Dark Scale Policy v07

**Doc class:** no-dark M0 formula-table scale policy
**Status:** scale policy ready; no numeric scale values; no predictions; no scoring

Script:

```text
scripts/build_m0_no_dark_scale_policy.py
```

Derived outputs:

```text
data/derived/m0_no_dark_scale_policy_v07.csv
data/derived/m0_no_dark_scale_policy_summary_v07.csv
```

This artifact fills the fixed-scale policy slot of the M0 no-dark formula
table. It imports the coefficient-policy discipline from
`m0_no_dark_coefficient_policy_v07` and projects it to scale use: radial-domain
scope, normalization scales, transition scales, known-limit behavior, row-level
scale reuse, and fallback handoff.

## Current Result

The expected status is:

```text
M0_NO_DARK_SCALE_POLICY_READY
```

The policy is shape-aware after the Paper 10 update:

```text
scale choice != residual-window rescue
level/amplitude support != shape/readout support
```

It forbids post-hoc radial windows, hidden normalization scales, private
per-galaxy rescue scales, and endpoint-selected transition radii. Any later
adjustable scale, threshold, radial window, transition rule, or private row
privilege must be declared and counted before endpoint scoring.

The next formula-table policy blocker is:

```text
m0_no_dark_fallback_policy_v07
```

## Claim Boundary

This policy does not assign numeric scale values, write prediction rows,
compute velocities, compare M0/M1/M2, or decide the dark-sector question. It
only closes the fixed-scale policy slot of the M0 no-dark formula table.
