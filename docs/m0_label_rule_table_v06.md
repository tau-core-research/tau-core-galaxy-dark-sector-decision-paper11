# M0 Label Rule Table v06

**Doc class:** M0 morphology-label rule table
**Status:** label rule ready; no label validation; scoring blocked

Script:

```text
scripts/build_m0_label_rule_table.py
```

Derived outputs:

```text
data/derived/m0_label_rule_table_v06.csv
data/derived/m0_label_rule_table_summary_v06.csv
```

This artifact fills the M0 `morphology_label_rule` formula slot with a frozen
pre-scoring rule table. It defines source-observable scope, label categories,
fallback labels, exception handling, row scope, and freeze audit requirements.

## Current Result

The expected status is:

```text
M0_LABEL_RULE_TABLE_READY_SCORING_BLOCKED
```

The next required artifact is:

```text
m1_tau_response_formula_table_v06
```

## Claim Boundary

This table defines a label rule only. It writes no row-level label values,
does not validate morphology labels, does not compute endpoint scores, does not
compare M0/M1/M2, and does not decide whether a dark-sector component is
required.
