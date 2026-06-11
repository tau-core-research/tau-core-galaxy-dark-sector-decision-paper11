# Control Manifest v01

**Doc class:** control-policy manifest  
**Status:** controls declared; no implementation, no endpoint scoring  

Machine-readable manifest:

```text
data/source_manifest/control_manifest_v01.csv
```

The manifest declares controls required before any Paper 11 verdict:

- shuffled source labels;
- wrong-family assignment;
- null-source baseline;
- residual leakage audit;
- radial-zone perturbation/permutation.

## Claim Boundary

This manifest does not run controls and does not report control results. It
only declares which controls must exist before a family can be declared favored.

Next honest target:

```text
CONTROL_IMPLEMENTATION_FREEZE_V02
```
