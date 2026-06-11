# Galaxy Decision Endpoint Manifest v01

**Doc class:** endpoint decision manifest  
**Status:** decision fields declared; no galaxy sample selected, no scoring, no verdict  

This document declares the first galaxy-scope decision manifest for Paper 11.
The machine-readable manifest is:

```text
data/source_manifest/galaxy_decision_endpoint_manifest_v01.csv
```

## Purpose

The endpoint manifest defines what must be frozen before comparing:

```text
M0 = no-dark Tau morphology/readout
M1 = Tau base-substrate response
M2 = standard dark-sector benchmark
```

## Required Before Scoring

Before any model family can be evaluated, Paper 11 must freeze:

- endpoint scope;
- train-sample policy;
- held-out sample policy;
- shared scoring rule;
- wrong-family controls;
- shuffle controls;
- radial-zone diagnostics;
- decision ladder.

## Current Status

No galaxy sample is selected in this v01 manifest. This is deliberate: sample
selection is the next source-side task and must be completed before endpoint
scoring.

Allowed status:

```text
GALAXY_DECISION_ENDPOINT_MANIFEST_V01_DECLARED
```

Forbidden status:

```text
M0 wins;
M1 wins;
M2 wins;
dark sector required;
dark sector not required;
standard dark matter rejected.
```
