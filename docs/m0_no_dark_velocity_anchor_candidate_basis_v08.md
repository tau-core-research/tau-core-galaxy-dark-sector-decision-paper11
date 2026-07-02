# M0 No-Dark Velocity-Anchor Candidate Basis v08

**Doc class:** velocity-anchor candidate-basis gate
**Status:** candidate basis present; anchor selection rule missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_anchor_candidate_basis.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_anchor_candidate_basis_v08.csv
data/derived/m0_no_dark_velocity_anchor_candidate_basis_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_anchor_candidate_basis_v08`
presence blocker by listing only admissible classes of velocity-anchor carriers.
The candidate basis is source-side and pre-scoring. It permits only candidate
classes that can carry velocity or acceleration dimension without using
observed rotation residuals, heldout scores, family winners, best-fit curves,
posthoc rescaling, or fitted coefficient quality.

The basis does not choose among candidates. That narrower choice remains the
next required gate.

## Current Result

The expected status is:

```text
M0_NO_DARK_ANCHOR_CANDIDATE_BASIS_PRESENT_BLOCKED_ANCHOR_SELECTION_RULE_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_anchor_selection_rule_v08
```

## Claim Boundary

This gate declares only admissible and rejected candidate classes. It does not choose an anchor candidate, does not choose an anchor value, does not assign coupling normalization, does not write a velocity formula, does not write prediction rows, does not run endpoint scoring, and does not decide whether a dark-sector component is required.
