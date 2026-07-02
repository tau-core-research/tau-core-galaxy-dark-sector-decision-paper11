#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
ADMISSIBILITY_SUMMARY = DERIVED / "m0_no_dark_expression_admissibility_rule_summary_v13.csv"


FIELDNAMES = [
    "policy_id",
    "admissibility_id",
    "policy_class",
    "null_behavior",
    "fallback_behavior",
    "blocked_route",
    "allowed_handoff",
    "forbidden_inputs",
    "policy_status",
    "source_rule_claim_allowed",
    "expression_claim_allowed",
    "formula_claim_allowed",
    "numeric_prediction_allowed",
    "endpoint_scoring_allowed",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def admissibility_ready() -> bool:
    if not ADMISSIBILITY_SUMMARY.exists():
        return False
    rows = read_csv(ADMISSIBILITY_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_EXPRESSION_ADMISSIBILITY_RULE_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def policy_rows() -> list[dict[str, object]]:
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_exception"
    rows = [
        {
            "policy_id": "M0NDNFB13_SOURCE_FREEZE_NULL_POLICY",
            "admissibility_id": "M0NDADM13_SOURCE_FREEZE_ADMISSIBILITY",
            "policy_class": "source_freeze_null_policy",
            "null_behavior": "missing frozen source-domain evidence keeps the route unresolved",
            "fallback_behavior": "do not impute source-domain fields from endpoint rows",
            "blocked_route": "source_domain_missing",
            "allowed_handoff": "output_class_blocked_route",
        },
        {
            "policy_id": "M0NDNFB13_NO_DARK_CONSTRAINT_POLICY",
            "admissibility_id": "M0NDADM13_NO_DARK_EXCLUSION_ADMISSIBILITY",
            "policy_class": "no_dark_constraint_policy",
            "null_behavior": "no-dark exclusion remains a dimensionless absence constraint",
            "fallback_behavior": "constraint violation blocks M0 rather than adding dark-response compensation",
            "blocked_route": "explicit_dark_response_attempted",
            "allowed_handoff": "output_class_family_constraint",
        },
        {
            "policy_id": "M0NDNFB13_MORPHOLOGY_LABEL_POLICY",
            "admissibility_id": "M0NDADM13_MORPHOLOGY_READOUT_ADMISSIBILITY",
            "policy_class": "morphology_label_null_policy",
            "null_behavior": "ambiguous or missing morphology/readout label leaves the source factor unresolved",
            "fallback_behavior": "do not switch morphology labels after seeing endpoint residuals",
            "blocked_route": "morphology_readout_unresolved",
            "allowed_handoff": "output_class_typed_source_factor",
        },
        {
            "policy_id": "M0NDNFB13_U_READ_INCOMPARABILITY_POLICY",
            "admissibility_id": "M0NDADM13_U_READ_MARKER_ADMISSIBILITY",
            "policy_class": "u_read_incomparability_policy",
            "null_behavior": "empty or incomparable U_read marker remains a non-scalar admissibility state",
            "fallback_behavior": "do not coerce U_read into a fitted scalar score",
            "blocked_route": "u_read_incomparable",
            "allowed_handoff": "output_class_admissibility_marker",
        },
        {
            "policy_id": "M0NDNFB13_BARYONIC_BINDING_POLICY",
            "admissibility_id": "M0NDADM13_BARYONIC_BINDING_ADMISSIBILITY",
            "policy_class": "baryonic_binding_null_policy",
            "null_behavior": "missing or unit-inconsistent baryonic/source binding remains unresolved",
            "fallback_behavior": "do not repair missing units or normalization from best-fit curves",
            "blocked_route": "baryonic_binding_unresolved",
            "allowed_handoff": "output_class_source_input_binding",
        },
        {
            "policy_id": "M0NDNFB13_FAILURE_ROUTE_POLICY",
            "admissibility_id": "M0NDADM13_FAILURE_ROUTE_ADMISSIBILITY",
            "policy_class": "failure_route_policy",
            "null_behavior": "underdetermined source-basis route remains blocked",
            "fallback_behavior": "failure marker dominates post-hoc exception creation",
            "blocked_route": "failure_route_dominates",
            "allowed_handoff": "output_class_blocked_route",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["policy_status"] = "READY"
        row["source_rule_claim_allowed"] = "false"
        row["expression_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_expression_null_fallback_policy_only_no_source_rule_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["policy_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    return [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_NULL_FALLBACK_POLICY_V13",
            "null_fallback_artifact": "m0_no_dark_expression_null_fallback_policy_v13",
            "admissibility_status": "READY" if admissibility_ready() else "BLOCKED",
            "policy_rows": len(rows),
            "ready_policy_rows": ready,
            "blocked_policy_rows": blocked,
            "source_rule_claim_allowed": "false",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_NULL_FALLBACK_POLICY_READY"
            if blocked == 0 and admissibility_ready()
            else "M0_NO_DARK_EXPRESSION_NULL_FALLBACK_POLICY_BLOCKED",
            "next_required_artifact": "m0_no_dark_expression_output_class_v13",
            "claim_boundary": "m0_no_dark_expression_null_fallback_policy_only_no_source_rule_no_formula_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_expression_null_fallback_policy_v13.md").write_text(
        """# M0 No-Dark Expression Null/Fallback Policy v13

**Doc class:** no-dark M0 expression null/fallback policy record
**Status:** null/fallback policy ready; output class still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_expression_null_fallback_policy.py
```

Derived outputs:

```text
data/derived/m0_no_dark_expression_null_fallback_policy_v13.csv
data/derived/m0_no_dark_expression_null_fallback_policy_summary_v13.csv
```

This artifact records how null, gauge, missing-input, incomparability, and
failure-route cases are handled before any no-dark M0 source rule is written.
It blocks endpoint-selected repairs and post-hoc exceptions.

## Current Result

The expected status is:

```text
M0_NO_DARK_EXPRESSION_NULL_FALLBACK_POLICY_READY
```

Six null/fallback rows are ready:

- source-domain null policy;
- no-dark constraint violation policy;
- morphology/readout label policy;
- finite-local `U_read` incomparability policy;
- baryonic/source binding null policy;
- failure-route domination policy.

The next missing artifact is:

```text
m0_no_dark_expression_output_class_v13
```

## Claim Boundary

This null/fallback record does not define the M0 no-dark source rule, does not
define an expression, does not write a formula, does not compute predicted
velocities, does not score galaxies, and does not decide the dark-sector
question. It only authorizes the next source-side construction artifact: the
output class.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = policy_rows()
    write_csv(DERIVED / "m0_no_dark_expression_null_fallback_policy_v13.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_expression_null_fallback_policy_summary_v13.csv",
        summary(rows),
        [
            "summary_id",
            "null_fallback_artifact",
            "admissibility_status",
            "policy_rows",
            "ready_policy_rows",
            "blocked_policy_rows",
            "source_rule_claim_allowed",
            "expression_claim_allowed",
            "formula_claim_allowed",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_EXPRESSION_NULL_FALLBACK_POLICY_V13_BUILT")


if __name__ == "__main__":
    main()
