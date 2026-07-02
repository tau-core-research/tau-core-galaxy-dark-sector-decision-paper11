# M0 No-Dark Equation Kernel Interface v09

**Doc class:** no-dark M0 equation-kernel interface contract
**Status:** interface ready; kernel expression still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_equation_kernel_interface.py
```

Derived outputs:

```text
data/derived/m0_no_dark_equation_kernel_interface_v09.csv
data/derived/m0_no_dark_equation_kernel_interface_summary_v09.csv
```

This artifact closes the non-expression interface slots of the M0 no-dark
equation kernel: input binding, output mapping, parameter audit, failure
policy, and reproducible-hook handoff.

## Current Result

The expected status is:

```text
M0_NO_DARK_EQUATION_KERNEL_INTERFACE_READY
```

The next required artifact is:

```text
m0_no_dark_kernel_expression_v10
```

## Claim Boundary

This interface does not write the kernel expression, does not define a velocity
formula, does not assign numeric coefficients, does not write prediction rows,
and does not allow endpoint scoring. It only narrows the equation-kernel blocker
to the missing kernel-expression artifact.
