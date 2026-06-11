# Galaxy Sample Freeze v01

**Doc class:** sample-freeze manifest  
**Status:** policy only; no galaxy list selected, no endpoint scoring  

Machine-readable manifest:

```text
data/source_manifest/galaxy_sample_freeze_v01.csv
```

This file declares the source-side sample policies needed before Paper 11 can
compare `M0`, `M1`, and `M2`.

## Current Status

No concrete galaxy identifiers are selected in v01. This is deliberate. The
manifest freezes the roles that must be filled next:

- sample scope;
- train/calibration subset;
- held-out decision subset;
- challenge/problematic subset;
- exclusion policy.

## Claim Boundary

This manifest does not claim:

- a galaxy endpoint result;
- a train/held-out split;
- that any family wins;
- that dark sector is needed or not needed.

Next honest target:

```text
SOURCE_SIDE_GALAXY_LIST_FREEZE_V02
```
