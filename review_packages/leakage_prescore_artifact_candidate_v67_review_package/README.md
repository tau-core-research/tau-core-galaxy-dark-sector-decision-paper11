# Leakage Prescore Artifact Candidate v67 Review Package

**Status:** candidate review package only; not leakage evidence; no activation; no endpoint scoring.

This package converts the v67 candidate ledger into a fillable response
template. It asks reviewers to accept or reject each candidate artifact before
any later leakage-evidence ingestion gate may consider it.

## Reviewer Tasks

1. Review the proposed candidate artifact URI/id and hash/accession.
2. Confirm whether the candidate covers the minimal required fields.
3. Confirm whether the candidate is prescore and uses no forbidden inputs.
4. Mark whether the row may become a leakage-evidence candidate after a later
   ingestion gate. Keep activation and endpoint scoring disabled.

## Hard Stops

- Do not treat this package as active leakage evidence.
- Do not copy rows into `data/input/leakage_audit_evidence_v10.csv`.
- Do not mark leakage rows as passed from this package.
- Do not activate scoring rows or compute endpoint scores.
