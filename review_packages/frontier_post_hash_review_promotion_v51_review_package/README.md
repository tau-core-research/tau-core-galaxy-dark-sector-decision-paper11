# Frontier Post-Hash Review Promotion Package

**Status:** review package only; not v21 evidence input; no source import; no endpoint scoring.

This package is for a human review-promotion decision after the v50 external
SPARC hash recomputation audit closed the hash caveat.

## What Is Already Closed

- The v46 draft has the v21 column shape but remains review-required.
- The v48 response passed route/prescore checks but did not authorize v21 copy.
- The v50 hash audit recomputed and matched the SPARC Table1 hash.
- The v51 recheck confirms hash support for all eighteen review rows.

## What Is Still Needed

The reviewer must explicitly decide whether the eighteen rows may be promoted
to active v21 provenance evidence.

Use:

```text
templates/frontier_review_promotion_authorization_TEMPLATE.csv
```

Only a later ingestion gate may consume a completed authorization response. This
package itself must not be copied into:

```text
data/input/source_import_provenance_evidence_v21.csv
```

## Hard Stops

- Do not treat this package as active v21 evidence.
- Do not mark `PROVENANCE_EVIDENCE_COMPLETE` from this package alone.
- Do not import observed values or run endpoint scoring from this package.
- Do not use endpoint residuals, family winners, or score outcomes to authorize
  provenance rows.
