# M0 No-Dark Coefficient Policy v07

**Doc class:** no-dark M0 formula-table coefficient policy
**Status:** coefficient policy ready; no numeric values; no predictions; no scoring

Script:

```text
scripts/build_m0_no_dark_coefficient_policy.py
```

Derived outputs:

```text
data/derived/m0_no_dark_coefficient_policy_v07.csv
data/derived/m0_no_dark_coefficient_policy_summary_v07.csv
```

This artifact fills the first concrete formula-table policy blocker identified
by the v81/v82 scoring frontier. It imports the expression-side coefficient
freeze discipline from `m0_no_dark_expression_coefficient_freeze_v12` and
projects it to the M0 formula-table level.

## Current Result

The expected status is:

```text
M0_NO_DARK_COEFFICIENT_POLICY_READY
```

The policy is shape-aware after the Paper 10 update:

```text
level/amplitude support != shape/readout support
```

It forbids hidden dark-sector compensation inside M0 and requires any future
adjustable coefficient, scale, switch, threshold, or per-galaxy privilege to be
declared and counted before endpoint scoring.

The next formula-table policy blocker is:

```text
m0_no_dark_scale_policy_v07
```

## Claim Boundary

This policy does not assign numeric coefficient values, write prediction rows,
compute velocities, compare M0/M1/M2, or decide the dark-sector question. It
only closes the coefficient-policy slot of the M0 no-dark formula table.
