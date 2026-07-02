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
keeps endpoint scoring disabled because three global scoring prerequisites
remain blocked after the family formula-table prerequisite became ready. The
first concrete global blocker is
`shared_input_count_discount_policy_v10.csv`, after the M1
response-parameter inventory, countability classification, count-value ledger,
adjustable-slot resolution, final-count candidate, and final-count freeze
became present, and after the M1 per-galaxy response-privilege audit resolved
all eighteen rows as zero protocol-local privileges. The M1 per-galaxy
response-privilege freeze is now present too and freezes those eighteen rows at
zero protocol-local privileges. The M2 benchmark-parameter inventory is now
present too and records twelve profile/nuisance slots for later
classification. The M2 benchmark-parameter countability classification is now
present too and classifies those twelve slots without writing count values.
The M2 benchmark-parameter adjustable-slot resolution is now present too and
resolves the eight conditional benchmark/nuisance rows to zero under the
current no-values/no-predictions scaffold.
The M2 benchmark-parameter final-count candidate is now present too and records
candidate `k_M2_global=0` only as a freeze input.
The M2 benchmark-parameter final-count freeze is now present too and freezes
protocol-local `k_M2_global=0`, handing off to the per-galaxy benchmark
privilege audit.
The M2 benchmark-parameter count-value ledger is now present too and resolves
four protocol/guard rows to zero while leaving eight benchmark/nuisance rows
conditional. This still writes no `Response_tau`, response values, benchmark
values, final M2 count, parsimony, endpoint scores, or a dark-sector verdict.

## Claim Boundary

This gate does not compute scores, compare model families, pass controls, or
decide whether a Tau dark-sector response layer is necessary.
