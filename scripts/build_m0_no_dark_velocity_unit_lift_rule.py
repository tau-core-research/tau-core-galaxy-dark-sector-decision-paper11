#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDNAMES = [
    "unit_lift_check_id",
    "unit_lift_component",
    "required_condition",
    "observed_status",
    "unit_lift_decision",
    "next_required_artifact",
    "forbidden_inputs",
    "velocity_unit_lift_written",
    "dimension_anchor_written",
    "velocity_formula_written",
    "numeric_prediction_rows_written",
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


def summary_row(path: str) -> dict[str, str]:
    rows = read_csv(DERIVED / path)
    if len(rows) != 1:
        raise ValueError(f"expected one summary row in {path}")
    return rows[0]


def unit_lift_rows() -> list[dict[str, object]]:
    coupling_rule = summary_row("m0_no_dark_source_to_velocity_coupling_rule_summary_v08.csv")
    dimensional_trace = summary_row("m0_no_dark_payload_dimensional_trace_summary_v12.csv")
    readout_interface = summary_row("m0_no_dark_readout_equation_interface_summary_v08.csv")
    formula_interface = summary_row("m0_no_dark_formula_body_interface_summary_v08.csv")
    coefficient_policy = summary_row("m0_no_dark_coefficient_policy_summary_v07.csv")
    scale_policy = summary_row("m0_no_dark_scale_policy_summary_v07.csv")
    common_forbidden = (
        "endpoint_residual;heldout_score;family_winner;best_fit_curve;"
        "posthoc_unit_rescale;posthoc_coefficient_fit;posthoc_coupling_choice;"
        "posthoc_dimension_anchor"
    )
    rows = [
        {
            "unit_lift_check_id": "M0NDVULR08_COUPLING_HANDOFF",
            "unit_lift_component": "coupling_rule_handoff",
            "required_condition": "source-to-velocity coupling-rule gate is present and identifies the missing velocity-unit lift",
            "observed_status": coupling_rule["overall_status"],
            "unit_lift_decision": "READY_FOR_UNIT_LIFT_REVIEW",
            "next_required_artifact": "m0_no_dark_velocity_dimension_anchor_rule_v08",
        },
        {
            "unit_lift_check_id": "M0NDVULR08_DIMENSION_TRACE",
            "unit_lift_component": "payload_dimensional_trace",
            "required_condition": "payload dimensional trace declares unit classes but does not choose a velocity-producing anchor",
            "observed_status": dimensional_trace["overall_status"],
            "unit_lift_decision": "READY_DIMENSION_TRACE_GUARD_ONLY",
            "next_required_artifact": "m0_no_dark_velocity_dimension_anchor_rule_v08",
        },
        {
            "unit_lift_check_id": "M0NDVULR08_READOUT_OUTPUT",
            "unit_lift_component": "readout_output_target",
            "required_condition": "readout interface declares the v_pred_km_s target while the dimensional path remains unproved",
            "observed_status": readout_interface["overall_status"],
            "unit_lift_decision": "READY_OUTPUT_TARGET_GUARD_ONLY",
            "next_required_artifact": "m0_no_dark_velocity_dimension_anchor_rule_v08",
        },
        {
            "unit_lift_check_id": "M0NDVULR08_FORMULA_INTERFACE",
            "unit_lift_component": "formula_body_interface",
            "required_condition": "formula interface exposes arguments but does not authorize a velocity-dimensional lift",
            "observed_status": formula_interface["overall_status"],
            "unit_lift_decision": "READY_INTERFACE_GUARD_ONLY",
            "next_required_artifact": "m0_no_dark_velocity_dimension_anchor_rule_v08",
        },
        {
            "unit_lift_check_id": "M0NDVULR08_DIMENSION_ANCHOR",
            "unit_lift_component": "velocity_dimension_anchor",
            "required_condition": "a source-independent dimensional anchor must be declared before unit-free source terms can enter velocity units",
            "observed_status": "NO_VELOCITY_DIMENSION_ANCHOR_RULE_PRESENT",
            "unit_lift_decision": "BLOCKED_VELOCITY_DIMENSION_ANCHOR_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_dimension_anchor_rule_v08",
        },
        {
            "unit_lift_check_id": "M0NDVULR08_NORMALIZATION_GUARD",
            "unit_lift_component": "normalization_guard",
            "required_condition": "coefficient and scale policies may guard normalization but cannot provide hidden unit conversion values",
            "observed_status": f"{coefficient_policy['overall_status']}+{scale_policy['overall_status']}",
            "unit_lift_decision": "BLOCKED_ANCHOR_NORMALIZATION_RULE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_dimension_anchor_rule_v08",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["velocity_unit_lift_written"] = "false"
        row["dimension_anchor_written"] = "false"
        row["velocity_formula_written"] = "false"
        row["numeric_prediction_rows_written"] = 0
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_velocity_unit_lift_rule_gate_only_no_dimension_anchor_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = sum(str(row["unit_lift_decision"]).startswith("BLOCKED") for row in rows)
    return [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_UNIT_LIFT_RULE_V08",
            "unit_lift_artifact": "m0_no_dark_velocity_unit_lift_rule_v08",
            "unit_lift_checks": len(rows),
            "blocked_unit_lift_checks": blocked,
            "velocity_unit_lift_written": "false",
            "dimension_anchor_written": "false",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": 0,
            "families_with_numeric_predictions": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_VELOCITY_UNIT_LIFT_PRESENT_BLOCKED_DIMENSION_ANCHOR_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_dimension_anchor_rule_v08",
            "claim_boundary": "m0_no_dark_velocity_unit_lift_rule_gate_only_no_dimension_anchor_no_predictions_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_velocity_unit_lift_rule_v08.md").write_text(
        """# M0 No-Dark Velocity-Unit Lift Rule v08

**Doc class:** velocity-unit lift gate
**Status:** unit-lift gate present; dimension anchor missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_unit_lift_rule.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_unit_lift_rule_v08.csv
data/derived/m0_no_dark_velocity_unit_lift_rule_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_unit_lift_rule_v08` presence
blocker without declaring a velocity-producing unit lift. It records that the
no-dark route still needs a source-independent velocity-dimension anchor before
unit-free morphology/readout source variables can lawfully contribute to a
`v_pred_km_s` formula.

## Current Result

The expected status is:

```text
M0_NO_DARK_VELOCITY_UNIT_LIFT_PRESENT_BLOCKED_DIMENSION_ANCHOR_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_dimension_anchor_rule_v08
```

## Claim Boundary

This gate does not declare a dimension anchor, does not choose a coupling
normalization, does not assign coefficients or scales, does not write a velocity
formula, does not write prediction rows, does not run endpoint scoring, and does
not decide the dark-sector question. It only narrows the scoring blocker to the
missing velocity-dimension anchor rule.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = unit_lift_rows()
    write_csv(DERIVED / "m0_no_dark_velocity_unit_lift_rule_v08.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_velocity_unit_lift_rule_summary_v08.csv",
        summary(rows),
        [
            "summary_id",
            "unit_lift_artifact",
            "unit_lift_checks",
            "blocked_unit_lift_checks",
            "velocity_unit_lift_written",
            "dimension_anchor_written",
            "velocity_formula_written",
            "numeric_prediction_rows_written",
            "families_with_numeric_predictions",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_VELOCITY_UNIT_LIFT_RULE_V08_BUILT")


if __name__ == "__main__":
    main()
