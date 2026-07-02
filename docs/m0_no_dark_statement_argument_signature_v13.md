# M0 No-Dark Statement Argument Signature v13

**Doc class:** no-dark M0 statement argument-signature contract
**Status:** argument signature ready; constraint guards blocked; no formula; no scoring

Script:

```text
scripts/build_m0_no_dark_statement_argument_signature.py
```

Derived outputs:

```text
data/derived/m0_no_dark_statement_argument_signature_v13.csv
data/derived/m0_no_dark_statement_argument_signature_summary_v13.csv
```

This artifact records the allowed argument slots for the M0 no-dark statement
path. It binds term classes to source-side, baryonic, radial, readout, guard,
and assembly roles without writing an algebraic expression or executable
prediction function.

## Current Result

The expected status is:

```text
M0_NO_DARK_STATEMENT_ARGUMENT_SIGNATURE_READY_FOR_CONSTRAINT_GUARDS
```

The next missing artifact is:

```text
m0_no_dark_statement_constraint_guards_v13
```

## Claim Boundary

This argument-signature artifact does not define a velocity formula, does not
assign coefficients, does not compute predictions, does not score galaxies, and
does not decide the dark-sector question. It only freezes allowed argument
roles before constraint guards and dimensional checks are considered.
