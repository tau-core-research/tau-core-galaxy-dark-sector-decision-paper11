# M0 No-Dark Readout Equation Interface v08

**Doc class:** no-dark M0 readout-equation interface contract
**Status:** interface ready; equation kernel still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_readout_equation_interface.py
```

Derived outputs:

```text
data/derived/m0_no_dark_readout_equation_interface_v08.csv
data/derived/m0_no_dark_readout_equation_interface_summary_v08.csv
```

This artifact closes the non-kernel interface slots of the M0 no-dark readout
equation: argument signature, output-unit target, parameter exposure,
domain/failure behavior, and serialization handoff.

## Current Result

The expected status is:

```text
M0_NO_DARK_READOUT_EQUATION_INTERFACE_READY
```

The next required artifact is:

```text
m0_no_dark_equation_kernel_v09
```

## Claim Boundary

This interface does not write the equation kernel, does not define a velocity
formula, does not assign numeric coefficients, does not write prediction rows,
and does not allow endpoint scoring. It only narrows the readout-equation
blocker to the missing equation-kernel artifact.
