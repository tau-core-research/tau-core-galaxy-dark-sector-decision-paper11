# Scoring Activation Gate v13

**Doc class:** executable scoring-activation gate
**Status:** row activation ready; global scoring blocked; no scoring allowed

Script:

```text
scripts/run_scoring_activation_gate.py
```

Derived outputs:

```text
data/derived/scoring_activation_gate_v13.csv
data/derived/scoring_activation_global_blockers_v13.csv
data/derived/scoring_activation_summary_v13.csv
```

This gate combines row-level and global prerequisites before any endpoint
scoring runner may execute.

## Row-Level Inputs

Each declared scoring row must pass:

```text
real source-value import
leakage audit
row activation
```

## Global Inputs

The endpoint must also have:

```text
family prediction tables
numeric parameter counts
control runner outputs
numeric decision thresholds
```

## Current Result

The expected status is:

```text
SCORING_ROW_ACTIVATION_READY_GLOBAL_SCORING_BLOCKED
```

The current package activates all eighteen rows at the row-gate level, but
keeps endpoint scoring disabled because all four global scoring prerequisites
remain blocked. The first concrete global blocker is
`m0_no_dark_formula_body_v07`.

## Claim Boundary

This gate does not compute scores, compare model families, pass controls, or
decide whether a Tau dark-sector response layer is necessary.
