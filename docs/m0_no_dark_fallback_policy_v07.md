# M0 No-Dark Fallback Policy v07

**Doc class:** no-dark M0 formula-table fallback policy
**Status:** fallback policy ready; no fallback prediction rows; no numeric predictions; no scoring

Script:

```text
scripts/build_m0_no_dark_fallback_policy.py
```

Derived outputs:

```text
data/derived/m0_no_dark_fallback_policy_v07.csv
data/derived/m0_no_dark_fallback_policy_summary_v07.csv
```

This artifact fills the fallback-policy slot of the M0 no-dark formula table.
It imports the fixed-scale discipline from `m0_no_dark_scale_policy_v07` and
projects it to zero-response, missing-label, inadmissible-input, null/gauge,
failure-reporting, and prediction-table handoff routes.

## Current Result

The expected status is:

```text
M0_NO_DARK_FALLBACK_POLICY_READY
```

The policy is scoring-safe:

```text
fallback route != fitted rescue
failure state != dropped hard row
null/gauge route != empirical success
```

It forbids hidden exception terms, post-hoc label switches, residual-specific
null rescues, and silent row/radius drops. Fallback states may only be carried
forward as explicit readiness metadata until a later executable prediction
artifact authorizes numeric prediction rows.

The next formula-table handoff is:

```text
family_prediction_tables_v08.csv
```

## Claim Boundary

This policy does not write fallback velocity predictions, compute velocities,
compare M0/M1/M2, activate endpoint scoring, or decide the dark-sector
question. It only closes the fallback-policy slot of the M0 no-dark formula
table.
