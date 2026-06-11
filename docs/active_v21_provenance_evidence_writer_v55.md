# Active v21 Provenance Evidence Writer v55

**Doc class:** active provenance evidence input writer  
**Status:** active v21 evidence written; no observed values; no scoring allowed  

Script:

```text
scripts/run_active_v21_provenance_evidence_writer.py
```

Inputs:

```text
data/derived/authorized_provenance_evidence_payload_v54.csv
```

Outputs:

```text
data/input/source_import_provenance_evidence_v21.csv
data/derived/active_v21_provenance_evidence_writer_summary_v55.csv
```

This layer writes the authorized v54 provenance payload into the active v21
input location. It writes only source provenance fields and does not import
observed rotation values.

## Current Result

The expected status is:

```text
ACTIVE_V21_PROVENANCE_EVIDENCE_WRITTEN
```

All eighteen rows are written with `PROVENANCE_EVIDENCE_COMPLETE`. Endpoint
scoring remains disabled.

## Claim Boundary

This writer closes the active provenance-evidence input frontier only. It is
not observed source import, not endpoint scoring, and not a dark-sector verdict.
The next frontier is reviewed raw SPARC-like source input.
