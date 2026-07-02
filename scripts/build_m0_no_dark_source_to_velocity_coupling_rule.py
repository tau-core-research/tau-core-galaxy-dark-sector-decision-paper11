#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDNAMES = [
    "coupling_rule_check_id",
    "coupling_rule_component",
    "required_condition",
    "observed_status",
    "coupling_rule_decision",
    "next_required_artifact",
    "forbidden_inputs",
    "coupling_rule_written",
    "velocity_unit_lift_written",
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


def coupling_rule_rows() -> list[dict[str, object]]:
    equation_body = summary_row("m0_no_dark_source_to_rotation_equation_body_summary_v08.csv")
    dimensional_audit = summary_row("m0_no_dark_expression_dimensional_audit_summary_v12.csv")
    coefficient_policy = summary_row("m0_no_dark_coefficient_policy_summary_v07.csv")
    scale_policy = summary_row("m0_no_dark_scale_policy_summary_v07.csv")
    formula_interface = summary_row("m0_no_dark_formula_body_interface_summary_v08.csv")
    common_forbidden = (
        "endpoint_residual;heldout_score;family_winner;best_fit_curve;"
        "posthoc_unit_rescale;posthoc_coefficient_fit;posthoc_coupling_choice;"
        "posthoc_velocity_unit_lift"
    )
    rows = [
        {
            "coupling_rule_check_id": "M0NDSTVCR08_EQUATION_BODY_HANDOFF",
            "coupling_rule_component": "equation_body_handoff",
            "required_condition": "equation-body gate is present and identifies the missing source-to-velocity coupling rule",
            "observed_status": equation_body["overall_status"],
            "coupling_rule_decision": "READY_FOR_COUPLING_RULE_REVIEW",
            "next_required_artifact": "m0_no_dark_velocity_unit_lift_rule_v08",
        },
        {
            "coupling_rule_check_id": "M0NDSTVCR08_UNIT_ROUTE",
            "coupling_rule_component": "velocity_unit_lift",
            "required_condition": "unit-free morphology/readout source variables need an explicit source-independent lift into velocity units",
            "observed_status": dimensional_audit["overall_status"],
            "coupling_rule_decision": "BLOCKED_VELOCITY_UNIT_LIFT_RULE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_unit_lift_rule_v08",
        },
        {
            "coupling_rule_check_id": "M0NDSTVCR08_COUPLING_NORMALIZATION",
            "coupling_rule_component": "coupling_normalization",
            "required_condition": "any coupling normalization must be declared before endpoint scoring and cannot be selected from heldout residuals",
            "observed_status": coefficient_policy["overall_status"],
            "coupling_rule_decision": "BLOCKED_SOURCE_INDEPENDENT_NORMALIZATION_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_unit_lift_rule_v08",
        },
        {
            "coupling_rule_check_id": "M0NDSTVCR08_SCALE_ROUTE",
            "coupling_rule_component": "scale_route",
            "required_condition": "fixed scales may guard the route but cannot silently provide the velocity-dimensional lift",
            "observed_status": scale_policy["overall_status"],
            "coupling_rule_decision": "READY_SCALE_GUARD_ONLY",
            "next_required_artifact": "m0_no_dark_velocity_unit_lift_rule_v08",
        },
        {
            "coupling_rule_check_id": "M0NDSTVCR08_INTERFACE",
            "coupling_rule_component": "formula_interface",
            "required_condition": "formula interface is present but cannot choose source-to-velocity coupling from endpoint performance",
            "observed_status": formula_interface["overall_status"],
            "coupling_rule_decision": "READY_INTERFACE_GUARD_ONLY",
            "next_required_artifact": "m0_no_dark_velocity_unit_lift_rule_v08",
        },
        {
            "coupling_rule_check_id": "M0NDSTVCR08_OUTPUT_GUARD",
            "coupling_rule_component": "prediction_output_guard",
            "required_condition": "no velocity formula or prediction rows may be emitted until the unit lift and normalization are lawful",
            "observed_status": "NO_VELOCITY_UNIT_LIFT_RULE_PRESENT",
            "coupling_rule_decision": "BLOCKED_OUTPUT_UNAUTHORIZED",
            "next_required_artifact": "m0_no_dark_velocity_unit_lift_rule_v08",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["coupling_rule_written"] = "false"
        row["velocity_unit_lift_written"] = "false"
        row["velocity_formula_written"] = "false"
        row["numeric_prediction_rows_written"] = 0
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_source_to_velocity_coupling_rule_gate_only_no_unit_lift_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = sum(str(row["coupling_rule_decision"]).startswith("BLOCKED") for row in rows)
    return [
        {
            "summary_id": "M0_NO_DARK_SOURCE_TO_VELOCITY_COUPLING_RULE_V08",
            "coupling_rule_artifact": "m0_no_dark_source_to_velocity_coupling_rule_v08",
            "coupling_rule_checks": len(rows),
            "blocked_coupling_rule_checks": blocked,
            "coupling_rule_written": "false",
            "velocity_unit_lift_written": "false",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": 0,
            "families_with_numeric_predictions": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_COUPLING_RULE_PRESENT_BLOCKED_VELOCITY_UNIT_LIFT_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_unit_lift_rule_v08",
            "claim_boundary": "m0_no_dark_source_to_velocity_coupling_rule_gate_only_no_unit_lift_no_predictions_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_source_to_velocity_coupling_rule_v08.md").write_text(
        """# M0 No-Dark Source-to-Velocity Coupling Rule v08

**Doc class:** source-to-velocity coupling-rule gate
**Status:** coupling-rule gate present; velocity-unit lift missing; no predictions

Script:

```text
scripts/build_m0_no_dark_source_to_velocity_coupling_rule.py
```

Derived outputs:

```text
data/derived/m0_no_dark_source_to_velocity_coupling_rule_v08.csv
data/derived/m0_no_dark_source_to_velocity_coupling_rule_summary_v08.csv
```

This artifact closes the `m0_no_dark_source_to_velocity_coupling_rule_v08`
presence blocker without declaring a coupling law. It records that the no-dark
path still needs a source-independent velocity-unit lift before unit-free
morphology/readout source variables can be converted into a velocity-dimensional
readout formula.

## Current Result

The expected status is:

```text
M0_NO_DARK_COUPLING_RULE_PRESENT_BLOCKED_VELOCITY_UNIT_LIFT_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_unit_lift_rule_v08
```

## Claim Boundary

This gate does not define a coupling law, does not choose a unit lift, does not
assign coefficients or scales, does not write a velocity formula, does not
write prediction rows, does not run endpoint scoring, and does not decide the
dark-sector question. It only narrows the scoring blocker to the missing
velocity-unit lift rule.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = coupling_rule_rows()
    write_csv(DERIVED / "m0_no_dark_source_to_velocity_coupling_rule_v08.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_source_to_velocity_coupling_rule_summary_v08.csv",
        summary(rows),
        [
            "summary_id",
            "coupling_rule_artifact",
            "coupling_rule_checks",
            "blocked_coupling_rule_checks",
            "coupling_rule_written",
            "velocity_unit_lift_written",
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
    print("PAPER11_M0_NO_DARK_SOURCE_TO_VELOCITY_COUPLING_RULE_V08_BUILT")


if __name__ == "__main__":
    main()
