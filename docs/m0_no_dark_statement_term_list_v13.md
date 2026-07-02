# M0 No-Dark Statement Term List v13

**Doc class:** no-dark M0 statement term-list contract
**Status:** term classes ready; argument signature blocked; no formula; no scoring

Script:

```text
scripts/build_m0_no_dark_statement_term_list.py
```

Derived outputs:

```text
data/derived/m0_no_dark_statement_term_list_v13.csv
data/derived/m0_no_dark_statement_term_list_summary_v13.csv
```

This artifact records the allowed term classes for the M0 no-dark source-side
statement path. It does not assemble these terms into a mathematical
expression. It does not bind concrete arguments, choose coefficients, compute
predictions, or score endpoint residuals.

## Current Result

The expected status is:

```text
M0_NO_DARK_STATEMENT_TERM_LIST_READY_FOR_ARGUMENT_SIGNATURE
```

The next missing artifact is:

```text
m0_no_dark_statement_argument_signature_v13
```

## Claim Boundary

This term-list artifact allows only term classes: source-state, baryonic input,
readout-operator, no-dark constraint, null/fallback, and assembly-operator
slots. It does not define a velocity formula and does not decide the
dark-sector question.
