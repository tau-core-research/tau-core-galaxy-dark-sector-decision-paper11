# M0 No-Dark Formula Table Contract v06

**Doc class:** no-dark M0 formula-table contract
**Status:** contract ready; formula body blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_formula_table_contract.py
```

Derived outputs:

```text
data/derived/m0_no_dark_formula_table_contract_v06.csv
data/derived/m0_no_dark_formula_table_contract_summary_v06.csv
```

This contract is the first concrete expansion of the
`m0_no_dark_formula_table_v06` blocker. It defines the minimum table
components that a no-dark Tau morphology/readout formula must fill before M0
prediction rows can be written.

## Current Result

The expected status is:

```text
M0_NO_DARK_FORMULA_TABLE_CONTRACT_READY_BODY_BLOCKED
```

The table contract exists, but zero formula-body rows and zero numeric
prediction rows are written. The next concrete missing artifact is:

```text
m0_no_dark_kernel_expression_v10
```

## Claim Boundary

This contract does not define the no-dark Tau formula, does not compute
predicted velocities, does not compare M0/M1/M2, and does not make a
dark-sector verdict. It only narrows the scoring frontier from a missing M0
formula-table artifact through the v07 body contract to the first missing
no-dark readout equation and its frozen policies.
