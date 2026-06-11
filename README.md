# Tau Core Galaxy Dark-Sector Decision Paper 11

This repository is the initial private scaffold for Paper 11:

**A source-frozen decision protocol for dark-sector necessity in Tau Core galaxy rotation**

The paper is designed as a narrow decision protocol built on Paper 10-style
freeze discipline and Paper 9/10 galaxy-readout experience. It asks whether
galaxy-rotation endpoints require a dark-sector response layer, or whether a
no-dark Tau morphology/readout endpoint can remain sufficient under held-out
tests and wrong-family controls.

## Main Claim

The repository defines a reproducible decision scaffold for comparing three
model families:

```text
M0: no-dark Tau morphology/readout endpoint
M1: Tau base-substrate / Tau dark-sector response endpoint
M2: standard dark-sector benchmark endpoint
```

The decision is galaxy-scope only and must be made from source-frozen inputs,
held-out endpoint tests, and controls that prevent residual leakage.

## Does Not Claim

- It does not claim that dark matter does not exist.
- It does not claim that Tau Core replaces the standard dark sector.
- It does not claim that a Tau dark-sector response field has been proved.
- It does not claim a `Response_tau` formula.
- It does not claim lensing, CMB, BAO, supernova, growth, or cosmological validation.
- It does not claim a galaxy-rotation endpoint result.

## Included Data

Only compact protocol manifests are included:

```text
data/source_manifest/model_family_decision_protocol.csv
data/source_manifest/policy_bundle_freeze_requirements.csv
data/source_manifest/decision_outcome_ladder.csv
```

These are source-side decision artifacts. They contain no endpoint residuals
and no fitted galaxy results.

## Reproduce

```bash
python scripts/reproduce.py
```

The reproduction script validates the protocol manifests, compiles the
manuscript with `tectonic`, builds `arxiv_submission_source.zip`, and runs
pytest smoke tests.

## arXiv Source Package

`arxiv_submission_source.zip` is generated from `paper11_submission_source/`
and excludes `main.pdf` plus TeX build byproducts.

## Scope

Paper 11 should remain a decision paper:

```text
Paper 10 provides galaxy-readout and freeze-method foundations.
Paper 11 compares no-dark, Tau dark-sector response, and standard dark-sector
benchmark families under the same endpoint-blind decision protocol.
```

The next honest target is a frozen policy-bundle instance, not a response
formula or physical readout claim.
