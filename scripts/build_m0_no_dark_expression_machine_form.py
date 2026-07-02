#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
DIMENSIONAL_AUDIT_SUMMARY = DERIVED / "m0_no_dark_expression_dimensional_audit_summary_v12.csv"


FIELDNAMES = [
    "machine_form_id",
    "dimensional_audit_id",
    "serialization_class",
    "serialized_contract",
    "required_fields",
    "blocked_runtime_behavior",
    "allowed_handoff",
    "forbidden_inputs",
    "machine_form_status",
    "frozen_expression_claim_allowed",
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


def dimensional_audit_ready() -> bool:
    if not DIMENSIONAL_AUDIT_SUMMARY.exists():
        return False
    rows = read_csv(DIMENSIONAL_AUDIT_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_EXPRESSION_DIMENSIONAL_AUDIT_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def machine_form_rows() -> list[dict[str, object]]:
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_callable_switch"
    rows = [
        {
            "machine_form_id": "M0NDMF12_SOURCE_STATE_SERIALIZATION",
            "dimensional_audit_id": "M0NDDA12_SOURCE_STATE_UNIT_AUDIT",
            "serialization_class": "source_state_serialization",
            "serialized_contract": "typed source-state and morphology/readout markers are serialized as named inputs, not inferred response terms",
            "required_fields": "source_state_id;source_route_id;morphology_marker_id;readout_marker_id;unit_guard_id",
            "blocked_runtime_behavior": "derive_source_state_correction_from_endpoint_residual",
            "allowed_handoff": "formula_body_source_state_argument_contract",
        },
        {
            "machine_form_id": "M0NDMF12_NO_DARK_CONSTRAINT_SERIALIZATION",
            "dimensional_audit_id": "M0NDDA12_NO_DARK_CONSTRAINT_UNIT_AUDIT",
            "serialization_class": "no_dark_constraint_serialization",
            "serialized_contract": "no-dark eligibility is serialized as a dimensionless constraint flag and cannot host hidden dark-response terms",
            "required_fields": "m0_family_id;no_dark_constraint_id;eligibility_status;constraint_guard_id",
            "blocked_runtime_behavior": "inject_hidden_density_acceleration_or_potential_compensator",
            "allowed_handoff": "formula_body_no_dark_constraint_guard",
        },
        {
            "machine_form_id": "M0NDMF12_BARYONIC_INPUT_SERIALIZATION",
            "dimensional_audit_id": "M0NDDA12_BARYONIC_INPUT_UNIT_AUDIT",
            "serialization_class": "baryonic_input_serialization",
            "serialized_contract": "baryonic/source inputs keep imported units and unresolved units remain explicit null states",
            "required_fields": "baryonic_input_id;radius_grid_id;unit_status;null_state_id;provenance_guard_id",
            "blocked_runtime_behavior": "repair_missing_units_from_best_fit_or_endpoint_residual",
            "allowed_handoff": "formula_body_baryonic_argument_contract",
        },
        {
            "machine_form_id": "M0NDMF12_READOUT_OPERATOR_SERIALIZATION",
            "dimensional_audit_id": "M0NDDA12_READOUT_OPERATOR_UNIT_AUDIT",
            "serialization_class": "readout_operator_serialization",
            "serialized_contract": "readout-operator roles are serialized as named slots whose unit-bearing amplitudes or thresholds must be declared later before use",
            "required_fields": "operator_slot_id;operator_role;unit_role_status;coefficient_policy_id;selection_guard_id",
            "blocked_runtime_behavior": "select_operator_units_from_heldout_score_or_family_winner",
            "allowed_handoff": "formula_body_readout_operator_slot_contract",
        },
        {
            "machine_form_id": "M0NDMF12_FAILURE_ROUTE_SERIALIZATION",
            "dimensional_audit_id": "M0NDDA12_FAILURE_ROUTE_UNIT_AUDIT",
            "serialization_class": "failure_route_serialization",
            "serialized_contract": "blocked, null, gauge, and unresolved routes are serialized as stop states rather than rescue terms",
            "required_fields": "failure_route_id;null_or_gauge_status;stop_condition;downstream_blocker_id",
            "blocked_runtime_behavior": "emit_unit_bearing_rescue_term_or_silent_exception",
            "allowed_handoff": "formula_body_fallback_branch_contract",
        },
        {
            "machine_form_id": "M0NDMF12_ASSEMBLY_SERIALIZATION",
            "dimensional_audit_id": "M0NDDA12_ASSEMBLY_UNIT_AUDIT",
            "serialization_class": "assembly_serialization",
            "serialized_contract": "assembly shell exposes argument order, output-unit target, and guards without computing v_pred_km_s",
            "required_fields": "assembly_id;argument_signature_id;output_unit_target;guard_order;prediction_writer_blocker_id",
            "blocked_runtime_behavior": "produce_velocity_formula_or_prediction_array",
            "allowed_handoff": "formula_body_assembly_contract",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["machine_form_status"] = "READY"
        row["frozen_expression_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_expression_machine_form_only_serialization_contract_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["machine_form_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    audit_ready = dimensional_audit_ready()
    return [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_MACHINE_FORM_V12",
            "machine_form_artifact": "m0_no_dark_expression_machine_form_v12",
            "dimensional_audit_status": "READY" if audit_ready else "BLOCKED",
            "machine_form_rows": len(rows),
            "ready_machine_form_rows": ready,
            "blocked_machine_form_rows": blocked,
            "serialized_prediction_callable_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_MACHINE_FORM_READY"
            if blocked == 0 and audit_ready
            else "M0_NO_DARK_EXPRESSION_MACHINE_FORM_BLOCKED",
            "next_required_artifact": "family_prediction_tables_v08.csv",
            "claim_boundary": "m0_no_dark_expression_machine_form_only_serialization_contract_no_formula_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_expression_machine_form_v12.md").write_text(
        """# M0 No-Dark Expression Machine Form v12

**Doc class:** no-dark M0 expression machine-form serialization contract
**Status:** machine form ready; formula and scoring still blocked

Script:

```text
scripts/build_m0_no_dark_expression_machine_form.py
```

Derived outputs:

```text
data/derived/m0_no_dark_expression_machine_form_v12.csv
data/derived/m0_no_dark_expression_machine_form_summary_v12.csv
```

This artifact serializes the source-side M0 no-dark expression contract into
machine-readable slots that a later formula-body writer can consume. It records
source-state, no-dark constraint, baryonic-input, readout-operator,
failure-route, and assembly contracts.

## Current Result

The expected status is:

```text
M0_NO_DARK_EXPRESSION_MACHINE_FORM_READY
```

Six machine-form rows are ready:

- source-state serialization;
- no-dark constraint serialization;
- baryonic/source input serialization;
- readout-operator serialization;
- failure-route serialization;
- assembly serialization.

The next required artifact is:

```text
family_prediction_tables_v08.csv
```

## Claim Boundary

This machine form is not a velocity formula, not a callable prediction engine,
not a fitted response model, and not an endpoint score. It does not decide the
dark-sector question. It only closes the serialization slot of the M0 no-dark
frozen-expression contract and hands the remaining work to formula/prediction
table construction.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = machine_form_rows()
    write_csv(DERIVED / "m0_no_dark_expression_machine_form_v12.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_expression_machine_form_summary_v12.csv",
        summary(rows),
        [
            "summary_id",
            "machine_form_artifact",
            "dimensional_audit_status",
            "machine_form_rows",
            "ready_machine_form_rows",
            "blocked_machine_form_rows",
            "serialized_prediction_callable_written",
            "formula_claim_allowed",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_EXPRESSION_MACHINE_FORM_V12_BUILT")


if __name__ == "__main__":
    main()
