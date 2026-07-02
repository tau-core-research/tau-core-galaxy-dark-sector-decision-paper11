# M2 Benchmark Parameter Final Count Candidate v14

**Doc class:** M2 benchmark-parameter final-count candidate
**Reader role:** scoring-frontier parameter-count reviewer
**Status:** M2 global benchmark-parameter count candidate ready for freeze; no values; no scoring
**Canonical parent:** M2 benchmark-parameter adjustable-slot resolution v13

Script:

```text
scripts/build_m2_benchmark_parameter_final_count_candidate.py
```

Derived outputs:

```text
data/derived/m2_benchmark_parameter_final_count_candidate_v14.csv
data/derived/m2_benchmark_parameter_final_count_candidate_summary_v14.csv
```

## Current Result

The v14 candidate combines the four zero-valued protocol/guard rows from the
v12 count-value ledger with the eight conditional benchmark/nuisance rows
resolved by the v13 adjustable-slot resolution. The resulting candidate M2
global benchmark-parameter count is recorded only as a freeze input candidate.
The candidate M2 global benchmark-parameter count is protocol-local and not a
physical benchmark-value claim.

The expected status is:

```text
M2_BENCHMARK_PARAMETER_FINAL_COUNT_CANDIDATE_V14_READY_FOR_FREEZE
```

The next required artifact is:

```text
m2_benchmark_parameter_final_count_freeze_v15.csv
```

## Claim Boundary

This artifact does not freeze the final M2 global count, does not write
benchmark/profile values, does not write nuisance values, does not emit M2
prediction rows, does not compute parsimony, does not authorize endpoint
scoring, and does not decide whether a dark-sector benchmark is physically
absent or necessary. It only creates a protocol-local candidate count for the
next freeze/audit gate.

It does not decide whether a dark-sector benchmark is physically absent.
