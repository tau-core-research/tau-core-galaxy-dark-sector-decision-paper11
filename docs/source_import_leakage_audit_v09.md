# Source Import and Leakage Audit v09

**Doc class:** executable source-import/leakage gate
**Status:** source values and leakage pass ready; no rows activated

Script:

```text
scripts/run_source_import_leakage_audit.py
```

Derived outputs:

```text
data/derived/source_import_and_leakage_audit_v09.csv
data/derived/source_import_requirements_v09.csv
data/derived/leakage_audit_findings_v09.csv
data/derived/source_import_leakage_summary_v09.csv
```

This layer audits the v08 scoring-input scaffold. It now sees the v12
real-values input, the v77-written v10 leakage evidence input, and the v78
leakage-pass review result. It records the source-import and leakage audit as
ready, but it keeps every row unactivated until a separate scoring activation
policy or gate allows activation.

## Current Result

The expected status is:

```text
SOURCE_IMPORT_AND_LEAKAGE_READY
```

All eighteen rows pass leakage audit. No row is activated for scoring.

## Claim Boundary

This audit does not compute scores, does not compare `M0`, `M1`, or `M2`, and
does not produce a dark-sector verdict.

Next honest target:

```text
scoring_activation_gate_recheck_after_leakage_pass
```
