# M0 No-Dark Expression Null/Fallback Policy v13

**Doc class:** no-dark M0 expression null/fallback policy record
**Status:** null/fallback policy ready; output class still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_expression_null_fallback_policy.py
```

Derived outputs:

```text
data/derived/m0_no_dark_expression_null_fallback_policy_v13.csv
data/derived/m0_no_dark_expression_null_fallback_policy_summary_v13.csv
```

This artifact records how null, gauge, missing-input, incomparability, and
failure-route cases are handled before any no-dark M0 source rule is written.
It blocks endpoint-selected repairs and post-hoc exceptions.

## Current Result

The expected status is:

```text
M0_NO_DARK_EXPRESSION_NULL_FALLBACK_POLICY_READY
```

Six null/fallback rows are ready:

- source-domain null policy;
- no-dark constraint violation policy;
- morphology/readout label policy;
- finite-local `U_read` incomparability policy;
- baryonic/source binding null policy;
- failure-route domination policy.

The next missing artifact is:

```text
m0_no_dark_expression_output_class_v13
```

## Claim Boundary

This null/fallback record does not define the M0 no-dark source rule, does not
define an expression, does not write a formula, does not compute predicted
velocities, does not score galaxies, and does not decide the dark-sector
question. It only authorizes the next source-side construction artifact: the
output class.
