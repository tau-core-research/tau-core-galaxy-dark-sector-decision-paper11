# M0 No-Dark Readout Equation Contract v08

**Doc class:** no-dark M0 readout-equation contract
**Status:** equation contract ready; kernel blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_readout_equation_contract.py
```

Derived outputs:

```text
data/derived/m0_no_dark_readout_equation_contract_v08.csv
data/derived/m0_no_dark_readout_equation_contract_summary_v08.csv
```

This contract expands the `m0_no_dark_readout_equation_v08` blocker into the
minimum equation slots required before the no-dark M0 readout can become a
formula-bearing object.

## Current Result

The expected status is:

```text
M0_NO_DARK_READOUT_EQUATION_CONTRACT_READY_KERNEL_BLOCKED
```

The readout-equation contract exists, but zero equations and zero numeric
prediction rows are written. The first concrete missing artifact is:

```text
m0_no_dark_kernel_expression_v10
```

## Claim Boundary

This contract does not define the M0 equation kernel, does not compute
predicted velocities, does not compare M0/M1/M2, and does not make a
dark-sector verdict. It only narrows the scoring frontier from a missing
readout-equation artifact through the v09 kernel contract to the first missing
no-dark kernel expression.
