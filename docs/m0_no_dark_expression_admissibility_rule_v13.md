# M0 No-Dark Expression Admissibility Rule v13

**Doc class:** no-dark M0 expression admissibility-rule record
**Status:** admissibility rule ready; null/fallback policy still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_expression_admissibility_rule.py
```

Derived outputs:

```text
data/derived/m0_no_dark_expression_admissibility_rule_v13.csv
data/derived/m0_no_dark_expression_admissibility_rule_summary_v13.csv
```

This artifact records which source-basis elements may pass into later no-dark
M0 source-rule construction. It is a source-side admissibility gate, not a
formula, fit, prediction, or endpoint score.

## Current Result

The expected status is:

```text
M0_NO_DARK_EXPRESSION_ADMISSIBILITY_RULE_READY
```

Six admissibility rows are ready:

- frozen source-domain admissibility;
- dimensionless no-dark constraint admissibility;
- morphology/readout factor admissibility;
- finite-local `U_read` marker admissibility;
- unit-preserving baryonic/source binding admissibility;
- blocked failure-route admissibility.

The next missing artifact is:

```text
m0_no_dark_expression_null_fallback_policy_v13
```

## Claim Boundary

This admissibility record does not define the M0 no-dark source rule, does not
define an expression, does not write a formula, does not compute predicted
velocities, does not score galaxies, and does not decide the dark-sector
question. It only authorizes the next source-side construction artifact: the
null/fallback policy.
