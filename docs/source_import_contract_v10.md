# Source Import Contract v10

**Doc class:** executable source-import contract  
**Status:** contract built; values missing; no observed data imported  

Script:

```text
scripts/build_source_import_contract.py
```

Derived outputs:

```text
data/derived/source_import_table_v10.csv
data/derived/observed_input_contract_v10.csv
data/derived/leakage_evidence_contract_v10.csv
data/derived/source_import_contract_summary_v10.csv
```

This layer defines the concrete source-import contract required before scoring
can receive observed inputs.

## Current Result

The expected status is:

```text
SOURCE_IMPORT_CONTRACT_READY_VALUES_MISSING
```

All source routes, numeric observed values, and leakage evidence remain
unfilled.

## Claim Boundary

This contract does not import data, compute scores, pass leakage audit, or
activate any scoring row.

Next honest target:

```text
SOURCE_IMPORT_VALUES_V11
```
