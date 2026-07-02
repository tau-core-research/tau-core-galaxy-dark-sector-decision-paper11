# M0 No-Dark Formula Body Contract v07

**Doc class:** no-dark M0 formula-body contract
**Status:** body contract ready; readout equation blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_formula_body_contract.py
```

Derived outputs:

```text
data/derived/m0_no_dark_formula_body_contract_v07.csv
data/derived/m0_no_dark_formula_body_contract_summary_v07.csv
```

This contract expands the `m0_no_dark_formula_body_v07` blocker into the
minimum formula-body slots required before the no-dark M0 table can be
considered formula-ready.

## Current Result

The expected status is:

```text
M0_NO_DARK_FORMULA_BODY_CONTRACT_READY_EQUATION_BLOCKED
```

The formula-body contract exists, but zero formula equations and zero numeric
prediction rows are written. The first concrete missing artifact is:

```text
m0_no_dark_source_side_expression_statement_v13
```

## Claim Boundary

This contract does not provide the M0 readout equation, does not compute
predicted velocities, does not compare M0/M1/M2, and does not make a
dark-sector verdict. It only narrows the scoring frontier from a missing
formula-body artifact through the v08 readout-equation contract and v09 kernel
contract to the first missing parent-assumption basis for the no-dark rule
derivation.
