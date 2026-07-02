#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
NULL_FALLBACK_SUMMARY = DERIVED / "m0_no_dark_expression_null_fallback_policy_summary_v13.csv"


FIELDNAMES = [
    "output_class_id",
    "policy_id",
    "output_class",
    "output_role",
    "allowed_output",
    "blocked_output",
    "allowed_handoff",
    "forbidden_inputs",
    "output_class_status",
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


def null_fallback_ready() -> bool:
    if not NULL_FALLBACK_SUMMARY.exists():
        return False
    rows = read_csv(NULL_FALLBACK_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_EXPRESSION_NULL_FALLBACK_POLICY_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def output_class_rows() -> list[dict[str, object]]:
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_exception"
    rows = [
        {
            "output_class_id": "M0NDOC13_SOURCE_DOMAIN_OUTPUT_CLASS",
            "policy_id": "M0NDNFB13_SOURCE_FREEZE_NULL_POLICY",
            "output_class": "source_domain_evidence_state",
            "output_role": "declares whether the source-domain route is available, unresolved, or blocked",
            "allowed_output": "typed source-domain evidence state only",
            "blocked_output": "endpoint-filled source-domain value",
            "allowed_handoff": "source_rule_leakage_audit_source_domain_check",
        },
        {
            "output_class_id": "M0NDOC13_NO_DARK_CONSTRAINT_OUTPUT_CLASS",
            "policy_id": "M0NDNFB13_NO_DARK_CONSTRAINT_POLICY",
            "output_class": "no_dark_family_constraint_state",
            "output_role": "declares the M0 no-dark exclusion constraint as a family-level eligibility state",
            "allowed_output": "dimensionless M0 constraint marker",
            "blocked_output": "dark-response compensation term or fitted dark-sector substitute",
            "allowed_handoff": "source_rule_leakage_audit_family_constraint_check",
        },
        {
            "output_class_id": "M0NDOC13_MORPHOLOGY_FACTOR_OUTPUT_CLASS",
            "policy_id": "M0NDNFB13_MORPHOLOGY_LABEL_POLICY",
            "output_class": "typed_morphology_readout_factor",
            "output_role": "declares morphology/readout labels as typed factors rather than residual-selected scalars",
            "allowed_output": "predeclared morphology/readout factor class",
            "blocked_output": "post-hoc label switch after endpoint inspection",
            "allowed_handoff": "source_rule_leakage_audit_morphology_factor_check",
        },
        {
            "output_class_id": "M0NDOC13_U_READ_MARKER_OUTPUT_CLASS",
            "policy_id": "M0NDNFB13_U_READ_INCOMPARABILITY_POLICY",
            "output_class": "u_read_admissibility_marker",
            "output_role": "declares finite-local U_read as an admissibility marker, not a fitted endpoint score",
            "allowed_output": "non-scalar admissibility marker or incomparability marker",
            "blocked_output": "coerced scalar fitted from endpoint residuals",
            "allowed_handoff": "source_rule_leakage_audit_u_read_marker_check",
        },
        {
            "output_class_id": "M0NDOC13_BARYONIC_BINDING_OUTPUT_CLASS",
            "policy_id": "M0NDNFB13_BARYONIC_BINDING_POLICY",
            "output_class": "source_input_binding_state",
            "output_role": "declares whether baryonic/source inputs are bound with required unit and provenance discipline",
            "allowed_output": "source-side binding state with unresolved marker when needed",
            "blocked_output": "normalization repaired from best-fit curves",
            "allowed_handoff": "source_rule_leakage_audit_binding_check",
        },
        {
            "output_class_id": "M0NDOC13_FAILURE_ROUTE_OUTPUT_CLASS",
            "policy_id": "M0NDNFB13_FAILURE_ROUTE_POLICY",
            "output_class": "blocked_route_failure_marker",
            "output_role": "declares explicit failure routes that must dominate post-hoc exception creation",
            "allowed_output": "typed blocked-route marker",
            "blocked_output": "silent exception or endpoint-selected bypass",
            "allowed_handoff": "source_rule_leakage_audit_failure_route_check",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["output_class_status"] = "READY"
        row["source_rule_claim_allowed"] = "false"
        row["expression_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_expression_output_class_only_no_source_rule_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["output_class_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    return [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_OUTPUT_CLASS_V13",
            "output_class_artifact": "m0_no_dark_expression_output_class_v13",
            "null_fallback_status": "READY" if null_fallback_ready() else "BLOCKED",
            "output_class_rows": len(rows),
            "ready_output_class_rows": ready,
            "blocked_output_class_rows": blocked,
            "source_rule_claim_allowed": "false",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_OUTPUT_CLASS_READY"
            if blocked == 0 and null_fallback_ready()
            else "M0_NO_DARK_EXPRESSION_OUTPUT_CLASS_BLOCKED",
            "next_required_artifact": "m0_no_dark_expression_source_rule_leakage_audit_v13",
            "claim_boundary": "m0_no_dark_expression_output_class_only_no_source_rule_no_formula_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_expression_output_class_v13.md").write_text(
        """# M0 No-Dark Expression Output Class v13

**Doc class:** no-dark M0 expression output-class record
**Status:** output class ready; source-rule leakage audit still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_expression_output_class.py
```

Derived outputs:

```text
data/derived/m0_no_dark_expression_output_class_v13.csv
data/derived/m0_no_dark_expression_output_class_summary_v13.csv
```

This artifact declares what kind of object the M0 no-dark expression path may
hand forward after the null/fallback policy. It does not write the source rule
or formula. It only classifies allowed output shapes so the next audit can check
that the source rule is not selected from endpoint residuals.

## Current Result

The expected status is:

```text
M0_NO_DARK_EXPRESSION_OUTPUT_CLASS_READY
```

Six output classes are ready:

- source-domain evidence state;
- no-dark family constraint state;
- typed morphology/readout factor;
- finite-local `U_read` admissibility marker;
- source-input binding state;
- blocked-route failure marker.

The next missing artifact is:

```text
m0_no_dark_expression_source_rule_leakage_audit_v13
```

## Claim Boundary

This output-class record does not define the M0 no-dark source rule, does not
define an expression, does not write a formula, does not compute predicted
velocities, does not score galaxies, and does not decide the dark-sector
question. It only authorizes the next source-side construction artifact: the
source-rule leakage audit.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = output_class_rows()
    write_csv(DERIVED / "m0_no_dark_expression_output_class_v13.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_expression_output_class_summary_v13.csv",
        summary(rows),
        [
            "summary_id",
            "output_class_artifact",
            "null_fallback_status",
            "output_class_rows",
            "ready_output_class_rows",
            "blocked_output_class_rows",
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
    print("PAPER11_M0_NO_DARK_EXPRESSION_OUTPUT_CLASS_V13_BUILT")


if __name__ == "__main__":
    main()
