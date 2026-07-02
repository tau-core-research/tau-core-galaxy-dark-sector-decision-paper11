# M1 Admissibility Table v06

**Doc class:** M1 response-admissibility rule table
**Status:** admissibility table ready; benchmark profile blocked; no response values

Script:

```text
scripts/build_m1_admissibility_table.py
```

Derived outputs:

```text
data/derived/m1_admissibility_table_v06.csv
data/derived/m1_admissibility_table_summary_v06.csv
```

This artifact fills the M1 `response_admissibility_rule` slot as a pre-scoring
contract. It checks source-freeze admissibility, non-circularity, no posthoc
rescue, scale/readout guarding, explicit zero-response cases, and channel
handoff discipline.

## Current Result

The expected status is:

```text
M1_ADMISSIBILITY_TABLE_READY_M2_BENCHMARK_BLOCKED
```

The next required artifact is:

```text
m2_benchmark_profile_table_v06
```

## Claim Boundary

This table does not claim a `Response_tau` formula, does not prove a physical
Tau response field, writes no numeric response values, writes no M1 prediction
rows, computes no endpoint scores, and makes no dark-sector verdict.
