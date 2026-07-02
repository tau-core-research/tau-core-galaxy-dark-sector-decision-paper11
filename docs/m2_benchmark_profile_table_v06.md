# M2 Benchmark Profile Table v06

**Doc class:** M2 benchmark-profile table contract
**Status:** benchmark profile table ready; nuisance policy blocked; no scoring

Script:

```text
scripts/build_m2_benchmark_profile_table.py
```

Derived outputs:

```text
data/derived/m2_benchmark_profile_table_v06.csv
data/derived/m2_benchmark_profile_table_summary_v06.csv
```

This artifact fills the M2 `benchmark_profile_formula` slot as a pre-scoring
contract. It freezes the benchmark profile-family policy, halo-parameter slot
policy, prior policy, nuisance-policy handoff, profile-switch guard, and
prediction handoff.

## Current Result

The expected status is:

```text
M2_BENCHMARK_PROFILE_TABLE_READY_NUISANCE_BLOCKED
```

The next required artifact is:

```text
m2_nuisance_policy_table_v06
```

## Claim Boundary

This table does not validate the standard dark sector, does not prove an M2
endpoint result, writes no numeric profile values, writes no M2 prediction
rows, computes no endpoint scores, and makes no dark-sector verdict.
