# M0 No-Dark Equation Kernel Contract v09

**Doc class:** no-dark M0 equation-kernel contract
**Status:** kernel contract ready; expression blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_equation_kernel_contract.py
```

Derived outputs:

```text
data/derived/m0_no_dark_equation_kernel_contract_v09.csv
data/derived/m0_no_dark_equation_kernel_contract_summary_v09.csv
```

This contract expands the `m0_no_dark_equation_kernel_v09` blocker into the
minimum kernel slots required before the no-dark M0 readout can become an
equation-bearing object.

## Current Result

The expected status is:

```text
M0_NO_DARK_EQUATION_KERNEL_CONTRACT_READY_EXPRESSION_BLOCKED
```

The equation-kernel contract exists, but zero kernel expressions and zero
numeric prediction rows are written. The first concrete missing artifact is:

```text
m0_no_dark_expression_source_rule_v12
```

## Claim Boundary

This contract does not define the M0 kernel expression, does not compute
predicted velocities, does not compare M0/M1/M2, and does not make a
dark-sector verdict. It only narrows the scoring frontier from a missing
equation-kernel artifact through the v10 kernel-expression contract to the
first missing source-side expression rule.
