# Leakage Prescore Artifact Request Ledger v64

**Doc class:** leakage prescore artifact request ledger
**Status:** request ledger open; no leakage evidence; no activation; no scoring allowed

## Script

```text
scripts/build_leakage_prescore_artifact_request_ledger.py
```

## Outputs

```text
data/derived/leakage_prescore_artifact_request_ledger_v64.csv
data/derived/leakage_prescore_artifact_request_coverage_v64.csv
data/derived/leakage_prescore_artifact_request_summary_v64.csv
```

## Purpose

This layer converts the v63 no-go intake into a row-level request ledger. Each
open LEC10 row now has a request family, minimal required fields, forbidden
endpoint-derived inputs, and a review question.

## Current Result

The ledger contains 72 open request rows across eighteen galaxies and four
leakage checks. It creates zero leakage-evidence rows, authorizes zero
activation rows, and keeps endpoint scoring disabled.

## Claim Boundary

This request ledger is not active leakage evidence. It does not pass leakage
audit, activate scoring rows, compute scores, compare model families, or decide
dark-sector necessity.
