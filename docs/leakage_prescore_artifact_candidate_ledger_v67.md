# Leakage Prescore Artifact Candidate Ledger v67

**Doc class:** leakage prescore artifact candidate ledger
**Status:** candidates identified for review; no leakage evidence; no activation; no scoring allowed

## Script

```text
scripts/build_leakage_prescore_artifact_candidate_ledger.py
```

## Outputs

```text
data/derived/leakage_prescore_artifact_candidate_ledger_v67.csv
data/derived/leakage_prescore_artifact_candidate_coverage_v67.csv
data/derived/leakage_prescore_artifact_candidate_summary_v67.csv
```

## Purpose

This layer maps each open v64 request to the best available prescore artifact
candidate already present in the repository. It separates full candidates from
partial candidates and keeps every row review-required.

## Current Result

The ledger identifies 72 candidate rows across eighteen galaxies and four
leakage checks. Source-route and observed-input candidates are present. Morph
label and benchmark-policy candidates are partial and require reviewer
confirmation or stronger bundle support.

## Claim Boundary

This candidate ledger is not active leakage evidence. It does not pass leakage
audit, activate scoring rows, compute scores, compare model families, or decide
dark-sector necessity.
