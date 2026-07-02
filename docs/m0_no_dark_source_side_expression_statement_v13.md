# M0 No-Dark Source-Side Expression Statement v13

**Doc class:** no-dark M0 source-side expression statement envelope
**Status:** statement envelope ready; term list blocked; no formula; no scoring

Script:

```text
scripts/build_m0_no_dark_source_side_expression_statement.py
```

Derived outputs:

```text
data/derived/m0_no_dark_source_side_expression_statement_v13.csv
data/derived/m0_no_dark_source_side_expression_statement_summary_v13.csv
```

This artifact writes the source-side statement envelope required by the v12
frozen-expression statement contract. It does not write the mathematical
expression body. It fixes the allowed pre-score role of the statement, its
source-side scope, M0 no-dark family binding, output intent, freeze guard, and
handoff to the concrete term-list artifact.

## Current Result

The expected status is:

```text
M0_NO_DARK_SOURCE_SIDE_EXPRESSION_STATEMENT_READY_FOR_TERM_LIST
```

The next missing artifact is:

```text
m0_no_dark_statement_term_list_v13
```

## Claim Boundary

This source-side statement envelope does not define a velocity formula, does
not list admissible terms, does not bind arguments, does not assign
coefficients, does not compute predictions, does not score galaxies, and does
not decide the dark-sector question. It only authorizes the next formula-side
construction artifact: the frozen term list.
