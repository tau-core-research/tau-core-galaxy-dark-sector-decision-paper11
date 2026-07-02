# Control Execution Readiness v09

**Doc class:** control execution readiness gate
**Status:** control contracts ready for score-calculation preflight; verdict controls not executed

Script:

```text
scripts/build_control_execution_readiness.py
```

Derived outputs:

```text
data/derived/control_execution_readiness_v09.csv
data/derived/control_execution_readiness_summary_v09.csv
```

This gate separates two things that must not be conflated:

- score-calculation preflight readiness, where each control has a frozen output
  contract and can be scheduled around the primary scoring run;
- verdict-control readiness, which requires executed control result rows and
  reviewed pass/fail outcomes.

Several controls require the primary score table before they can be evaluated.
Therefore this artifact does not claim that controls have passed. It only
records that the control contracts are ready enough not to block the first raw
score-calculation runner.

## Claim Boundary

This artifact writes no control result rows, computes no control scores, claims
no control pass, authorizes no endpoint verdict, and makes no dark-sector
verdict.
