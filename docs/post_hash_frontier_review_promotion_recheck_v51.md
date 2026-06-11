# Post-Hash Frontier Review Promotion Recheck v51

**Doc class:** post-hash promotion recheck  
**Status:** promotion still blocked; no evidence written; no scoring allowed  

Script:

```text
scripts/run_post_hash_frontier_review_promotion_recheck.py
```

Inputs:

```text
data/derived/frontier_provenance_review_response_intake_v48.csv
data/derived/frontier_provenance_review_response_intake_summary_v48.csv
data/derived/frontier_external_hash_recompute_audit_summary_v50.csv
```

Derived outputs:

```text
data/derived/post_hash_frontier_review_promotion_recheck_v51.csv
data/derived/post_hash_frontier_review_promotion_recheck_summary_v51.csv
```

This layer rechecks the v49 promotion blocker after the external hash caveat is
closed by v50.

## Current Result

The expected status is:

```text
POST_HASH_FRONTIER_REVIEW_PROMOTION_RECHECK_BLOCKED
```

The hash blocker is closed for the eighteen review rows, but promotion remains
blocked because the v48 review response did not explicitly authorize:

- copying rows into `data/input/source_import_provenance_evidence_v21.csv`;
- marking provenance evidence complete;
- treating the review response as a promotion decision.

## Claim Boundary

This recheck is not provenance evidence and not a scoring result. It narrows the
next required action to explicit review-promotion authorization after hash
certificate.
