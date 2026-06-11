# Family Formula Registry v04

**Doc class:** formula-slot registry  
**Status:** required formula slots declared; formulas and numeric counts pending  

Machine-readable manifest:

```text
data/source_manifest/family_formula_registry_v04.csv
```

This manifest names the formula slots that must exist before numeric
parameter-count and endpoint scoring can be honest.

## Required Slots

The registry requires:

- `M0` no-dark readout formula and label rule;
- `M1` Tau response formula and response admissibility rule;
- `M2` benchmark profile and nuisance policy;
- shared data-loader/masking policy;
- numeric parameter-count table.

The registry intentionally does not fill these formulas. It prevents Paper 11
from scoring a family whose formula has not been declared before the run.

## Claim Boundary

This manifest does not claim a `Response_tau` formula, a physical response
field, or a family winner.

Next honest target:

```text
FAMILY_FORMULA_TABLES_AND_NUMERIC_COUNTS_V05
```
