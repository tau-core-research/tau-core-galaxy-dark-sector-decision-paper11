# Leakage Partial Candidate Sufficiency Review Package v71

This package defines the minimum leakage policy after the v70 ingestion gate and
creates a review handoff for the 36 partial candidate rows.

## Status

- Required leakage components for endpoint scoring: 4
- Components with full draft candidates: 2
- Components requiring sufficiency review: 2
- Partial candidate rows requiring review: 36
- Minimum scoring policy: full four-component leakage required before endpoint scoring

## Claim Boundary

This package is not active leakage evidence. It does not write
`data/input/leakage_audit_evidence_v10.csv`, authorize leakage pass, activate
rows, compute scores, or make a dark-sector verdict.

The package only asks reviewers whether the blocked morphology-label and
benchmark-policy candidate rows are sufficient for a later leakage-evidence
ingestion gate.

## Next Required Artifact

`completed_leakage_partial_candidate_sufficiency_v71_review_response`
