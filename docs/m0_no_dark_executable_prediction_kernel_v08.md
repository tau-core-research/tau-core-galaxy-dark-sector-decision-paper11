# M0 No-Dark Executable Prediction Kernel v08

**Doc class:** executable prediction-kernel gate
**Status:** kernel gate present; velocity formula missing; no predictions

Script:

```text
scripts/build_m0_no_dark_executable_prediction_kernel.py
```

Derived outputs:

```text
data/derived/m0_no_dark_executable_prediction_kernel_v08.csv
data/derived/m0_no_dark_executable_prediction_kernel_summary_v08.csv
```

This artifact closes the `m0_no_dark_executable_prediction_kernel_v08`
presence blocker without promoting the M0 no-dark source-side expression body
into a velocity formula. It records that the next missing object is the
velocity-readout formula body needed before any `v_pred_km_s` row can be
emitted.

## Current Result

The expected status is:

```text
M0_NO_DARK_EXECUTABLE_KERNEL_PRESENT_BLOCKED_VELOCITY_FORMULA_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_readout_formula_v08
```

## Claim Boundary

This gate does not define a velocity formula, does not assign coefficients,
does not write prediction rows, does not run endpoint scoring, and does not
decide the dark-sector question. It only narrows the scoring blocker from
``executable kernel missing'' to the missing M0 no-dark velocity-readout
formula.
