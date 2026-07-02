# M0 No-Dark Statement Constraint Guards v13

**Doc class:** no-dark M0 statement constraint-guard contract
**Status:** constraint guards ready; pre-dimensional proof blocked; no formula; no scoring

Script:

```text
scripts/build_m0_no_dark_statement_constraint_guards.py
```

Derived outputs:

```text
data/derived/m0_no_dark_statement_constraint_guards_v13.csv
data/derived/m0_no_dark_statement_constraint_guards_summary_v13.csv
```

This artifact records the domain, null, gauge/readout, no-dark, fallback, and
leakage/freeze guards required before any formula body can be considered.

## Current Result

The expected status is:

```text
M0_NO_DARK_STATEMENT_CONSTRAINT_GUARDS_READY_FOR_PRE_DIMENSIONAL_PROOF
```

The next missing artifact is:

```text
m0_no_dark_statement_pre_dimensional_proof_v13
```

## Claim Boundary

This guard artifact does not define a velocity formula, does not assign
coefficients, does not compute predictions, does not score galaxies, and does
not decide the dark-sector question. It only freezes admissible guard policy
before dimensional proof and formula-body work.
