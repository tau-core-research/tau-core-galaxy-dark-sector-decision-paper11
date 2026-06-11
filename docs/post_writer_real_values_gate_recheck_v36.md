# Post-Writer Real Values Gate Recheck v36

**Doc class:** post-writer real-values gate recheck
**Status:** real-values gate recheck ready; no activation; no scoring allowed

Script:

```text
scripts/run_post_writer_real_values_gate_recheck.py
```

Derived outputs:

```text
data/derived/post_writer_real_values_gate_recheck_v36.csv
data/derived/post_writer_real_values_gate_recheck_summary_v36.csv
```

This layer links the v35 post-writer raw-adapter recheck back to the v12 real
values gate. It confirms that imported numeric values pass the value gate after
the writer path while still not activating rows or computing scores.

## Current Result

The expected status is:

```text
POST_WRITER_REAL_VALUES_GATE_RECHECK_READY
```

All eighteen candidate rows have value-gate support, 450 numeric rows are
imported, eighteen rows pass the value gate, and no row is activated for
scoring.

## Claim Boundary

This recheck is not an observed-data import and not a scoring result. It only
records that the real-values gate is ready while leakage audit and scoring
activation remain blocked.
