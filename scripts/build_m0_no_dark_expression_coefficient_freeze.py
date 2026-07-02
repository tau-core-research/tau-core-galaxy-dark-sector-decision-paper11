#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
INPUT_DOMAIN_SUMMARY = DERIVED / "m0_no_dark_expression_input_domain_summary_v12.csv"


FIELDNAMES = [
    "coefficient_policy_id",
    "input_domain_id",
    "coefficient_class",
    "freeze_policy",
    "count_policy",
    "allowed_state",
    "blocked_state",
    "allowed_handoff",
    "forbidden_inputs",
    "coefficient_policy_status",
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


def input_domain_ready() -> bool:
    if not INPUT_DOMAIN_SUMMARY.exists():
        return False
    rows = read_csv(INPUT_DOMAIN_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_EXPRESSION_INPUT_DOMAIN_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def coefficient_rows() -> list[dict[str, object]]:
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_parameter_discount"
    rows = [
        {
            "coefficient_policy_id": "M0NDCF12_SOURCE_STATE_COEFFICIENT_POLICY",
            "input_domain_id": "M0NDID12_SOURCE_STATE_DOMAIN",
            "coefficient_class": "source_state_coefficient_scope",
            "freeze_policy": "source-state coefficients or switches must be declared before prediction writing",
            "count_policy": "any adjustable source-state coefficient or post-freeze morphology switch counts",
            "allowed_state": "predeclared coefficient slot or explicit no-coefficient marker",
            "blocked_state": "coefficient or switch chosen after endpoint residual inspection",
            "allowed_handoff": "dimensional_audit_source_state_scope",
        },
        {
            "coefficient_policy_id": "M0NDCF12_NO_DARK_CONSTRAINT_COEFFICIENT_POLICY",
            "input_domain_id": "M0NDID12_NO_DARK_CONSTRAINT_DOMAIN",
            "coefficient_class": "no_dark_constraint_coefficient_scope",
            "freeze_policy": "no-dark eligibility marker carries no hidden compensator coefficient",
            "count_policy": "any compensating dark-response-like coefficient disqualifies M0 or counts as non-M0 privilege",
            "allowed_state": "dimensionless fixed family-eligibility marker",
            "blocked_state": "hidden dark-sector amplitude, scale, or response coefficient",
            "allowed_handoff": "dimensional_audit_no_dark_constraint_scope",
        },
        {
            "coefficient_policy_id": "M0NDCF12_BARYONIC_INPUT_COEFFICIENT_POLICY",
            "input_domain_id": "M0NDID12_BARYONIC_INPUT_DOMAIN",
            "coefficient_class": "baryonic_input_coefficient_scope",
            "freeze_policy": "baryonic normalization and unit choices must be source-side or counted",
            "count_policy": "any adjustable baryonic normalization, scale, or mass-model privilege counts",
            "allowed_state": "source-side binding state with coefficient slot exposed when adjustable",
            "blocked_state": "best-fit normalization hidden inside source binding",
            "allowed_handoff": "dimensional_audit_baryonic_scope",
        },
        {
            "coefficient_policy_id": "M0NDCF12_READOUT_OPERATOR_COEFFICIENT_POLICY",
            "input_domain_id": "M0NDID12_READOUT_OPERATOR_DOMAIN",
            "coefficient_class": "readout_operator_coefficient_scope",
            "freeze_policy": "readout operator coefficients, thresholds, or scales must be exposed before scoring",
            "count_policy": "any adjustable readout amplitude, radial scale, threshold, or kernel-shape parameter counts",
            "allowed_state": "predeclared operator coefficient slot or fixed symbolic marker",
            "blocked_state": "operator parameter chosen by heldout score or family winner",
            "allowed_handoff": "dimensional_audit_readout_scope",
        },
        {
            "coefficient_policy_id": "M0NDCF12_FAILURE_ROUTE_COEFFICIENT_POLICY",
            "input_domain_id": "M0NDID12_FAILURE_ROUTE_DOMAIN",
            "coefficient_class": "failure_route_coefficient_scope",
            "freeze_policy": "failure routes cannot create uncounted rescue coefficients",
            "count_policy": "any per-galaxy exception or failure-route rescue parameter counts at full weight",
            "allowed_state": "explicit blocked/null/failure marker",
            "blocked_state": "silent exception coefficient or residual-specific rescue term",
            "allowed_handoff": "dimensional_audit_failure_scope",
        },
        {
            "coefficient_policy_id": "M0NDCF12_ASSEMBLY_COEFFICIENT_POLICY",
            "input_domain_id": "M0NDID12_FORM_ASSEMBLY_DOMAIN",
            "coefficient_class": "assembly_coefficient_scope",
            "freeze_policy": "assembly-level coefficient inventory must be visible before formula, machine form, or scoring",
            "count_policy": "all adjustable coefficients, scales, switches, and per-galaxy privileges must be counted; numeric counts remain pending",
            "allowed_state": "coefficient inventory shell with no numeric values",
            "blocked_state": "complete fitted formula or discounted parameter count",
            "allowed_handoff": "dimensional_audit_assembly_scope",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["coefficient_policy_status"] = "READY"
        row["expression_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_expression_coefficient_freeze_only_policy_no_values_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["coefficient_policy_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    return [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_COEFFICIENT_FREEZE_V12",
            "coefficient_freeze_artifact": "m0_no_dark_expression_coefficient_freeze_v12",
            "input_domain_status": "READY" if input_domain_ready() else "BLOCKED",
            "coefficient_policy_rows": len(rows),
            "ready_coefficient_policy_rows": ready,
            "blocked_coefficient_policy_rows": blocked,
            "numeric_coefficient_values_written": 0,
            "numeric_parameter_counts_written": 0,
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_COEFFICIENT_FREEZE_READY"
            if blocked == 0 and input_domain_ready()
            else "M0_NO_DARK_EXPRESSION_COEFFICIENT_FREEZE_BLOCKED",
            "next_required_artifact": "m0_no_dark_expression_dimensional_audit_v12",
            "claim_boundary": "m0_no_dark_expression_coefficient_freeze_only_policy_no_values_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_expression_coefficient_freeze_v12.md").write_text(
        """# M0 No-Dark Expression Coefficient Freeze v12

**Doc class:** no-dark M0 expression coefficient-freeze policy
**Status:** coefficient policy ready; dimensional audit still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_expression_coefficient_freeze.py
```

Derived outputs:

```text
data/derived/m0_no_dark_expression_coefficient_freeze_v12.csv
data/derived/m0_no_dark_expression_coefficient_freeze_summary_v12.csv
```

This artifact freezes the coefficient policy for the M0 no-dark expression
path. It does not provide numeric coefficient values and does not provide final
numeric parameter counts. It only states what later artifacts must expose and
count before any prediction or scoring can be written.

## Current Result

The expected status is:

```text
M0_NO_DARK_EXPRESSION_COEFFICIENT_FREEZE_READY
```

Six coefficient-policy rows are ready:

- source-state coefficient scope;
- no-dark constraint coefficient scope;
- baryonic/source input coefficient scope;
- readout-operator coefficient scope;
- failure-route coefficient scope;
- assembly coefficient inventory scope.

The next missing artifact is:

```text
m0_no_dark_expression_dimensional_audit_v12
```

## Claim Boundary

This coefficient-freeze policy does not define a complete expression, does not
write a formula, does not assign numeric coefficients, does not compute
predicted velocities, does not score galaxies, and does not decide the
dark-sector question. It only authorizes the next construction artifact:
dimensional audit.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = coefficient_rows()
    write_csv(DERIVED / "m0_no_dark_expression_coefficient_freeze_v12.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_expression_coefficient_freeze_summary_v12.csv",
        summary(rows),
        [
            "summary_id",
            "coefficient_freeze_artifact",
            "input_domain_status",
            "coefficient_policy_rows",
            "ready_coefficient_policy_rows",
            "blocked_coefficient_policy_rows",
            "numeric_coefficient_values_written",
            "numeric_parameter_counts_written",
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
    print("PAPER11_M0_NO_DARK_EXPRESSION_COEFFICIENT_FREEZE_V12_BUILT")


if __name__ == "__main__":
    main()
