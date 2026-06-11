# Leakage Prescore Artifact Request v64 Review Package

**Status:** review package only; not leakage evidence; no activation; no endpoint scoring.

This package converts the v64 request ledger into a fillable response template.
It asks reviewers to provide reviewed prescore artifact identifiers and
hash/accession values for each open LEC10 row.

## Reviewer Tasks

1. Fill the requested prescore artifact URI/id and hash/accession.
2. Verify that all minimal required fields are covered.
3. Confirm the artifact is prescore and does not use endpoint residuals, family
   winners, best-fit scores, or post-score selections.
4. Keep activation and endpoint scoring disabled. A later ingestion gate must
   decide whether any row can become leakage evidence.

## Hard Stops

- Do not treat this package as active leakage evidence.
- Do not copy rows into `data/input/leakage_audit_evidence_v10.csv`.
- Do not mark leakage rows as passed from this package.
- Do not activate scoring rows or compute endpoint scores.
