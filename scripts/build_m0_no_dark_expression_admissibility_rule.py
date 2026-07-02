#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
SOURCE_BASIS_SUMMARY = DERIVED / "m0_no_dark_expression_source_basis_summary_v13.csv"


FIELDNAMES = [
    "admissibility_id",
    "basis_id",
    "admissibility_class",
    "admissibility_rule",
    "admissible_handoff",
    "block_condition",
    "forbidden_inputs",
    "admissibility_status",
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


def source_basis_ready() -> bool:
    if not SOURCE_BASIS_SUMMARY.exists():
        return False
    rows = read_csv(SOURCE_BASIS_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_EXPRESSION_SOURCE_BASIS_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def admissibility_rows() -> list[dict[str, object]]:
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_term_selection"
    rows = [
        {
            "admissibility_id": "M0NDADM13_SOURCE_FREEZE_ADMISSIBILITY",
            "basis_id": "M0NDESB13_SOURCE_FREEZE_BASIS",
            "admissibility_class": "source_freeze_admissibility",
            "admissibility_rule": "frozen source-domain basis may enter only as a typed input-domain declaration",
            "admissible_handoff": "source_rule_input_domain",
            "block_condition": "missing frozen source-domain evidence or endpoint-selected input repair",
        },
        {
            "admissibility_id": "M0NDADM13_NO_DARK_EXCLUSION_ADMISSIBILITY",
            "basis_id": "M0NDESB13_NO_DARK_EXCLUSION_BASIS",
            "admissibility_class": "no_dark_constraint_admissibility",
            "admissibility_rule": "no-dark exclusion may enter only as a dimensionless family constraint",
            "admissible_handoff": "source_rule_family_constraint",
            "block_condition": "attempt to introduce explicit dark-response density, mass, acceleration, or compensating term",
        },
        {
            "admissibility_id": "M0NDADM13_MORPHOLOGY_READOUT_ADMISSIBILITY",
            "basis_id": "M0NDESB13_MORPHOLOGY_READOUT_BASIS",
            "admissibility_class": "morphology_factor_admissibility",
            "admissibility_rule": "morphology/readout basis may enter only as a typed source factor with later dimensional closure",
            "admissible_handoff": "source_rule_morphology_factor",
            "block_condition": "posthoc morphology label switch or endpoint-selected source factor",
        },
        {
            "admissibility_id": "M0NDADM13_U_READ_MARKER_ADMISSIBILITY",
            "basis_id": "M0NDESB13_U_READ_ADMISSIBILITY_BASIS",
            "admissibility_class": "u_read_marker_admissibility",
            "admissibility_rule": "U_read may enter only as a finite-local dimensionless admissibility marker",
            "admissible_handoff": "source_rule_admissibility_marker",
            "block_condition": "attempt to use U_read as a fitted velocity scale or scalar family score",
        },
        {
            "admissibility_id": "M0NDADM13_BARYONIC_BINDING_ADMISSIBILITY",
            "basis_id": "M0NDESB13_BARYONIC_BINDING_BASIS",
            "admissibility_class": "baryonic_binding_admissibility",
            "admissibility_rule": "baryonic/source bindings may enter only with imported physical units preserved",
            "admissible_handoff": "source_rule_input_binding",
            "block_condition": "posthoc normalization, unit rescale, or residual-fitted baryonic correction",
        },
        {
            "admissibility_id": "M0NDADM13_FAILURE_ROUTE_ADMISSIBILITY",
            "basis_id": "M0NDESB13_FAILURE_ROUTE_BASIS",
            "admissibility_class": "failure_route_admissibility",
            "admissibility_rule": "failure-route basis may enter only as a blocked/null route for unresolved cases",
            "admissible_handoff": "null_fallback_policy_route",
            "block_condition": "attempt to replace a blocked route with endpoint-selected exception handling",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["admissibility_status"] = "READY"
        row["source_rule_claim_allowed"] = "false"
        row["expression_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_expression_admissibility_rule_only_no_source_rule_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["admissibility_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    return [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_ADMISSIBILITY_RULE_V13",
            "admissibility_artifact": "m0_no_dark_expression_admissibility_rule_v13",
            "source_basis_status": "READY" if source_basis_ready() else "BLOCKED",
            "admissibility_rows": len(rows),
            "ready_admissibility_rows": ready,
            "blocked_admissibility_rows": blocked,
            "source_rule_claim_allowed": "false",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_ADMISSIBILITY_RULE_READY"
            if blocked == 0 and source_basis_ready()
            else "M0_NO_DARK_EXPRESSION_ADMISSIBILITY_RULE_BLOCKED",
            "next_required_artifact": "m0_no_dark_expression_null_fallback_policy_v13",
            "claim_boundary": "m0_no_dark_expression_admissibility_rule_only_no_source_rule_no_formula_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_expression_admissibility_rule_v13.md").write_text(
        """# M0 No-Dark Expression Admissibility Rule v13

**Doc class:** no-dark M0 expression admissibility-rule record
**Status:** admissibility rule ready; null/fallback policy still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_expression_admissibility_rule.py
```

Derived outputs:

```text
data/derived/m0_no_dark_expression_admissibility_rule_v13.csv
data/derived/m0_no_dark_expression_admissibility_rule_summary_v13.csv
```

This artifact records which source-basis elements may pass into later no-dark
M0 source-rule construction. It is a source-side admissibility gate, not a
formula, fit, prediction, or endpoint score.

## Current Result

The expected status is:

```text
M0_NO_DARK_EXPRESSION_ADMISSIBILITY_RULE_READY
```

Six admissibility rows are ready:

- frozen source-domain admissibility;
- dimensionless no-dark constraint admissibility;
- morphology/readout factor admissibility;
- finite-local `U_read` marker admissibility;
- unit-preserving baryonic/source binding admissibility;
- blocked failure-route admissibility.

The next missing artifact is:

```text
m0_no_dark_expression_null_fallback_policy_v13
```

## Claim Boundary

This admissibility record does not define the M0 no-dark source rule, does not
define an expression, does not write a formula, does not compute predicted
velocities, does not score galaxies, and does not decide the dark-sector
question. It only authorizes the next source-side construction artifact: the
null/fallback policy.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = admissibility_rows()
    write_csv(DERIVED / "m0_no_dark_expression_admissibility_rule_v13.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_expression_admissibility_rule_summary_v13.csv",
        summary(rows),
        [
            "summary_id",
            "admissibility_artifact",
            "source_basis_status",
            "admissibility_rows",
            "ready_admissibility_rows",
            "blocked_admissibility_rows",
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
    print("PAPER11_M0_NO_DARK_EXPRESSION_ADMISSIBILITY_RULE_V13_BUILT")


if __name__ == "__main__":
    main()
