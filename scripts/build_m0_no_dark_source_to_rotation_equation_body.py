#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDNAMES = [
    "equation_body_check_id",
    "equation_body_component",
    "required_condition",
    "observed_status",
    "equation_body_decision",
    "next_required_artifact",
    "forbidden_inputs",
    "equation_body_written",
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


def equation_body_rows() -> list[dict[str, object]]:
    velocity_formula = summary_row("m0_no_dark_velocity_readout_formula_summary_v08.csv")
    formula_body = summary_row("m0_no_dark_formula_body_contract_summary_v07.csv")
    formula_interface = summary_row("m0_no_dark_formula_body_interface_summary_v08.csv")
    dimensional_audit = summary_row("m0_no_dark_expression_dimensional_audit_summary_v12.csv")
    coefficient_policy = summary_row("m0_no_dark_coefficient_policy_summary_v07.csv")
    scale_policy = summary_row("m0_no_dark_scale_policy_summary_v07.csv")
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_unit_rescale;posthoc_coefficient_fit;posthoc_coupling_choice"
    rows = [
        {
            "equation_body_check_id": "M0NDSTREB08_FORMULA_HANDOFF",
            "equation_body_component": "velocity_formula_handoff",
            "required_condition": "velocity-readout formula gate is present and hands off to equation-body review",
            "observed_status": velocity_formula["overall_status"],
            "equation_body_decision": "READY_FOR_EQUATION_BODY_REVIEW",
            "next_required_artifact": "m0_no_dark_source_to_velocity_coupling_rule_v08",
        },
        {
            "equation_body_check_id": "M0NDSTREB08_FORMULA_BODY_CONTRACT",
            "equation_body_component": "formula_body_contract",
            "required_condition": "formula-body contract has ready slots but does not itself write an equation",
            "observed_status": formula_body["overall_status"],
            "equation_body_decision": "BLOCKED_EQUATION_BODY_NOT_AUTHORIZED",
            "next_required_artifact": "m0_no_dark_source_to_velocity_coupling_rule_v08",
        },
        {
            "equation_body_check_id": "M0NDSTREB08_INTERFACE",
            "equation_body_component": "formula_body_interface",
            "required_condition": "formula-body interface exposes arguments without choosing a source-to-velocity coupling",
            "observed_status": formula_interface["overall_status"],
            "equation_body_decision": "READY_INTERFACE_GUARD_ONLY",
            "next_required_artifact": "m0_no_dark_source_to_velocity_coupling_rule_v08",
        },
        {
            "equation_body_check_id": "M0NDSTREB08_DIMENSIONAL_COUPLING",
            "equation_body_component": "dimensional_coupling_rule",
            "required_condition": "unit-free source and morphology/readout markers require an explicit lawful coupling before entering velocity units",
            "observed_status": dimensional_audit["overall_status"],
            "equation_body_decision": "BLOCKED_SOURCE_TO_VELOCITY_COUPLING_RULE_MISSING",
            "next_required_artifact": "m0_no_dark_source_to_velocity_coupling_rule_v08",
        },
        {
            "equation_body_check_id": "M0NDSTREB08_COEFFICIENT_POLICY",
            "equation_body_component": "coefficient_policy",
            "required_condition": "coefficient policy is present but cannot assign values or hidden per-galaxy privileges",
            "observed_status": coefficient_policy["overall_status"],
            "equation_body_decision": "READY_POLICY_GUARD_ONLY",
            "next_required_artifact": "m0_no_dark_source_to_velocity_coupling_rule_v08",
        },
        {
            "equation_body_check_id": "M0NDSTREB08_SCALE_POLICY",
            "equation_body_component": "scale_policy",
            "required_condition": "scale policy is present but cannot select a numeric coupling scale from endpoint performance",
            "observed_status": scale_policy["overall_status"],
            "equation_body_decision": "READY_SCALE_GUARD_ONLY",
            "next_required_artifact": "m0_no_dark_source_to_velocity_coupling_rule_v08",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["equation_body_written"] = "false"
        row["velocity_formula_written"] = "false"
        row["numeric_prediction_rows_written"] = 0
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_source_to_rotation_equation_body_gate_only_no_coupling_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = sum(str(row["equation_body_decision"]).startswith("BLOCKED") for row in rows)
    return [
        {
            "summary_id": "M0_NO_DARK_SOURCE_TO_ROTATION_EQUATION_BODY_V08",
            "equation_body_artifact": "m0_no_dark_source_to_rotation_equation_body_v08",
            "equation_body_checks": len(rows),
            "blocked_equation_body_checks": blocked,
            "equation_body_written": "false",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": 0,
            "families_with_numeric_predictions": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EQUATION_BODY_PRESENT_BLOCKED_SOURCE_TO_VELOCITY_COUPLING_RULE_MISSING",
            "next_required_artifact": "m0_no_dark_source_to_velocity_coupling_rule_v08",
            "claim_boundary": "m0_no_dark_source_to_rotation_equation_body_gate_only_no_coupling_no_predictions_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_source_to_rotation_equation_body_v08.md").write_text(
        """# M0 No-Dark Source-to-Rotation Equation Body v08

**Doc class:** source-to-rotation equation-body gate
**Status:** equation-body gate present; coupling rule missing; no predictions

Script:

```text
scripts/build_m0_no_dark_source_to_rotation_equation_body.py
```

Derived outputs:

```text
data/derived/m0_no_dark_source_to_rotation_equation_body_v08.csv
data/derived/m0_no_dark_source_to_rotation_equation_body_summary_v08.csv
```

This artifact closes the `m0_no_dark_source_to_rotation_equation_body_v08`
presence blocker without writing the equation body. It records that the M0
no-dark path still needs an explicit source-to-velocity coupling rule before
source/morphology/readout markers can lawfully enter a velocity-dimensional
formula.

## Current Result

The expected status is:

```text
M0_NO_DARK_EQUATION_BODY_PRESENT_BLOCKED_SOURCE_TO_VELOCITY_COUPLING_RULE_MISSING
```

The next required artifact is:

```text
m0_no_dark_source_to_velocity_coupling_rule_v08
```

## Claim Boundary

This gate does not define the equation body, does not choose a coupling law,
does not assign coefficients or scales, does not write prediction rows, does
not run endpoint scoring, and does not decide the dark-sector question. It only
narrows the scoring blocker to the missing source-to-velocity coupling rule.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = equation_body_rows()
    write_csv(DERIVED / "m0_no_dark_source_to_rotation_equation_body_v08.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_source_to_rotation_equation_body_summary_v08.csv",
        summary(rows),
        [
            "summary_id",
            "equation_body_artifact",
            "equation_body_checks",
            "blocked_equation_body_checks",
            "equation_body_written",
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
    print("PAPER11_M0_NO_DARK_SOURCE_TO_ROTATION_EQUATION_BODY_V08_BUILT")


if __name__ == "__main__":
    main()
