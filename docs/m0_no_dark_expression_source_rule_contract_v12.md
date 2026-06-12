# M0 No-Dark Expression Source Rule Contract v12

**Doc class:** no-dark M0 source-rule contract
**Status:** source-rule contract ready; derivation blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_expression_source_rule_contract.py
```

Derived outputs:

```text
data/derived/m0_no_dark_expression_source_rule_contract_v12.csv
data/derived/m0_no_dark_expression_source_rule_contract_summary_v12.csv
```

This contract expands the `m0_no_dark_expression_source_rule_v12` blocker into
the minimum source-rule slots required before a no-dark M0 expression can be
derived without endpoint residual leakage.

## Current Result

The expected status is:

```text
M0_NO_DARK_EXPRESSION_SOURCE_RULE_CONTRACT_READY_DERIVATION_BLOCKED
```

The source-rule contract exists, but zero source rules and zero numeric
prediction rows are written. The first concrete missing artifact is:

```text
m0_no_dark_expression_rule_derivation_v13
```

## Claim Boundary

This contract does not derive the M0 no-dark rule, does not define the
expression, does not compute predicted velocities, does not compare M0/M1/M2,
and does not make a dark-sector verdict. It only narrows the scoring frontier
from a missing source-side expression rule to the first missing derivation
record.
