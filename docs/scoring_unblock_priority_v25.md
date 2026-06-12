# Scoring Unblock Priority v25

**Doc class:** scoring unblock priority ledger  
**Status:** first scoring frontier identified; no scoring allowed  

Script:

```text
scripts/build_scoring_unblock_priority.py
```

Derived outputs:

```text
data/derived/scoring_unblock_priority_v25.csv
data/derived/scoring_unblock_priority_summary_v25.csv
```

This layer converts the v24 dependency closure into an ordered unblock plan. It
does not open the scoring path. It identifies which blocked dependency is the
current source-side frontier and which global scoring prerequisites can be
prepared in parallel.

## Current Result

The expected status is:

```text
SCORING_UNBLOCK_FRONTIER_IDENTIFIED
```

The first frontier dependency is:

```text
SCD24_FAMILY_FORMULA_TABLES
```

The first required artifact is:

```text
m0_no_dark_rule_parent_assumption_basis_v14
```

## Claim Boundary

This priority ledger is not a score, not a model comparison, not empirical
validation, and not a dark-sector verdict. It only records the current
protocol-safe order for unblocking the endpoint scoring path.
