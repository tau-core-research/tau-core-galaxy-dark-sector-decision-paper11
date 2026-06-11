# Frontier Provenance Evidence Intake Contract v44

**Doc class:** frontier evidence intake contract  
**Status:** intake contract ready; not evidence; no promotion; no endpoint scoring allowed  

Script:

```text
scripts/build_frontier_provenance_evidence_intake_contract.py
```

Derived outputs:

```text
data/derived/frontier_provenance_evidence_intake_contract_v44.csv
data/derived/frontier_provenance_evidence_intake_checklist_v44.csv
data/derived/frontier_provenance_evidence_intake_contract_summary_v44.csv
```

This layer turns the first scoring frontier into a review-safe intake contract
for `data/input/source_import_provenance_evidence_v21.csv`. It defines the
field-level review rules and row-level manual collection checklist needed
before any provenance evidence row may be marked complete.

## Current Result

The expected status is:

```text
FRONTIER_EVIDENCE_INTAKE_CONTRACT_READY_NOT_EVIDENCE
```

The contract defines nine review rules and eighteen row-level collection
checklist entries. It creates zero evidence rows and does not allow provenance
promotion by itself.

## Claim Boundary

This contract is not source evidence, not source import, not endpoint scoring,
and not a dark-sector verdict. It only specifies how reviewed provenance
evidence must be collected before the blocked frontier can move.
