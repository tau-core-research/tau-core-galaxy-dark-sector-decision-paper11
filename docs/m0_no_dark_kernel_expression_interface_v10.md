# M0 No-Dark Kernel Expression Interface v10

**Doc class:** no-dark M0 kernel-expression interface contract
**Status:** interface ready; frozen expression payload still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_kernel_expression_interface.py
```

Derived outputs:

```text
data/derived/m0_no_dark_kernel_expression_interface_v10.csv
data/derived/m0_no_dark_kernel_expression_interface_summary_v10.csv
```

This artifact closes the non-payload interface slots of the M0 no-dark kernel
expression: variable bindings, constant exposure, dimensional path, and
serialized-form handoff.

## Current Result

The expected status is:

```text
M0_NO_DARK_KERNEL_EXPRESSION_INTERFACE_READY
```

The next required artifact is:

```text
m0_no_dark_frozen_expression_payload_v11
```

## Claim Boundary

This interface does not write the frozen expression payload, does not define a
velocity formula, does not assign numeric coefficients, does not write
prediction rows, and does not allow endpoint scoring. It only narrows the
kernel-expression blocker to the missing frozen-expression payload.
