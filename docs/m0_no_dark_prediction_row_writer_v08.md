# M0 No-Dark Prediction Row Writer v08

**Doc class:** prediction-row writer gate
**Status:** writer gate present; numeric row emission blocked

Script:

```text
scripts/build_m0_no_dark_prediction_row_writer.py
```

Derived outputs:

```text
data/derived/m0_no_dark_prediction_row_writer_v08.csv
data/derived/m0_no_dark_prediction_row_writer_summary_v08.csv
```

This artifact closes the narrow `m0_no_dark_prediction_row_writer_v08`
presence blocker without writing `v_pred_km_s` rows. The writer gate is present,
but it refuses row emission because the M0 no-dark path still lacks an
executable, dimensionally audited prediction kernel.

## Current Result

The expected status is:

```text
M0_NO_DARK_PREDICTION_ROW_WRITER_PRESENT_BLOCKED_EXECUTABLE_KERNEL_MISSING
```

The next required artifact is:

```text
m0_no_dark_executable_prediction_kernel_v08
```

## Claim Boundary

This gate does not compute velocities, does not write numeric family prediction
rows, does not compare M0/M1/M2, does not activate endpoint scoring, and does
not decide the dark-sector question. It only states the minimum condition under
which the M0 no-dark family could later emit prediction rows.
