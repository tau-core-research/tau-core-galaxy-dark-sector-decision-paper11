# Source Import and Leakage Audit v09

**Doc class:** executable source-import/leakage gate
**Status:** source values and leakage evidence present; pass review pending; no rows activated

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

This layer audits the v08 scoring-input scaffold. It now sees both the v12
real-values input and the v77-written v10 leakage evidence input, but it keeps
every row blocked until a separate leakage-pass review gate passes.

## Current Result

The expected status is:

```text
SOURCE_IMPORT_READY_LEAKAGE_EVIDENCE_REVIEW_PENDING
```

No row passes leakage audit and no row is activated for scoring.

## Claim Boundary

This audit does not compute scores, does not compare `M0`, `M1`, or `M2`, and
does not produce a dark-sector verdict.

Next honest target:

```text
leakage_audit_pass_review_gate_after_v10_evidence
```
