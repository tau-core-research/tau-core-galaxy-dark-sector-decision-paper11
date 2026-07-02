# M0 No-Dark Source-to-Velocity Coupling Rule v08

**Doc class:** source-to-velocity coupling-rule gate
**Status:** coupling-rule gate present; velocity-unit lift missing; no predictions

Script:

```text
scripts/build_m0_no_dark_source_to_velocity_coupling_rule.py
```

Derived outputs:

```text
data/derived/m0_no_dark_source_to_velocity_coupling_rule_v08.csv
data/derived/m0_no_dark_source_to_velocity_coupling_rule_summary_v08.csv
```

This artifact closes the `m0_no_dark_source_to_velocity_coupling_rule_v08`
presence blocker without declaring a coupling law. It records that the no-dark
path still needs a source-independent velocity-unit lift before unit-free
morphology/readout source variables can be converted into a velocity-dimensional
readout formula.

## Current Result

The expected status is:

```text
M0_NO_DARK_COUPLING_RULE_PRESENT_BLOCKED_VELOCITY_UNIT_LIFT_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_unit_lift_rule_v08
```

## Claim Boundary

This gate does not define a coupling law, does not choose a unit lift, does not
assign coefficients or scales, does not write a velocity formula, does not
write prediction rows, does not run endpoint scoring, and does not decide the
dark-sector question. It only narrows the scoring blocker to the missing
velocity-unit lift rule.
