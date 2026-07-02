# M0 No-Dark Velocity-Anchor Selection Rule v08

**Doc class:** velocity-anchor selection-rule gate
**Status:** selection rule present; anchor value freeze missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_anchor_selection_rule.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_anchor_selection_rule_v08.csv
data/derived/m0_no_dark_velocity_anchor_selection_rule_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_anchor_selection_rule_v08`
presence blocker by declaring a pre-scoring priority and fallback rule over the
admissible anchor classes. The rule prefers source-side baryonic gravitational
velocity/acceleration carriers, then source-side dimensioned field carriers,
then independently imported source-scale carriers when provenance and leakage
guards allow them. It rejects observed-rotation or residual-fit carriers under
all M0 no-dark scoring paths.

The rule does not freeze a concrete anchor value. That remains the next
required gate.

## Current Result

The expected status is:

```text
M0_NO_DARK_ANCHOR_SELECTION_RULE_PRESENT_BLOCKED_ANCHOR_VALUE_FREEZE_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_anchor_value_freeze_v08
```

## Claim Boundary

This gate declares only the pre-scoring selection rule over candidate classes. It does not freeze an anchor value, does not assign coupling normalization, does not write a velocity formula, does not write prediction rows, does not run endpoint scoring, and does not decide whether a dark-sector component is required.
