# Control Implementation Freeze v03

**Doc class:** control implementation manifest  
**Status:** implementation policy frozen; controls not run; no verdict  

Machine-readable manifest:

```text
data/source_manifest/control_implementation_freeze_v03.csv
```

This manifest fixes how the Paper 11 controls must be implemented before
endpoint scoring is allowed.

## Frozen Controls

The v03 controls are:

- shuffled source labels;
- wrong-family assignments;
- null-source baseline;
- residual-leakage audit;
- radial-zone perturbation;
- family-budget parity check.

Each control is a veto or downgrade gate. Passing a control does not prove a
family; failing a control prevents the corresponding interpretation from being
used.

## Claim Boundary

This manifest does not execute controls. It does not produce:

- control scores;
- family rankings;
- source-structure validation;
- a dark-sector verdict.

Next honest target:

```text
CONTROL_RUNNER_AND_LEAKAGE_AUDIT_V04
```
