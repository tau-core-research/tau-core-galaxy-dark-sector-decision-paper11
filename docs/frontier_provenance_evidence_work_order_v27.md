# Frontier Provenance Evidence Work Order v27

**Doc class:** first-frontier evidence collection work order  
**Status:** evidence collection open; no evidence written; no scoring allowed  

Script:

```text
scripts/build_frontier_provenance_evidence_work_order.py
```

Derived outputs:

```text
data/derived/frontier_provenance_evidence_work_order_v27.csv
data/derived/frontier_provenance_evidence_work_order_summary_v27.csv
```

This layer converts the v26 acceptance checklist into a concrete source
collection work order. It names the required evidence artifact and the minimum
source tasks for each candidate galaxy. It does not create or write evidence,
mutate provenance, import observed values, activate rows, or compute scores.

## Current Result

The expected status is:

```text
FRONTIER_EVIDENCE_WORK_ORDER_OPEN
```

All eighteen candidate rows remain open evidence-collection tasks. The work
order is a planning artifact only; it does not authorize writing
`data/input/source_import_provenance_evidence_v21.csv`.

## Claim Boundary

This work order is not provenance evidence and not a scoring result. It only
records the source-side work required before the first scoring frontier can be
reviewed.
