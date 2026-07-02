#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


ROW_FIELDS = [
    "writer_check_id",
    "writer_component",
    "required_condition",
    "observed_status",
    "writer_decision",
    "next_required_artifact",
    "forbidden_inputs",
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


def row_writer_rows() -> list[dict[str, object]]:
    formula_table = summary_row("m0_no_dark_formula_table_contract_summary_v06.csv")
    expression_body = summary_row("m0_no_dark_frozen_expression_body_summary_v14.csv")
    kernel_expression = summary_row("m0_no_dark_kernel_expression_contract_summary_v10.csv")
    equation_kernel = summary_row("m0_no_dark_equation_kernel_contract_summary_v09.csv")
    readout_equation = summary_row("m0_no_dark_readout_equation_contract_summary_v08.csv")
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_prediction_rescale"
    rows = [
        {
            "writer_check_id": "M0NDRW08_FORMULA_TABLE_HANDOFF",
            "writer_component": "formula_table_handoff",
            "required_condition": "M0 no-dark formula-table contract is ready for prediction rows",
            "observed_status": formula_table["overall_status"],
            "writer_decision": "READY_FOR_WRITER_REVIEW",
            "next_required_artifact": "m0_no_dark_executable_prediction_kernel_v08",
        },
        {
            "writer_check_id": "M0NDRW08_EXPRESSION_BODY",
            "writer_component": "frozen_expression_body",
            "required_condition": "frozen expression body is present but must not be treated as a velocity formula",
            "observed_status": expression_body["overall_status"],
            "writer_decision": "BLOCKED_NOT_EXECUTABLE_VELOCITY_FORMULA",
            "next_required_artifact": "m0_no_dark_executable_prediction_kernel_v08",
        },
        {
            "writer_check_id": "M0NDRW08_KERNEL_EXPRESSION",
            "writer_component": "kernel_expression",
            "required_condition": "kernel expression must expose an executable prediction callable with audited velocity units",
            "observed_status": kernel_expression["overall_status"],
            "writer_decision": "BLOCKED_EXECUTABLE_KERNEL_MISSING",
            "next_required_artifact": "m0_no_dark_executable_prediction_kernel_v08",
        },
        {
            "writer_check_id": "M0NDRW08_EQUATION_KERNEL",
            "writer_component": "equation_kernel",
            "required_condition": "equation kernel must serialize a source-to-v_pred_km_s map without endpoint-selected terms",
            "observed_status": equation_kernel["overall_status"],
            "writer_decision": "BLOCKED_EXECUTABLE_KERNEL_MISSING",
            "next_required_artifact": "m0_no_dark_executable_prediction_kernel_v08",
        },
        {
            "writer_check_id": "M0NDRW08_READOUT_EQUATION",
            "writer_component": "readout_equation",
            "required_condition": "readout equation must authorize row-level v_pred_km_s emission on the frozen radial grid",
            "observed_status": readout_equation["overall_status"],
            "writer_decision": "BLOCKED_NUMERIC_ROW_EMISSION_FORBIDDEN",
            "next_required_artifact": "m0_no_dark_executable_prediction_kernel_v08",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["numeric_prediction_rows_written"] = 0
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_prediction_row_writer_gate_only_no_predictions_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = sum(str(row["writer_decision"]).startswith("BLOCKED") for row in rows)
    return [
        {
            "summary_id": "M0_NO_DARK_PREDICTION_ROW_WRITER_V08",
            "writer_artifact": "m0_no_dark_prediction_row_writer_v08",
            "writer_checks": len(rows),
            "blocked_writer_checks": blocked,
            "numeric_prediction_rows_written": 0,
            "families_with_numeric_predictions": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_PREDICTION_ROW_WRITER_PRESENT_BLOCKED_EXECUTABLE_KERNEL_MISSING",
            "next_required_artifact": "m0_no_dark_executable_prediction_kernel_v08",
            "claim_boundary": "m0_no_dark_prediction_row_writer_gate_only_no_predictions_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_prediction_row_writer_v08.md").write_text(
        """# M0 No-Dark Prediction Row Writer v08

**Doc class:** prediction-row writer gate
**Status:** writer gate present; numeric row emission blocked

Script:

```text
scripts/build_m0_no_dark_prediction_row_writer.py
```

Derived outputs:

```text
data/derived/m0_no_dark_prediction_row_writer_v08.csv
data/derived/m0_no_dark_prediction_row_writer_summary_v08.csv
```

This artifact closes the narrow `m0_no_dark_prediction_row_writer_v08`
presence blocker without writing `v_pred_km_s` rows. The writer gate is present,
but it refuses row emission because the M0 no-dark path still lacks an
executable, dimensionally audited prediction kernel.

## Current Result

The expected status is:

```text
M0_NO_DARK_PREDICTION_ROW_WRITER_PRESENT_BLOCKED_EXECUTABLE_KERNEL_MISSING
```

The next required artifact is:

```text
m0_no_dark_executable_prediction_kernel_v08
```

## Claim Boundary

This gate does not compute velocities, does not write numeric family prediction
rows, does not compare M0/M1/M2, does not activate endpoint scoring, and does
not decide the dark-sector question. It only states the minimum condition under
which the M0 no-dark family could later emit prediction rows.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = row_writer_rows()
    write_csv(DERIVED / "m0_no_dark_prediction_row_writer_v08.csv", rows, ROW_FIELDS)
    write_csv(
        DERIVED / "m0_no_dark_prediction_row_writer_summary_v08.csv",
        summary(rows),
        [
            "summary_id",
            "writer_artifact",
            "writer_checks",
            "blocked_writer_checks",
            "numeric_prediction_rows_written",
            "families_with_numeric_predictions",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_PREDICTION_ROW_WRITER_V08_BUILT")


if __name__ == "__main__":
    main()
