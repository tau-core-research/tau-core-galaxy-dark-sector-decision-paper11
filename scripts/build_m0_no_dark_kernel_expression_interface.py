#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
EQUATION_KERNEL_INTERFACE_SUMMARY = DERIVED / "m0_no_dark_equation_kernel_interface_summary_v09.csv"
FROZEN_EXPRESSION_CONTRACT_SUMMARY = DERIVED / "m0_no_dark_frozen_expression_contract_summary_v11.csv"


FIELDNAMES = [
    "expression_interface_id",
    "expression_slot_id",
    "interface_class",
    "interface_contract",
    "required_handoff",
    "blocked_behavior",
    "allowed_next_use",
    "forbidden_inputs",
    "interface_status",
    "expression_claim_allowed",
    "kernel_claim_allowed",
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


def equation_kernel_interface_ready() -> bool:
    if not EQUATION_KERNEL_INTERFACE_SUMMARY.exists():
        return False
    rows = read_csv(EQUATION_KERNEL_INTERFACE_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_EQUATION_KERNEL_INTERFACE_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def frozen_expression_contract_ready() -> bool:
    if not FROZEN_EXPRESSION_CONTRACT_SUMMARY.exists():
        return False
    rows = read_csv(FROZEN_EXPRESSION_CONTRACT_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_FROZEN_EXPRESSION_READY_FOR_PREDICTION_WRITER"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and rows[0]["frozen_expressions_written"] == "0"
    )


def interface_rows() -> list[dict[str, object]]:
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_expression_switch"
    rows = [
        {
            "expression_interface_id": "M0NDKEI10_VARIABLE_BINDINGS",
            "expression_slot_id": "M0NDKE10_VARIABLE_BINDINGS",
            "interface_class": "variable_binding_interface",
            "interface_contract": "kernel-expression symbols must bind to declared source-side and baryonic inputs without endpoint-selected variables",
            "required_handoff": "argument_signature_id;source_state_id;baryonic_input_id;radius_grid_id;symbol_table_id",
            "blocked_behavior": "add_symbol_after_endpoint_or_family_comparison",
            "allowed_next_use": "frozen_expression_payload_variable_binding_check",
        },
        {
            "expression_interface_id": "M0NDKEI10_CONSTANTS",
            "expression_slot_id": "M0NDKE10_CONSTANTS",
            "interface_class": "constant_declaration_interface",
            "interface_contract": "all constants and switches must be exposed with fixed/free status before any prediction writer runs",
            "required_handoff": "constant_slot_id;fixed_or_free_status;unit_id;parameter_count_guard_id",
            "blocked_behavior": "hide_or_discount_constants_after_family_winner",
            "allowed_next_use": "frozen_expression_payload_constant_check",
        },
        {
            "expression_interface_id": "M0NDKEI10_DIMENSIONAL_PATH",
            "expression_slot_id": "M0NDKE10_DIMENSIONAL_PATH",
            "interface_class": "dimensional_path_interface",
            "interface_contract": "payload must include a unit path to km/s without posthoc endpoint rescaling",
            "required_handoff": "input_unit_ids;operator_unit_ids;output_unit_target;unit_failure_state",
            "blocked_behavior": "posthoc_unit_rescale_or_endpoint_specific_unit_patch",
            "allowed_next_use": "frozen_expression_payload_dimensional_check",
        },
        {
            "expression_interface_id": "M0NDKEI10_SERIALIZED_FORM",
            "expression_slot_id": "M0NDKE10_SERIALIZED_FORM",
            "interface_class": "serialized_form_interface",
            "interface_contract": "payload must provide a machine-readable expression form before prediction rows can be written",
            "required_handoff": "serialization_format_id;symbol_table_id;domain_guard_id;prediction_writer_blocker_id",
            "blocked_behavior": "write_executable_prediction_callable_or_velocity_array",
            "allowed_next_use": "frozen_expression_payload_serialization_check",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["interface_status"] = "READY"
        row["expression_claim_allowed"] = "false"
        row["kernel_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_kernel_expression_interface_only_no_expression_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["interface_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    upstream_ready = equation_kernel_interface_ready() and frozen_expression_contract_ready()
    return [
        {
            "summary_id": "M0_NO_DARK_KERNEL_EXPRESSION_INTERFACE_V10",
            "interface_artifact": "m0_no_dark_kernel_expression_interface_v10",
            "equation_kernel_interface_status": "READY" if equation_kernel_interface_ready() else "BLOCKED",
            "frozen_expression_contract_status": "READY_CONTRACT_ONLY_NO_PAYLOAD"
            if frozen_expression_contract_ready()
            else "BLOCKED",
            "interface_rows": len(rows),
            "ready_interface_rows": ready,
            "blocked_interface_rows": blocked,
            "frozen_expression_payload_written": "false",
            "expression_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_KERNEL_EXPRESSION_INTERFACE_READY"
            if blocked == 0 and upstream_ready
            else "M0_NO_DARK_KERNEL_EXPRESSION_INTERFACE_BLOCKED",
            "next_required_artifact": "m0_no_dark_frozen_expression_payload_v11",
            "claim_boundary": "m0_no_dark_kernel_expression_interface_only_no_payload_no_predictions_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_kernel_expression_interface_v10.md").write_text(
        """# M0 No-Dark Kernel Expression Interface v10

**Doc class:** no-dark M0 kernel-expression interface contract
**Status:** interface ready; frozen expression payload still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_kernel_expression_interface.py
```

Derived outputs:

```text
data/derived/m0_no_dark_kernel_expression_interface_v10.csv
data/derived/m0_no_dark_kernel_expression_interface_summary_v10.csv
```

This artifact closes the non-payload interface slots of the M0 no-dark kernel
expression: variable bindings, constant exposure, dimensional path, and
serialized-form handoff.

## Current Result

The expected status is:

```text
M0_NO_DARK_KERNEL_EXPRESSION_INTERFACE_READY
```

The next required artifact is:

```text
m0_no_dark_frozen_expression_payload_v11
```

## Claim Boundary

This interface does not write the frozen expression payload, does not define a
velocity formula, does not assign numeric coefficients, does not write
prediction rows, and does not allow endpoint scoring. It only narrows the
kernel-expression blocker to the missing frozen-expression payload.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = interface_rows()
    write_csv(DERIVED / "m0_no_dark_kernel_expression_interface_v10.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_kernel_expression_interface_summary_v10.csv",
        summary(rows),
        [
            "summary_id",
            "interface_artifact",
            "equation_kernel_interface_status",
            "frozen_expression_contract_status",
            "interface_rows",
            "ready_interface_rows",
            "blocked_interface_rows",
            "frozen_expression_payload_written",
            "expression_claim_allowed",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_KERNEL_EXPRESSION_INTERFACE_V10_BUILT")


if __name__ == "__main__":
    main()
