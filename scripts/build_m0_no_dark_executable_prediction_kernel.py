#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDNAMES = [
    "kernel_check_id",
    "kernel_component",
    "required_condition",
    "observed_status",
    "kernel_decision",
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


def kernel_rows() -> list[dict[str, object]]:
    row_writer = summary_row("m0_no_dark_prediction_row_writer_summary_v08.csv")
    body = summary_row("m0_no_dark_frozen_expression_body_summary_v14.csv")
    kernel_expression = summary_row("m0_no_dark_kernel_expression_contract_summary_v10.csv")
    equation_kernel = summary_row("m0_no_dark_equation_kernel_contract_summary_v09.csv")
    readout_equation = summary_row("m0_no_dark_readout_equation_contract_summary_v08.csv")
    formula_body = summary_row("m0_no_dark_formula_body_contract_summary_v07.csv")
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_unit_rescale;posthoc_coefficient_fit"
    rows = [
        {
            "kernel_check_id": "M0NDEPK08_WRITER_HANDOFF",
            "kernel_component": "prediction_row_writer_handoff",
            "required_condition": "prediction-row writer gate is present and hands off to executable-kernel review",
            "observed_status": row_writer["overall_status"],
            "kernel_decision": "READY_FOR_EXECUTABLE_KERNEL_REVIEW",
            "next_required_artifact": "m0_no_dark_velocity_readout_formula_v08",
        },
        {
            "kernel_check_id": "M0NDEPK08_BODY_NOT_FORMULA",
            "kernel_component": "frozen_expression_body",
            "required_condition": "source-side expression body must be promoted into an executable velocity-readout formula before row emission",
            "observed_status": body["overall_status"],
            "kernel_decision": "BLOCKED_VELOCITY_FORMULA_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_readout_formula_v08",
        },
        {
            "kernel_check_id": "M0NDEPK08_KERNEL_EXPRESSION",
            "kernel_component": "kernel_expression_contract",
            "required_condition": "kernel expression contract must be converted into executable semantics with no endpoint-selected terms",
            "observed_status": kernel_expression["overall_status"],
            "kernel_decision": "BLOCKED_EXECUTABLE_SEMANTICS_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_readout_formula_v08",
        },
        {
            "kernel_check_id": "M0NDEPK08_EQUATION_KERNEL",
            "kernel_component": "equation_kernel_contract",
            "required_condition": "equation-kernel contract must expose a callable map from declared inputs to velocity rows",
            "observed_status": equation_kernel["overall_status"],
            "kernel_decision": "BLOCKED_CALLABLE_MAP_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_readout_formula_v08",
        },
        {
            "kernel_check_id": "M0NDEPK08_READOUT_EQUATION",
            "kernel_component": "readout_equation_contract",
            "required_condition": "readout-equation contract must actually write the velocity-readout equation before numeric rows",
            "observed_status": readout_equation["overall_status"],
            "kernel_decision": "BLOCKED_EQUATION_NOT_WRITTEN",
            "next_required_artifact": "m0_no_dark_velocity_readout_formula_v08",
        },
        {
            "kernel_check_id": "M0NDEPK08_FORMULA_BODY",
            "kernel_component": "formula_body_contract",
            "required_condition": "formula-body contract must write a source-to-rotation formula body before predictions",
            "observed_status": formula_body["overall_status"],
            "kernel_decision": "BLOCKED_FORMULA_BODY_ROWS_NOT_WRITTEN",
            "next_required_artifact": "m0_no_dark_velocity_readout_formula_v08",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["velocity_formula_written"] = "false"
        row["numeric_prediction_rows_written"] = 0
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_executable_prediction_kernel_gate_only_no_formula_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = sum(str(row["kernel_decision"]).startswith("BLOCKED") for row in rows)
    return [
        {
            "summary_id": "M0_NO_DARK_EXECUTABLE_PREDICTION_KERNEL_V08",
            "kernel_artifact": "m0_no_dark_executable_prediction_kernel_v08",
            "kernel_checks": len(rows),
            "blocked_kernel_checks": blocked,
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": 0,
            "families_with_numeric_predictions": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXECUTABLE_KERNEL_PRESENT_BLOCKED_VELOCITY_FORMULA_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_readout_formula_v08",
            "claim_boundary": "m0_no_dark_executable_prediction_kernel_gate_only_no_formula_no_predictions_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_executable_prediction_kernel_v08.md").write_text(
        """# M0 No-Dark Executable Prediction Kernel v08

**Doc class:** executable prediction-kernel gate
**Status:** kernel gate present; velocity formula missing; no predictions

Script:

```text
scripts/build_m0_no_dark_executable_prediction_kernel.py
```

Derived outputs:

```text
data/derived/m0_no_dark_executable_prediction_kernel_v08.csv
data/derived/m0_no_dark_executable_prediction_kernel_summary_v08.csv
```

This artifact closes the `m0_no_dark_executable_prediction_kernel_v08`
presence blocker without promoting the M0 no-dark source-side expression body
into a velocity formula. It records that the next missing object is the
velocity-readout formula body needed before any `v_pred_km_s` row can be
emitted.

## Current Result

The expected status is:

```text
M0_NO_DARK_EXECUTABLE_KERNEL_PRESENT_BLOCKED_VELOCITY_FORMULA_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_readout_formula_v08
```

## Claim Boundary

This gate does not define a velocity formula, does not assign coefficients,
does not write prediction rows, does not run endpoint scoring, and does not
decide the dark-sector question. It only narrows the scoring blocker from
``executable kernel missing'' to the missing M0 no-dark velocity-readout
formula.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = kernel_rows()
    write_csv(DERIVED / "m0_no_dark_executable_prediction_kernel_v08.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_executable_prediction_kernel_summary_v08.csv",
        summary(rows),
        [
            "summary_id",
            "kernel_artifact",
            "kernel_checks",
            "blocked_kernel_checks",
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
    print("PAPER11_M0_NO_DARK_EXECUTABLE_PREDICTION_KERNEL_V08_BUILT")


if __name__ == "__main__":
    main()
