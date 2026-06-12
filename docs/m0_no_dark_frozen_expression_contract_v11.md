# M0 No-Dark Frozen Expression Contract v11

**Doc class:** no-dark M0 frozen-expression contract
**Status:** frozen-expression contract ready; source rule blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_frozen_expression_contract.py
```

Derived outputs:

```text
data/derived/m0_no_dark_frozen_expression_contract_v11.csv
data/derived/m0_no_dark_frozen_expression_contract_summary_v11.csv
```

This contract expands the `m0_no_dark_frozen_expression_v11` blocker into the
minimum freeze slots required before any no-dark M0 expression can become a
source-side, dimensionally auditable, machine-readable prediction input.

## Current Result

The expected status is:

```text
M0_NO_DARK_FROZEN_EXPRESSION_CONTRACT_READY_SOURCE_RULE_BLOCKED
```

The frozen-expression contract exists, but zero frozen expressions and zero
numeric prediction rows are written. The first concrete missing artifact is:

```text
m0_no_dark_rule_parent_assumption_basis_v14
```

## Claim Boundary

This contract does not define the M0 no-dark expression, does not compute
predicted velocities, does not compare M0/M1/M2, and does not make a
dark-sector verdict. It only narrows the scoring frontier from a missing frozen
expression through the v12 source-rule contract to the first missing
parent-assumption basis for the no-dark rule derivation.
