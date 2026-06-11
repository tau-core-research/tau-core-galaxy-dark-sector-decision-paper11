# Family Parameter Count Freeze v03

**Doc class:** parsimony and family-budget manifest  
**Status:** count rules frozen; numeric counts pending; no endpoint scoring  

Machine-readable manifest:

```text
data/source_manifest/family_parameter_count_freeze_v03.csv
```

This manifest defines what must count as model-family flexibility before Paper
11 compares `M0`, `M1`, and `M2`.

## Frozen Rule

The rule is deliberately conservative:

- any adjustable endpoint coefficient counts;
- any per-galaxy exception counts;
- any post-freeze label switch counts;
- any response carrier, activation gate, scale, amplitude, or handoff choice
  counts unless it is frozen source-side before scoring;
- any benchmark halo/profile switch counts unless it is frozen before scoring.

This protects the decision from a simple failure mode: one family winning
because it was allowed more hidden freedom.

## Claim Boundary

This manifest does not provide final numeric parameter counts. Those require
the actual activated formula tables for `M0`, `M1`, and `M2`.

It does not claim:

- that `M0` is parameter-free;
- that `M1` has a constructed physical response field;
- that `M2` is globally validated;
- that any family wins.

Next honest target:

```text
FAMILY_FORMULA_REGISTRY_AND_NUMERIC_PARAMETER_COUNTS_V04
```
