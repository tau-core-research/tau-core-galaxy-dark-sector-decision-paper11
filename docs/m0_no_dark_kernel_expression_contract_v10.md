# M0 No-Dark Kernel Expression Contract v10

**Doc class:** no-dark M0 kernel-expression contract
**Status:** expression contract ready; frozen expression blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_kernel_expression_contract.py
```

Derived outputs:

```text
data/derived/m0_no_dark_kernel_expression_contract_v10.csv
data/derived/m0_no_dark_kernel_expression_contract_summary_v10.csv
```

This contract expands the `m0_no_dark_kernel_expression_v10` blocker into the
minimum expression slots required before the no-dark M0 kernel can become a
frozen, dimensionally auditable, machine-readable expression.

## Current Result

The expected status is:

```text
M0_NO_DARK_KERNEL_EXPRESSION_CONTRACT_READY_FROZEN_EXPRESSION_BLOCKED
```

The kernel-expression contract exists, but zero frozen expressions and zero
numeric prediction rows are written. The first concrete missing artifact is:

```text
m0_no_dark_frozen_expression_v11
```

## Claim Boundary

This contract does not define the M0 no-dark expression, does not compute
predicted velocities, does not compare M0/M1/M2, and does not make a
dark-sector verdict. It only narrows the scoring frontier from a missing kernel
expression to the first missing frozen no-dark expression.
