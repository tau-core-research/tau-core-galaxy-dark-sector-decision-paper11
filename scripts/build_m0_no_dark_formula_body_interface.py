#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
MACHINE_FORM_SUMMARY = DERIVED / "m0_no_dark_expression_machine_form_summary_v12.csv"


FIELDNAMES = [
    "interface_slot_id",
    "body_slot_id",
    "interface_class",
    "interface_contract",
    "required_handoff",
    "blocked_behavior",
    "allowed_next_use",
    "forbidden_inputs",
    "interface_status",
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


def machine_form_ready() -> bool:
    if not MACHINE_FORM_SUMMARY.exists():
        return False
    rows = read_csv(MACHINE_FORM_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_EXPRESSION_MACHINE_FORM_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def interface_rows() -> list[dict[str, object]]:
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_formula_switch"
    rows = [
        {
            "interface_slot_id": "M0NDBI08_SOURCE_ARGUMENTS",
            "body_slot_id": "M0NDB07_SOURCE_ARGUMENTS",
            "interface_class": "source_argument_interface",
            "interface_contract": "source-state, morphology/readout, null, and guard arguments are admitted only through the machine-form slots",
            "required_handoff": "source_state_id;source_route_id;morphology_marker_id;readout_marker_id;guard_id",
            "blocked_behavior": "add_source_argument_after_endpoint_residual_or_family_winner",
            "allowed_next_use": "readout_equation_argument_signature",
        },
        {
            "interface_slot_id": "M0NDBI08_BARYONIC_HANDOFF",
            "body_slot_id": "M0NDB07_BARYONIC_HANDOFF",
            "interface_class": "baryonic_handoff_interface",
            "interface_contract": "shared baryonic/radial inputs are passed as imported inputs with explicit unit and null-state guards",
            "required_handoff": "baryonic_input_id;radius_grid_id;unit_status;null_state_id",
            "blocked_behavior": "repair_baryonic_units_or_normalization_from_fit_quality",
            "allowed_next_use": "readout_equation_baryonic_argument_signature",
        },
        {
            "interface_slot_id": "M0NDBI08_SCALE_LAW",
            "body_slot_id": "M0NDB07_SCALE_LAW",
            "interface_class": "scale_law_interface",
            "interface_contract": "scale slots may be named and counted, but their law and numeric values remain unwritten until readout-equation work",
            "required_handoff": "scale_slot_id;scale_role;unit_role_status;selection_guard_id",
            "blocked_behavior": "select_scale_from_heldout_score_or_best_fit_curve",
            "allowed_next_use": "readout_equation_scale_slot_contract",
        },
        {
            "interface_slot_id": "M0NDBI08_COEFFICIENT_DOMAIN",
            "body_slot_id": "M0NDB07_COEFFICIENT_DOMAIN",
            "interface_class": "coefficient_domain_interface",
            "interface_contract": "coefficient slots may be exposed for later counting, without assigning values or hidden per-galaxy privileges",
            "required_handoff": "coefficient_slot_id;fixed_or_free_status;unit_role_status;parameter_count_guard_id",
            "blocked_behavior": "discount_or_add_parameters_after_family_comparison",
            "allowed_next_use": "readout_equation_parameter_exposure_contract",
        },
        {
            "interface_slot_id": "M0NDBI08_FALLBACK_BRANCHES",
            "body_slot_id": "M0NDB07_FALLBACK_BRANCHES",
            "interface_class": "fallback_branch_interface",
            "interface_contract": "null, gauge, invalid-input, and missing-label branches stop or route construction rather than adding rescue terms",
            "required_handoff": "failure_route_id;null_or_gauge_status;stop_condition;downstream_blocker_id",
            "blocked_behavior": "emit_residual_specific_rescue_term_or_exception",
            "allowed_next_use": "readout_equation_domain_and_failure_contract",
        },
        {
            "interface_slot_id": "M0NDBI08_OUTPUT_UNIT_CHECK",
            "body_slot_id": "M0NDB07_OUTPUT_UNIT_CHECK",
            "interface_class": "output_unit_interface",
            "interface_contract": "the output target remains v_pred_km_s on the frozen radial grid, but the velocity-producing equation is not written here",
            "required_handoff": "assembly_id;argument_signature_id;output_unit_target;guard_order",
            "blocked_behavior": "write_velocity_prediction_or_unit_rescale",
            "allowed_next_use": "readout_equation_unit_path_contract",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["interface_status"] = "READY"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_formula_body_interface_only_no_equation_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["interface_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    machine_ready = machine_form_ready()
    return [
        {
            "summary_id": "M0_NO_DARK_FORMULA_BODY_INTERFACE_V08",
            "interface_artifact": "m0_no_dark_formula_body_interface_v08",
            "machine_form_status": "READY" if machine_ready else "BLOCKED",
            "interface_rows": len(rows),
            "ready_interface_rows": ready,
            "blocked_interface_rows": blocked,
            "readout_equation_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_FORMULA_BODY_INTERFACE_READY"
            if blocked == 0 and machine_ready
            else "M0_NO_DARK_FORMULA_BODY_INTERFACE_BLOCKED",
            "next_required_artifact": "m0_no_dark_readout_equation_v08",
            "claim_boundary": "m0_no_dark_formula_body_interface_only_no_equation_no_predictions_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_formula_body_interface_v08.md").write_text(
        """# M0 No-Dark Formula Body Interface v08

**Doc class:** no-dark M0 formula-body interface contract
**Status:** interface ready; readout equation still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_formula_body_interface.py
```

Derived outputs:

```text
data/derived/m0_no_dark_formula_body_interface_v08.csv
data/derived/m0_no_dark_formula_body_interface_summary_v08.csv
```

This artifact promotes the non-equation interface pieces needed by the later M0
no-dark formula body. It records the source-argument, baryonic handoff,
scale-slot, coefficient-domain, fallback-branch, and output-unit interfaces.

## Current Result

The expected status is:

```text
M0_NO_DARK_FORMULA_BODY_INTERFACE_READY
```

The next required artifact is:

```text
m0_no_dark_readout_equation_v08
```

## Claim Boundary

This interface does not write the M0 no-dark readout equation, does not define a
velocity formula, does not assign numeric coefficient values, does not write
prediction rows, and does not allow endpoint scoring. It only narrows the
family-prediction blocker to the missing readout-equation artifact.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = interface_rows()
    write_csv(DERIVED / "m0_no_dark_formula_body_interface_v08.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_formula_body_interface_summary_v08.csv",
        summary(rows),
        [
            "summary_id",
            "interface_artifact",
            "machine_form_status",
            "interface_rows",
            "ready_interface_rows",
            "blocked_interface_rows",
            "readout_equation_written",
            "formula_claim_allowed",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_FORMULA_BODY_INTERFACE_V08_BUILT")


if __name__ == "__main__":
    main()
