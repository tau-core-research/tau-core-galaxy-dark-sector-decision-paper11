# Frontier Provenance Evidence Acceptance v26

**Doc class:** first-frontier evidence acceptance checklist  
**Status:** evidence acceptance pending input; no scoring allowed  

Script:

```text
scripts/build_frontier_provenance_evidence_acceptance.py
```

Derived outputs:

```text
data/derived/frontier_provenance_evidence_acceptance_v26.csv
data/derived/frontier_provenance_evidence_acceptance_summary_v26.csv
```

This layer turns the v25 first frontier into a row-level acceptance checklist.
It defines what must be present before provenance evidence can be reviewed for
promotion. It does not create evidence, mutate provenance, import observed
values, activate rows, or score model families.

## Current Result

The expected status is:

```text
FRONTIER_EVIDENCE_ACCEPTANCE_PENDING_INPUT
```

No real `data/input/source_import_provenance_evidence_v21.csv` file is present,
so all eighteen candidate rows remain blocked and zero rows are accepted for
promotion review.

## Claim Boundary

This checklist is not provenance evidence and not a scoring result. It only
records the minimum row-level acceptance conditions for the current scoring
frontier.
