# M0 No-Dark Velocity-Anchor Source Law v08

**Doc class:** velocity-anchor source-law gate
**Status:** source-law gate present; anchor candidate basis missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_anchor_source_law.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_anchor_source_law_v08.csv
data/derived/m0_no_dark_velocity_anchor_source_law_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_anchor_source_law_v08` presence
blocker by declaring the rule class for a lawful velocity anchor. The no-dark
M0 route may only obtain velocity dimension from a source-side, pre-scoring,
dimensioned carrier. The anchor cannot be chosen from endpoint residuals,
heldout scores, family winners, best-fit curves, posthoc rescaling, or fitted
coefficient quality.

The artifact intentionally does not list the admissible candidate carriers.
That narrower basis remains the next required gate.

## Current Result

The expected status is:

```text
M0_NO_DARK_ANCHOR_SOURCE_LAW_PRESENT_BLOCKED_ANCHOR_CANDIDATE_BASIS_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_anchor_candidate_basis_v08
```

## Claim Boundary

This gate declares only the source-law admissibility layer. It does not choose an anchor candidate, does not choose an anchor value, does not assign coupling normalization, does not write a velocity formula, does not write prediction rows, does not run endpoint scoring, and does not decide whether a dark-sector component is required.
