# M0 No-Dark Rule Dimensional Precheck v14

**Doc class:** no-dark M0 source-side dimensional precheck
**Status:** dimensional precheck ready; derivation provenance/leakage audit still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_rule_dimensional_precheck.py
```

Derived outputs:

```text
data/derived/m0_no_dark_rule_dimensional_precheck_v14.csv
data/derived/m0_no_dark_rule_dimensional_precheck_summary_v14.csv
```

This artifact records a pre-expression dimensional route for the M0 no-dark
rule family. It checks that the already generated term/check classes can be
handed to a later source-rule derivation without silently introducing dark
response terms, fitted unit rescalings, endpoint residuals, or velocity
predictions.

## Current Result

The expected status is:

```text
M0_NO_DARK_RULE_DIMENSIONAL_PRECHECK_READY
```

Six precheck rows are ready:

- typed input-domain route;
- dimensionless M0 no-dark exclusion route;
- morphology/readout source-factor route;
- dimensionless finite-local `U_read` admissibility route;
- unit-preserving baryonic/source binding route;
- dimension-safe blocked failure route.

The next missing artifact is:

```text
m0_no_dark_rule_derivation_provenance_leakage_v14
```

## Claim Boundary

This precheck does not define the M0 no-dark expression, does not specify
coefficients, does not compute predicted velocities, does not score galaxies,
and does not decide the dark-sector question. It only authorizes the next
source-side artifact: a derivation provenance and leakage audit.
