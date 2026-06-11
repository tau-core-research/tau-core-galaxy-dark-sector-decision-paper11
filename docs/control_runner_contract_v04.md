# Control Runner Contract v04

**Doc class:** control-runner contract  
**Status:** runner contracts declared; no implementation; no control result  

Machine-readable manifest:

```text
data/source_manifest/control_runner_contract_v04.csv
```

This manifest defines the input and output contracts for the Paper 11 controls.
It is the bridge between frozen control policy and executable control scripts.

## Runner Contracts

Each runner must state:

- the frozen inputs it is allowed to consume;
- the output table it must produce;
- the activation dependencies that must be satisfied first;
- the endpoint-derived inputs it is forbidden to use.

The contracts cover shuffled labels, wrong-family assignment, null-source
baseline, leakage audit, radial-zone perturbation, and family-budget parity.

## Claim Boundary

No runner is implemented or executed here. Passing these contracts will be a
future reproducibility step, not a current scientific result.

Next honest target:

```text
CONTROL_RUNNER_IMPLEMENTATION_V05
```
