#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDNAMES = [
    "formula_check_id",
    "formula_component",
    "required_condition",
    "observed_status",
    "formula_decision",
    "next_required_artifact",
    "forbidden_inputs",
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


def formula_rows() -> list[dict[str, object]]:
    executable_kernel = summary_row("m0_no_dark_executable_prediction_kernel_summary_v08.csv")
    formula_body = summary_row("m0_no_dark_formula_body_contract_summary_v07.csv")
    readout_equation = summary_row("m0_no_dark_readout_equation_contract_summary_v08.csv")
    dimensional_audit = summary_row("m0_no_dark_expression_dimensional_audit_summary_v12.csv")
    machine_form = summary_row("m0_no_dark_expression_machine_form_summary_v12.csv")
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_unit_rescale;posthoc_coefficient_fit"
    rows = [
        {
            "formula_check_id": "M0NDVRF08_KERNEL_HANDOFF",
            "formula_component": "executable_kernel_handoff",
            "required_condition": "executable-kernel gate is present and hands off to velocity-readout formula review",
            "observed_status": executable_kernel["overall_status"],
            "formula_decision": "READY_FOR_VELOCITY_FORMULA_REVIEW",
            "next_required_artifact": "m0_no_dark_source_to_rotation_equation_body_v08",
        },
        {
            "formula_check_id": "M0NDVRF08_FORMULA_BODY",
            "formula_component": "formula_body_contract",
            "required_condition": "formula body contract must promote ready slots into an explicit source-to-rotation equation body",
            "observed_status": formula_body["overall_status"],
            "formula_decision": "BLOCKED_EQUATION_BODY_NOT_WRITTEN",
            "next_required_artifact": "m0_no_dark_source_to_rotation_equation_body_v08",
        },
        {
            "formula_check_id": "M0NDVRF08_READOUT_EQUATION",
            "formula_component": "readout_equation_contract",
            "required_condition": "readout-equation contract must expose a velocity-dimensional equation, not only a readiness contract",
            "observed_status": readout_equation["overall_status"],
            "formula_decision": "BLOCKED_READOUT_EQUATION_BODY_MISSING",
            "next_required_artifact": "m0_no_dark_source_to_rotation_equation_body_v08",
        },
        {
            "formula_check_id": "M0NDVRF08_DIMENSIONAL_AUDIT",
            "formula_component": "dimensional_audit",
            "required_condition": "unit-route audit must remain satisfied when the equation body is later written",
            "observed_status": dimensional_audit["overall_status"],
            "formula_decision": "READY_UNIT_ROUTE_GUARD_ONLY",
            "next_required_artifact": "m0_no_dark_source_to_rotation_equation_body_v08",
        },
        {
            "formula_check_id": "M0NDVRF08_MACHINE_FORM",
            "formula_component": "machine_form",
            "required_condition": "machine form must remain a serialization contract until an equation body exists",
            "observed_status": machine_form["overall_status"],
            "formula_decision": "READY_SERIALIZATION_GUARD_ONLY",
            "next_required_artifact": "m0_no_dark_source_to_rotation_equation_body_v08",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["velocity_formula_written"] = "false"
        row["numeric_prediction_rows_written"] = 0
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_velocity_readout_formula_gate_only_no_equation_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = sum(str(row["formula_decision"]).startswith("BLOCKED") for row in rows)
    return [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_READOUT_FORMULA_V08",
            "formula_artifact": "m0_no_dark_velocity_readout_formula_v08",
            "formula_checks": len(rows),
            "blocked_formula_checks": blocked,
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": 0,
            "families_with_numeric_predictions": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_VELOCITY_FORMULA_PRESENT_BLOCKED_EQUATION_BODY_MISSING",
            "next_required_artifact": "m0_no_dark_source_to_rotation_equation_body_v08",
            "claim_boundary": "m0_no_dark_velocity_readout_formula_gate_only_no_equation_no_predictions_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_velocity_readout_formula_v08.md").write_text(
        """# M0 No-Dark Velocity Readout Formula v08

**Doc class:** velocity-readout formula gate
**Status:** formula gate present; equation body missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_readout_formula.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_readout_formula_v08.csv
data/derived/m0_no_dark_velocity_readout_formula_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_readout_formula_v08` presence
blocker without writing a velocity formula. It records that the ready formula
body, dimensional-audit, and machine-form contracts still need a concrete
source-to-rotation equation body before `v_pred_km_s` rows can be emitted.

## Current Result

The expected status is:

```text
M0_NO_DARK_VELOCITY_FORMULA_PRESENT_BLOCKED_EQUATION_BODY_MISSING
```

The next required artifact is:

```text
m0_no_dark_source_to_rotation_equation_body_v08
```

## Claim Boundary

This gate does not define the equation body, does not assign coefficients,
does not write prediction rows, does not run endpoint scoring, and does not
decide the dark-sector question. It only narrows the scoring blocker from a
missing velocity formula to the missing source-to-rotation equation body.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = formula_rows()
    write_csv(DERIVED / "m0_no_dark_velocity_readout_formula_v08.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_velocity_readout_formula_summary_v08.csv",
        summary(rows),
        [
            "summary_id",
            "formula_artifact",
            "formula_checks",
            "blocked_formula_checks",
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
    print("PAPER11_M0_NO_DARK_VELOCITY_READOUT_FORMULA_V08_BUILT")


if __name__ == "__main__":
    main()
