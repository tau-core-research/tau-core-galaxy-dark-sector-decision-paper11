# Frontier Provenance v46 Review Package

**Status:** review package only; not v21 evidence input; no source import; no endpoint scoring.

This package is for reviewing the proposed provenance evidence payload before
anything is copied to `data/input/source_import_provenance_evidence_v21.csv`.

## Reviewer Tasks

1. Verify each SPARC source route points to the intended pre-score source row.
2. Verify the source hash/accession matches the stated source file.
3. Verify the leakage-evidence id is a pre-score source-route review id, not a
   post-score/model-selection artifact.
4. Only after review may a later promotion step mark rows as
   `PROVENANCE_EVIDENCE_COMPLETE`.

## Hard Stops

- Do not treat this package as the v21 evidence input.
- Do not copy rows into `data/input/source_import_provenance_evidence_v21.csv`
  unless a separate review-promotion gate explicitly authorizes it.
- Do not use endpoint residuals, family winners, or scores to approve source
  routes.
