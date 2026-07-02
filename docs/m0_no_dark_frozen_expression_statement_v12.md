# M0 No-Dark Frozen Expression Statement v12

**Doc class:** no-dark M0 frozen-expression statement contract
**Status:** statement contract ready; no formula; no scoring

Script:

```text
scripts/build_m0_no_dark_frozen_expression_statement_contract.py
```

Derived outputs:

```text
data/derived/m0_no_dark_frozen_expression_statement_v12.csv
data/derived/m0_no_dark_frozen_expression_statement_summary_v12.csv
```

This artifact expands the first formula-bearing statement blocker into the
minimum acceptance slots required before a source-side no-dark expression can
be treated as frozen.

## Current Result

The expected status is:

```text
M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_FOR_PAYLOAD
```

The first concrete missing artifact is:

```text
m0_no_dark_frozen_expression_payload_v11
```

## Claim Boundary

This contract does not define a velocity formula, does not assign coefficients,
does not compute predictions, does not score galaxies, and does not decide the
dark-sector question. It only tracks the statement-side slots required before
the payload can be accepted.
