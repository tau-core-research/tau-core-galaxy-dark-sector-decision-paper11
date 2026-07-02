# M0 No-Dark Expression Input Domain v12

**Doc class:** no-dark M0 expression input-domain binding record
**Status:** input-domain binding ready; coefficient freeze still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_expression_input_domain.py
```

Derived outputs:

```text
data/derived/m0_no_dark_expression_input_domain_v12.csv
data/derived/m0_no_dark_expression_input_domain_summary_v12.csv
```

This artifact binds the symbolic-form shell to allowed input domains. It records
the source-state, no-dark constraint, baryonic/source input, readout-operator,
failure-route, and form-assembly domains that later coefficient and dimensional
artifacts must respect.

## Current Result

The expected status is:

```text
M0_NO_DARK_EXPRESSION_INPUT_DOMAIN_READY
```

Six input-domain rows are ready:

- source-state domain;
- no-dark constraint domain;
- baryonic/source input domain;
- readout-operator domain;
- failure-route domain;
- form-assembly domain.

The next missing artifact is:

```text
m0_no_dark_expression_coefficient_freeze_v12
```

## Claim Boundary

This input-domain binding does not define a complete expression, does not write
a formula, does not assign coefficients, does not compute predicted velocities,
does not score galaxies, and does not decide the dark-sector question. It only
authorizes the next construction artifact: coefficient-freeze policy.
