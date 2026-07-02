# M0 No-Dark Formula Body Interface v08

**Doc class:** no-dark M0 formula-body interface contract
**Status:** interface ready; readout equation still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_formula_body_interface.py
```

Derived outputs:

```text
data/derived/m0_no_dark_formula_body_interface_v08.csv
data/derived/m0_no_dark_formula_body_interface_summary_v08.csv
```

This artifact promotes the non-equation interface pieces needed by the later M0
no-dark formula body. It records the source-argument, baryonic handoff,
scale-slot, coefficient-domain, fallback-branch, and output-unit interfaces.

## Current Result

The expected status is:

```text
M0_NO_DARK_FORMULA_BODY_INTERFACE_READY
```

The next required artifact is:

```text
m0_no_dark_readout_equation_v08
```

## Claim Boundary

This interface does not write the M0 no-dark readout equation, does not define a
velocity formula, does not assign numeric coefficient values, does not write
prediction rows, and does not allow endpoint scoring. It only narrows the
family-prediction blocker to the missing readout-equation artifact.
