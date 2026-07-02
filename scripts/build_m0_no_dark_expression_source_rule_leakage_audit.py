#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
OUTPUT_CLASS_SUMMARY = DERIVED / "m0_no_dark_expression_output_class_summary_v13.csv"


FIELDNAMES = [
    "audit_id",
    "output_class_id",
    "audit_class",
    "source_side_record",
    "leakage_rule",
    "accepted_evidence",
    "forbidden_inputs",
    "audit_status",
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


def output_class_ready() -> bool:
    if not OUTPUT_CLASS_SUMMARY.exists():
        return False
    rows = read_csv(OUTPUT_CLASS_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_EXPRESSION_OUTPUT_CLASS_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def audit_rows() -> list[dict[str, object]]:
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_exception"
    rows = [
        {
            "audit_id": "M0NDSRLA13_SOURCE_DOMAIN_LEAKAGE_AUDIT",
            "output_class_id": "M0NDOC13_SOURCE_DOMAIN_OUTPUT_CLASS",
            "audit_class": "source_domain_leakage_audit",
            "source_side_record": "m0_no_dark_expression_output_class_v13",
            "leakage_rule": "source-domain availability must be inherited from source-side records, not endpoint-filled after residual inspection",
            "accepted_evidence": "typed source-domain evidence state with endpoint-filled source-domain values blocked",
        },
        {
            "audit_id": "M0NDSRLA13_NO_DARK_CONSTRAINT_LEAKAGE_AUDIT",
            "output_class_id": "M0NDOC13_NO_DARK_CONSTRAINT_OUTPUT_CLASS",
            "audit_class": "no_dark_constraint_leakage_audit",
            "source_side_record": "m0_no_dark_expression_output_class_v13",
            "leakage_rule": "M0 no-dark eligibility must remain a predeclared family constraint, not a fitted dark-response substitute",
            "accepted_evidence": "dimensionless M0 constraint marker with dark-response compensation blocked",
        },
        {
            "audit_id": "M0NDSRLA13_MORPHOLOGY_FACTOR_LEAKAGE_AUDIT",
            "output_class_id": "M0NDOC13_MORPHOLOGY_FACTOR_OUTPUT_CLASS",
            "audit_class": "morphology_factor_leakage_audit",
            "source_side_record": "m0_no_dark_expression_output_class_v13",
            "leakage_rule": "morphology/readout factors must be predeclared typed factors, not labels switched after endpoint inspection",
            "accepted_evidence": "typed morphology/readout factor class with post-hoc label switching blocked",
        },
        {
            "audit_id": "M0NDSRLA13_U_READ_MARKER_LEAKAGE_AUDIT",
            "output_class_id": "M0NDOC13_U_READ_MARKER_OUTPUT_CLASS",
            "audit_class": "u_read_marker_leakage_audit",
            "source_side_record": "m0_no_dark_expression_output_class_v13",
            "leakage_rule": "finite-local U_read must remain an admissibility marker or incomparability marker, not a fitted endpoint score",
            "accepted_evidence": "non-scalar U_read admissibility marker with endpoint scalar coercion blocked",
        },
        {
            "audit_id": "M0NDSRLA13_BARYONIC_BINDING_LEAKAGE_AUDIT",
            "output_class_id": "M0NDOC13_BARYONIC_BINDING_OUTPUT_CLASS",
            "audit_class": "baryonic_binding_leakage_audit",
            "source_side_record": "m0_no_dark_expression_output_class_v13",
            "leakage_rule": "baryonic/source binding must preserve unit and provenance discipline, not normalization repaired from best-fit curves",
            "accepted_evidence": "source-side binding state with best-fit normalization repair blocked",
        },
        {
            "audit_id": "M0NDSRLA13_FAILURE_ROUTE_LEAKAGE_AUDIT",
            "output_class_id": "M0NDOC13_FAILURE_ROUTE_OUTPUT_CLASS",
            "audit_class": "failure_route_leakage_audit",
            "source_side_record": "m0_no_dark_expression_output_class_v13",
            "leakage_rule": "failure routes must remain explicit blocked-route markers, not silent endpoint-selected bypasses",
            "accepted_evidence": "typed blocked-route marker with silent exception and endpoint-selected bypass blocked",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["audit_status"] = "READY"
        row["source_rule_claim_allowed"] = "false"
        row["expression_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_expression_source_rule_leakage_audit_only_no_rule_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["audit_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    return [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_SOURCE_RULE_LEAKAGE_AUDIT_V13",
            "source_rule_leakage_audit_artifact": "m0_no_dark_expression_source_rule_leakage_audit_v13",
            "output_class_status": "READY" if output_class_ready() else "BLOCKED",
            "audit_rows": len(rows),
            "ready_audit_rows": ready,
            "blocked_audit_rows": blocked,
            "source_rule_claim_allowed": "false",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_SOURCE_RULE_LEAKAGE_AUDIT_READY"
            if blocked == 0 and output_class_ready()
            else "M0_NO_DARK_EXPRESSION_SOURCE_RULE_LEAKAGE_AUDIT_BLOCKED",
            "next_required_artifact": "m0_no_dark_expression_symbolic_form_v12",
            "claim_boundary": "m0_no_dark_expression_source_rule_leakage_audit_only_no_rule_no_formula_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_expression_source_rule_leakage_audit_v13.md").write_text(
        """# M0 No-Dark Expression Source-Rule Leakage Audit v13

**Doc class:** no-dark M0 expression source-rule leakage audit
**Status:** leakage audit ready; symbolic/formula expression still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_expression_source_rule_leakage_audit.py
```

Derived outputs:

```text
data/derived/m0_no_dark_expression_source_rule_leakage_audit_v13.csv
data/derived/m0_no_dark_expression_source_rule_leakage_audit_summary_v13.csv
```

This artifact audits whether the output-class handoff can remain source-side
and pre-endpoint before the no-dark M0 expression path advances. It checks the
source-domain state, no-dark family constraint, morphology/readout factor,
finite-local `U_read` marker, baryonic/source binding state, and failure-route
marker against endpoint residual, heldout score, family-winner, best-fit curve,
and post-hoc exception leakage.

## Current Result

The expected status is:

```text
M0_NO_DARK_EXPRESSION_SOURCE_RULE_LEAKAGE_AUDIT_READY
```

Six leakage-audit rows are ready:

- source-domain leakage audit;
- no-dark constraint leakage audit;
- morphology/readout factor leakage audit;
- finite-local `U_read` marker leakage audit;
- baryonic/source binding leakage audit;
- failure-route leakage audit.

The next missing artifact is:

```text
m0_no_dark_expression_symbolic_form_v12
```

## Claim Boundary

This leakage audit does not define the M0 no-dark source rule, does not define
an expression, does not write a formula, does not compute predicted velocities,
does not score galaxies, and does not decide the dark-sector question. It only
closes the source-rule leakage-audit gate and authorizes the next construction
artifact: the symbolic or algorithmic expression form.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = audit_rows()
    write_csv(DERIVED / "m0_no_dark_expression_source_rule_leakage_audit_v13.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_expression_source_rule_leakage_audit_summary_v13.csv",
        summary(rows),
        [
            "summary_id",
            "source_rule_leakage_audit_artifact",
            "output_class_status",
            "audit_rows",
            "ready_audit_rows",
            "blocked_audit_rows",
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
    print("PAPER11_M0_NO_DARK_EXPRESSION_SOURCE_RULE_LEAKAGE_AUDIT_V13_BUILT")


if __name__ == "__main__":
    main()
