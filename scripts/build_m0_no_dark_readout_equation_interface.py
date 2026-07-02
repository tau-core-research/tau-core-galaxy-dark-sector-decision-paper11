#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
FORMULA_BODY_INTERFACE_SUMMARY = DERIVED / "m0_no_dark_formula_body_interface_summary_v08.csv"


FIELDNAMES = [
    "readout_interface_id",
    "equation_slot_id",
    "interface_class",
    "interface_contract",
    "required_handoff",
    "blocked_behavior",
    "allowed_next_use",
    "forbidden_inputs",
    "interface_status",
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


def formula_body_interface_ready() -> bool:
    if not FORMULA_BODY_INTERFACE_SUMMARY.exists():
        return False
    rows = read_csv(FORMULA_BODY_INTERFACE_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_FORMULA_BODY_INTERFACE_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def interface_rows() -> list[dict[str, object]]:
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_equation_switch"
    rows = [
        {
            "readout_interface_id": "M0NDREI08_ARGUMENT_SIGNATURE",
            "equation_slot_id": "M0NDRE08_ARGUMENT_SIGNATURE",
            "interface_class": "argument_signature_interface",
            "interface_contract": "ordered source, baryonic, radial, scale, coefficient, and guard arguments are declared for the later kernel",
            "required_handoff": "source_state_id;baryonic_input_id;radius_grid_id;scale_slot_id;coefficient_slot_id;guard_id",
            "blocked_behavior": "add_or_reorder_arguments_after_endpoint_or_family_comparison",
            "allowed_next_use": "equation_kernel_input_binding_contract",
        },
        {
            "readout_interface_id": "M0NDREI08_UNITS",
            "equation_slot_id": "M0NDRE08_UNITS",
            "interface_class": "unit_target_interface",
            "interface_contract": "output target is declared as v_pred_km_s on the frozen radial grid, while the kernel must still prove the dimensional path",
            "required_handoff": "output_unit_target;radius_grid_unit;input_unit_guard;unit_failure_state",
            "blocked_behavior": "repair_units_by_posthoc_rescale_or_fit_quality",
            "allowed_next_use": "equation_kernel_output_map_and_unit_path_contract",
        },
        {
            "readout_interface_id": "M0NDREI08_PARAMETERS",
            "equation_slot_id": "M0NDRE08_PARAMETERS",
            "interface_class": "parameter_exposure_interface",
            "interface_contract": "all coefficient, switch, branch, and scale slots must be exposed for later parameter-count accounting",
            "required_handoff": "coefficient_slot_id;fixed_or_free_status;switch_slot_id;parameter_count_guard_id",
            "blocked_behavior": "hide_per_galaxy_privileges_or_discount_parameters_after_family_winner",
            "allowed_next_use": "equation_kernel_parameter_audit_contract",
        },
        {
            "readout_interface_id": "M0NDREI08_DOMAIN",
            "equation_slot_id": "M0NDRE08_DOMAIN",
            "interface_class": "domain_failure_interface",
            "interface_contract": "valid input domain, null/gauge branches, and invalid-input stop states are declared before kernel construction",
            "required_handoff": "valid_domain_id;null_state_id;gauge_state_id;failure_route_id;stop_condition",
            "blocked_behavior": "create_residual_specific_exception_or_rescue_branch",
            "allowed_next_use": "equation_kernel_failure_policy_contract",
        },
        {
            "readout_interface_id": "M0NDREI08_SERIALIZATION",
            "equation_slot_id": "M0NDRE08_SERIALIZATION",
            "interface_class": "serialization_interface",
            "interface_contract": "the later kernel must provide a machine-readable hook, but no executable prediction callable is written here",
            "required_handoff": "serialization_slot_id;argument_signature_id;output_unit_target;prediction_writer_blocker_id",
            "blocked_behavior": "write_prediction_callable_or_velocity_array",
            "allowed_next_use": "equation_kernel_reproducible_hook_contract",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["interface_status"] = "READY"
        row["equation_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_readout_equation_interface_only_no_kernel_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["interface_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    interface_ready = formula_body_interface_ready()
    return [
        {
            "summary_id": "M0_NO_DARK_READOUT_EQUATION_INTERFACE_V08",
            "interface_artifact": "m0_no_dark_readout_equation_interface_v08",
            "formula_body_interface_status": "READY" if interface_ready else "BLOCKED",
            "interface_rows": len(rows),
            "ready_interface_rows": ready,
            "blocked_interface_rows": blocked,
            "kernel_written": "false",
            "equation_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_READOUT_EQUATION_INTERFACE_READY"
            if blocked == 0 and interface_ready
            else "M0_NO_DARK_READOUT_EQUATION_INTERFACE_BLOCKED",
            "next_required_artifact": "m0_no_dark_equation_kernel_v09",
            "claim_boundary": "m0_no_dark_readout_equation_interface_only_no_kernel_no_predictions_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_readout_equation_interface_v08.md").write_text(
        """# M0 No-Dark Readout Equation Interface v08

**Doc class:** no-dark M0 readout-equation interface contract
**Status:** interface ready; equation kernel still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_readout_equation_interface.py
```

Derived outputs:

```text
data/derived/m0_no_dark_readout_equation_interface_v08.csv
data/derived/m0_no_dark_readout_equation_interface_summary_v08.csv
```

This artifact closes the non-kernel interface slots of the M0 no-dark readout
equation: argument signature, output-unit target, parameter exposure,
domain/failure behavior, and serialization handoff.

## Current Result

The expected status is:

```text
M0_NO_DARK_READOUT_EQUATION_INTERFACE_READY
```

The next required artifact is:

```text
m0_no_dark_equation_kernel_v09
```

## Claim Boundary

This interface does not write the equation kernel, does not define a velocity
formula, does not assign numeric coefficients, does not write prediction rows,
and does not allow endpoint scoring. It only narrows the readout-equation
blocker to the missing equation-kernel artifact.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = interface_rows()
    write_csv(DERIVED / "m0_no_dark_readout_equation_interface_v08.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_readout_equation_interface_summary_v08.csv",
        summary(rows),
        [
            "summary_id",
            "interface_artifact",
            "formula_body_interface_status",
            "interface_rows",
            "ready_interface_rows",
            "blocked_interface_rows",
            "kernel_written",
            "equation_claim_allowed",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_READOUT_EQUATION_INTERFACE_V08_BUILT")


if __name__ == "__main__":
    main()
