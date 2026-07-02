#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
COEFFICIENT_FREEZE_SUMMARY = DERIVED / "m0_no_dark_expression_coefficient_freeze_summary_v12.csv"


FIELDNAMES = [
    "dimensional_audit_id",
    "coefficient_policy_id",
    "unit_route_class",
    "required_unit_route",
    "audit_rule",
    "blocked_route",
    "allowed_handoff",
    "forbidden_inputs",
    "dimensional_audit_status",
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


def coefficient_freeze_ready() -> bool:
    if not COEFFICIENT_FREEZE_SUMMARY.exists():
        return False
    rows = read_csv(COEFFICIENT_FREEZE_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_EXPRESSION_COEFFICIENT_FREEZE_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def dimensional_rows() -> list[dict[str, object]]:
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_unit_rescale"
    rows = [
        {
            "dimensional_audit_id": "M0NDDA12_SOURCE_STATE_UNIT_AUDIT",
            "coefficient_policy_id": "M0NDCF12_SOURCE_STATE_COEFFICIENT_POLICY",
            "unit_route_class": "source_state_unit_route",
            "required_unit_route": "source-state and morphology/readout markers remain typed state variables unless a later formula declares a lawful coupling",
            "audit_rule": "unit-free markers cannot be silently reinterpreted as velocity, mass, or acceleration units",
            "blocked_route": "unit-bearing source-state correction inferred from endpoint residuals",
            "allowed_handoff": "machine_form_source_state_unit_guard",
        },
        {
            "dimensional_audit_id": "M0NDDA12_NO_DARK_CONSTRAINT_UNIT_AUDIT",
            "coefficient_policy_id": "M0NDCF12_NO_DARK_CONSTRAINT_COEFFICIENT_POLICY",
            "unit_route_class": "no_dark_constraint_unit_route",
            "required_unit_route": "no-dark constraint remains dimensionless and cannot carry compensating response units",
            "audit_rule": "M0 eligibility cannot introduce hidden density, acceleration, or potential units",
            "blocked_route": "dark-response-like unitful compensator inside the no-dark route",
            "allowed_handoff": "machine_form_no_dark_unit_guard",
        },
        {
            "dimensional_audit_id": "M0NDDA12_BARYONIC_INPUT_UNIT_AUDIT",
            "coefficient_policy_id": "M0NDCF12_BARYONIC_INPUT_COEFFICIENT_POLICY",
            "unit_route_class": "baryonic_input_unit_route",
            "required_unit_route": "baryonic/source inputs preserve imported physical units and unresolved units remain explicit null states",
            "audit_rule": "missing units cannot be repaired from best-fit curves or endpoint residuals",
            "blocked_route": "posthoc baryonic normalization or unit rescale",
            "allowed_handoff": "machine_form_baryonic_unit_guard",
        },
        {
            "dimensional_audit_id": "M0NDDA12_READOUT_OPERATOR_UNIT_AUDIT",
            "coefficient_policy_id": "M0NDCF12_READOUT_OPERATOR_COEFFICIENT_POLICY",
            "unit_route_class": "readout_operator_unit_route",
            "required_unit_route": "readout operator must expose any unit-bearing amplitude, scale, threshold, or kernel-shape role before formula work",
            "audit_rule": "operator units cannot be selected by heldout score or family winner",
            "blocked_route": "readout-unit conversion selected after endpoint inspection",
            "allowed_handoff": "machine_form_readout_unit_guard",
        },
        {
            "dimensional_audit_id": "M0NDDA12_FAILURE_ROUTE_UNIT_AUDIT",
            "coefficient_policy_id": "M0NDCF12_FAILURE_ROUTE_COEFFICIENT_POLICY",
            "unit_route_class": "failure_route_unit_route",
            "required_unit_route": "blocked, null, gauge, and unresolved routes cannot emit unit-bearing rescue terms",
            "audit_rule": "failure markers must stop construction rather than create dimensional patches",
            "blocked_route": "residual-specific rescue term or silent unit exception",
            "allowed_handoff": "machine_form_failure_unit_guard",
        },
        {
            "dimensional_audit_id": "M0NDDA12_ASSEMBLY_UNIT_AUDIT",
            "coefficient_policy_id": "M0NDCF12_ASSEMBLY_COEFFICIENT_POLICY",
            "unit_route_class": "assembly_unit_route",
            "required_unit_route": "assembly shell must expose the intended output-unit contract before machine form, without computing velocities",
            "audit_rule": "a future velocity-output formula must pass an explicit unit path; this artifact does not provide that formula",
            "blocked_route": "complete prediction callable or velocity formula without unit audit",
            "allowed_handoff": "machine_form_assembly_unit_guard",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["dimensional_audit_status"] = "READY"
        row["expression_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_expression_dimensional_audit_only_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["dimensional_audit_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    return [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_DIMENSIONAL_AUDIT_V12",
            "dimensional_audit_artifact": "m0_no_dark_expression_dimensional_audit_v12",
            "coefficient_freeze_status": "READY" if coefficient_freeze_ready() else "BLOCKED",
            "dimensional_audit_rows": len(rows),
            "ready_dimensional_audit_rows": ready,
            "blocked_dimensional_audit_rows": blocked,
            "velocity_formula_written": "false",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_DIMENSIONAL_AUDIT_READY"
            if blocked == 0 and coefficient_freeze_ready()
            else "M0_NO_DARK_EXPRESSION_DIMENSIONAL_AUDIT_BLOCKED",
            "next_required_artifact": "m0_no_dark_expression_machine_form_v12",
            "claim_boundary": "m0_no_dark_expression_dimensional_audit_only_no_formula_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_expression_dimensional_audit_v12.md").write_text(
        """# M0 No-Dark Expression Dimensional Audit v12

**Doc class:** no-dark M0 expression dimensional-audit record
**Status:** dimensional audit ready; machine form still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_expression_dimensional_audit.py
```

Derived outputs:

```text
data/derived/m0_no_dark_expression_dimensional_audit_v12.csv
data/derived/m0_no_dark_expression_dimensional_audit_summary_v12.csv
```

This artifact audits the unit-route discipline required before the M0 no-dark
expression can be serialized. It blocks post-hoc unit rescaling, hidden
dark-response-like units, endpoint-repaired baryonic normalizations, and
unit-bearing rescue terms.

## Current Result

The expected status is:

```text
M0_NO_DARK_EXPRESSION_DIMENSIONAL_AUDIT_READY
```

Six dimensional-audit rows are ready:

- source-state unit audit;
- no-dark constraint unit audit;
- baryonic/source input unit audit;
- readout-operator unit audit;
- failure-route unit audit;
- assembly unit audit.

The next missing artifact is:

```text
m0_no_dark_expression_machine_form_v12
```

## Claim Boundary

This dimensional audit does not define a complete expression, does not write a
velocity formula, does not assign numeric coefficients, does not compute
predicted velocities, does not score galaxies, and does not decide the
dark-sector question. It only authorizes the next construction artifact:
machine-form serialization.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = dimensional_rows()
    write_csv(DERIVED / "m0_no_dark_expression_dimensional_audit_v12.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_expression_dimensional_audit_summary_v12.csv",
        summary(rows),
        [
            "summary_id",
            "dimensional_audit_artifact",
            "coefficient_freeze_status",
            "dimensional_audit_rows",
            "ready_dimensional_audit_rows",
            "blocked_dimensional_audit_rows",
            "velocity_formula_written",
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
    print("PAPER11_M0_NO_DARK_EXPRESSION_DIMENSIONAL_AUDIT_V12_BUILT")


if __name__ == "__main__":
    main()
