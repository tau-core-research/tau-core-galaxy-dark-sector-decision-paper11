# M0 No-Dark Expression Source Basis v13

**Doc class:** no-dark M0 expression source-basis record
**Status:** source basis ready; admissibility rule still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_expression_source_basis.py
```

Derived outputs:

```text
data/derived/m0_no_dark_expression_source_basis_v13.csv
data/derived/m0_no_dark_expression_source_basis_summary_v13.csv
```

This artifact records the typed source-side basis elements that may be handed to
a later no-dark M0 source-rule construction. It does not choose coefficients,
write an expression, compute velocities, or score any galaxy.

## Current Result

The expected status is:

```text
M0_NO_DARK_EXPRESSION_SOURCE_BASIS_READY
```

Six source-basis rows are ready:

- frozen source-domain basis;
- dimensionless no-dark family constraint;
- morphology/readout source factor;
- dimensionless finite-local `U_read` admissibility marker;
- unit-preserving baryonic/source binding;
- blocked failure-route marker.

The next missing artifact is:

```text
m0_no_dark_expression_admissibility_rule_v13
```

## Claim Boundary

This source-basis record does not define the M0 no-dark source rule, does not
define an expression, does not write a formula, does not compute predicted
velocities, does not score galaxies, and does not decide the dark-sector
question. It only authorizes the next source-side construction artifact: the
admissibility rule.
