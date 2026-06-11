# Source Field Completeness v04

**Doc class:** activation-readiness manifest  
**Status:** required fields declared; no source rows activated; no endpoint scoring  

Machine-readable manifest:

```text
data/source_manifest/source_field_completeness_v04.csv
```

This manifest defines the minimum source-side fields needed before any Paper
11 galaxy row can become active for scoring.

## Required Field Families

The activation gate requires:

- radial grid and velocity uncertainty inputs;
- baryonic component inputs shared across `M0`, `M1`, and `M2`;
- morphology/readout labels for Tau-source families;
- environment/path flags where path terms may matter;
- spin, H I envelope, or position-velocity proxies before response activation;
- standard benchmark profile inputs for `M2`;
- leakage audit pass before any row is activated.

## Claim Boundary

This manifest does not fill the fields. It only says what must be complete
before scoring is allowed.

Next honest target:

```text
SOURCE_FIELD_ROW_AUDIT_V05
```
