#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
READOUT_INTERFACE_SUMMARY = DERIVED / "m0_no_dark_readout_equation_interface_summary_v08.csv"


FIELDNAMES = [
    "kernel_interface_id",
    "kernel_slot_id",
    "interface_class",
    "interface_contract",
    "required_handoff",
    "blocked_behavior",
    "allowed_next_use",
    "forbidden_inputs",
    "interface_status",
    "kernel_claim_allowed",
    "equation_claim_allowed",
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


def readout_interface_ready() -> bool:
    if not READOUT_INTERFACE_SUMMARY.exists():
        return False
    rows = read_csv(READOUT_INTERFACE_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_READOUT_EQUATION_INTERFACE_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def interface_rows() -> list[dict[str, object]]:
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_kernel_switch"
    rows = [
        {
            "kernel_interface_id": "M0NDEKI09_INPUT_BINDING",
            "kernel_slot_id": "M0NDEK09_INPUT_BINDING",
            "interface_class": "input_binding_interface",
            "interface_contract": "declared readout-equation arguments are bound to later kernel variables without adding endpoint-selected variables",
            "required_handoff": "argument_signature_id;source_state_id;baryonic_input_id;radius_grid_id;guard_id",
            "blocked_behavior": "add_kernel_variable_after_endpoint_or_family_comparison",
            "allowed_next_use": "kernel_expression_variable_binding_contract",
        },
        {
            "kernel_interface_id": "M0NDEKI09_OUTPUT_MAP",
            "kernel_slot_id": "M0NDEK09_OUTPUT_MAP",
            "interface_class": "output_map_interface",
            "interface_contract": "kernel output target and frozen radial-grid row mapping are declared without producing v_pred_km_s values",
            "required_handoff": "output_unit_target;radius_grid_id;row_mapping_id;unit_failure_state",
            "blocked_behavior": "write_prediction_rows_or_posthoc_unit_rescale",
            "allowed_next_use": "kernel_expression_output_map_contract",
        },
        {
            "kernel_interface_id": "M0NDEKI09_PARAMETER_AUDIT",
            "kernel_slot_id": "M0NDEK09_PARAMETER_AUDIT",
            "interface_class": "parameter_audit_interface",
            "interface_contract": "coefficient, switch, branch, and scale slots are exposed for later parameter counting without values",
            "required_handoff": "coefficient_slot_id;switch_slot_id;branch_slot_id;parameter_count_guard_id",
            "blocked_behavior": "hide_or_discount_parameters_after_family_winner",
            "allowed_next_use": "kernel_expression_parameter_audit_contract",
        },
        {
            "kernel_interface_id": "M0NDEKI09_FAILURE_POLICY",
            "kernel_slot_id": "M0NDEK09_FAILURE_POLICY",
            "interface_class": "failure_policy_interface",
            "interface_contract": "invalid-input, missing-source, null/gauge, and zero-response routes are stop states, not rescue terms",
            "required_handoff": "valid_domain_id;failure_route_id;null_state_id;gauge_state_id;stop_condition",
            "blocked_behavior": "create_residual_specific_exception_or_rescue_term",
            "allowed_next_use": "kernel_expression_failure_policy_contract",
        },
        {
            "kernel_interface_id": "M0NDEKI09_REPRODUCIBLE_HOOK",
            "kernel_slot_id": "M0NDEK09_REPRODUCIBLE_HOOK",
            "interface_class": "reproducible_hook_interface",
            "interface_contract": "later kernel expression must provide a reproducible hook, but no executable prediction hook is written here",
            "required_handoff": "serialization_slot_id;argument_signature_id;output_unit_target;prediction_writer_blocker_id",
            "blocked_behavior": "write_executable_prediction_callable_or_velocity_array",
            "allowed_next_use": "kernel_expression_serialization_contract",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["interface_status"] = "READY"
        row["kernel_claim_allowed"] = "false"
        row["equation_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_equation_kernel_interface_only_no_expression_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["interface_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    readout_ready = readout_interface_ready()
    return [
        {
            "summary_id": "M0_NO_DARK_EQUATION_KERNEL_INTERFACE_V09",
            "interface_artifact": "m0_no_dark_equation_kernel_interface_v09",
            "readout_equation_interface_status": "READY" if readout_ready else "BLOCKED",
            "interface_rows": len(rows),
            "ready_interface_rows": ready,
            "blocked_interface_rows": blocked,
            "kernel_expression_written": "false",
            "kernel_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EQUATION_KERNEL_INTERFACE_READY"
            if blocked == 0 and readout_ready
            else "M0_NO_DARK_EQUATION_KERNEL_INTERFACE_BLOCKED",
            "next_required_artifact": "m0_no_dark_kernel_expression_v10",
            "claim_boundary": "m0_no_dark_equation_kernel_interface_only_no_expression_no_predictions_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_equation_kernel_interface_v09.md").write_text(
        """# M0 No-Dark Equation Kernel Interface v09

**Doc class:** no-dark M0 equation-kernel interface contract
**Status:** interface ready; kernel expression still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_equation_kernel_interface.py
```

Derived outputs:

```text
data/derived/m0_no_dark_equation_kernel_interface_v09.csv
data/derived/m0_no_dark_equation_kernel_interface_summary_v09.csv
```

This artifact closes the non-expression interface slots of the M0 no-dark
equation kernel: input binding, output mapping, parameter audit, failure
policy, and reproducible-hook handoff.

## Current Result

The expected status is:

```text
M0_NO_DARK_EQUATION_KERNEL_INTERFACE_READY
```

The next required artifact is:

```text
m0_no_dark_kernel_expression_v10
```

## Claim Boundary

This interface does not write the kernel expression, does not define a velocity
formula, does not assign numeric coefficients, does not write prediction rows,
and does not allow endpoint scoring. It only narrows the equation-kernel blocker
to the missing kernel-expression artifact.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = interface_rows()
    write_csv(DERIVED / "m0_no_dark_equation_kernel_interface_v09.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_equation_kernel_interface_summary_v09.csv",
        summary(rows),
        [
            "summary_id",
            "interface_artifact",
            "readout_equation_interface_status",
            "interface_rows",
            "ready_interface_rows",
            "blocked_interface_rows",
            "kernel_expression_written",
            "kernel_claim_allowed",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_EQUATION_KERNEL_INTERFACE_V09_BUILT")


if __name__ == "__main__":
    main()
