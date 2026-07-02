#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDNAMES = [
    "formula_body_freeze_id",
    "formula_body_layer",
    "source_artifact",
    "frozen_formula_body",
    "required_condition",
    "observed_status",
    "formula_body_freeze_decision",
    "next_required_artifact",
    "forbidden_inputs",
    "formula_body_frozen",
    "velocity_formula_body_written",
    "numeric_prediction_rows_written",
    "endpoint_scoring_allowed",
    "claim_boundary",
]


SUMMARY_FIELDNAMES = [
    "summary_id",
    "formula_body_freeze_artifact",
    "formula_body_freeze_checks",
    "frozen_formula_body_checks",
    "blocked_formula_body_freeze_checks",
    "formula_body_frozen",
    "frozen_formula_body",
    "velocity_formula_body_written",
    "numeric_prediction_rows_written",
    "families_with_numeric_predictions",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]


FROZEN_FORMULA_BODY = "v_body_km_s(R) := v_anchor_km_s(R)"
NEXT_ARTIFACT = "m0_no_dark_prediction_row_value_freeze_v08"


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


def formula_body_freeze_rows() -> list[dict[str, object]]:
    anchor_values = summary_row("m0_no_dark_velocity_anchor_combined_anchor_value_freeze_summary_v08.csv")
    dimensional_trace = summary_row("m0_no_dark_payload_dimensional_trace_summary_v12.csv")
    leakage_pass = summary_row("leakage_audit_pass_review_summary_v78.csv")
    if anchor_values["overall_status"] != (
        "M0_NO_DARK_ANCHOR_COMBINED_ANCHOR_VALUES_FROZEN_BLOCKED_VELOCITY_FORMULA_BODY_FREEZE_MISSING"
    ):
        raise ValueError("combined-anchor value freeze is not in the expected handoff state")

    forbidden = (
        "v_obs_km_s;endpoint_residual;heldout_score;family_winner;best_fit_curve;"
        "posthoc_formula_switch;posthoc_prediction_rescale;posthoc_weight_fit;"
        "posthoc_sign_choice;posthoc_normalization;numeric_score_value"
    )
    source_artifact = "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08"
    rows = [
        {
            "formula_body_freeze_id": "M0NDVRFBF08_ANCHOR_VALUE_HANDOFF",
            "formula_body_layer": "combined_anchor_value_handoff",
            "source_artifact": source_artifact,
            "frozen_formula_body": FROZEN_FORMULA_BODY,
            "required_condition": "combined-anchor values are frozen before any velocity readout body is frozen",
            "observed_status": anchor_values["overall_status"],
            "formula_body_freeze_decision": "READY_FOR_VELOCITY_FORMULA_BODY_FREEZE_REVIEW",
            "next_required_artifact": NEXT_ARTIFACT,
        },
        {
            "formula_body_freeze_id": "M0NDVRFBF08_IDENTITY_READOUT_BODY",
            "formula_body_layer": "identity_no_dark_readout_body",
            "source_artifact": source_artifact,
            "frozen_formula_body": FROZEN_FORMULA_BODY,
            "required_condition": "M0 no-dark readout body uses the frozen baryonic anchor without extra dark-sector response term",
            "observed_status": anchor_values["overall_status"],
            "formula_body_freeze_decision": "IDENTITY_NO_DARK_FORMULA_BODY_FROZEN",
            "next_required_artifact": NEXT_ARTIFACT,
        },
        {
            "formula_body_freeze_id": "M0NDVRFBF08_DIMENSIONAL_BODY",
            "formula_body_layer": "dimensional_body_audit",
            "source_artifact": source_artifact,
            "frozen_formula_body": FROZEN_FORMULA_BODY,
            "required_condition": "v_anchor_km_s already carries km/s units, so the formula body preserves velocity dimension",
            "observed_status": dimensional_trace["overall_status"],
            "formula_body_freeze_decision": "DIMENSIONAL_FORMULA_BODY_FROZEN",
            "next_required_artifact": NEXT_ARTIFACT,
        },
        {
            "formula_body_freeze_id": "M0NDVRFBF08_LEAKAGE_GUARD",
            "formula_body_layer": "formula_body_leakage_guard",
            "source_artifact": source_artifact,
            "frozen_formula_body": FROZEN_FORMULA_BODY,
            "required_condition": "formula body is frozen without observed velocity, residual, heldout score, family winner, or best-fit feedback",
            "observed_status": leakage_pass["overall_status"],
            "formula_body_freeze_decision": "FORMULA_BODY_LEAKAGE_GUARD_FROZEN",
            "next_required_artifact": NEXT_ARTIFACT,
        },
        {
            "formula_body_freeze_id": "M0NDVRFBF08_ROW_VALUE_FREEZE",
            "formula_body_layer": "prediction_row_value_freeze",
            "source_artifact": source_artifact,
            "frozen_formula_body": FROZEN_FORMULA_BODY,
            "required_condition": "a later artifact must freeze prediction row values before family prediction rows or scoring can exist",
            "observed_status": "NO_PREDICTION_ROW_VALUE_FREEZE_PRESENT",
            "formula_body_freeze_decision": "BLOCKED_PREDICTION_ROW_VALUE_FREEZE_MISSING",
            "next_required_artifact": NEXT_ARTIFACT,
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = forbidden
        row["formula_body_frozen"] = "true"
        row["velocity_formula_body_written"] = "true"
        row["numeric_prediction_rows_written"] = 0
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_velocity_readout_formula_body_freeze_only_no_prediction_rows_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = sum(str(row["formula_body_freeze_decision"]).startswith("BLOCKED") for row in rows)
    frozen = sum(str(row["formula_body_freeze_decision"]).endswith("_FROZEN") for row in rows)
    return [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_READOUT_FORMULA_BODY_FREEZE_V08",
            "formula_body_freeze_artifact": "m0_no_dark_velocity_readout_formula_body_freeze_v08",
            "formula_body_freeze_checks": len(rows),
            "frozen_formula_body_checks": frozen,
            "blocked_formula_body_freeze_checks": blocked,
            "formula_body_frozen": "true",
            "frozen_formula_body": FROZEN_FORMULA_BODY,
            "velocity_formula_body_written": "true",
            "numeric_prediction_rows_written": 0,
            "families_with_numeric_predictions": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_VELOCITY_FORMULA_BODY_FROZEN_BLOCKED_PREDICTION_ROW_VALUE_FREEZE_MISSING",
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": "m0_no_dark_velocity_readout_formula_body_freeze_only_no_prediction_rows_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_velocity_readout_formula_body_freeze_v08.md").write_text(
        f"""# M0 No-Dark Velocity Readout Formula Body Freeze v08

**Doc class:** velocity-readout formula body-freeze gate
**Status:** formula body frozen; prediction row values missing; no scoring

Script:

```text
scripts/build_m0_no_dark_velocity_readout_formula_body_freeze.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_readout_formula_body_freeze_v08.csv
data/derived/m0_no_dark_velocity_readout_formula_body_freeze_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_readout_formula_body_freeze_v08`
presence blocker by freezing the M0 no-dark velocity readout formula body:

```text
{FROZEN_FORMULA_BODY}
```

The formula body uses the frozen source-side baryonic anchor values from:

```text
data/derived/m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08.csv
```

It adds no dark-sector response term, no residual-selected correction, and no
posthoc rescaling. It is a formula-body freeze only: it does not emit
`v_pred_km_s` rows and does not activate endpoint scoring.

## Current Result

The expected status is:

```text
M0_NO_DARK_VELOCITY_FORMULA_BODY_FROZEN_BLOCKED_PREDICTION_ROW_VALUE_FREEZE_MISSING
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This gate freezes the source-side no-dark velocity formula body only. It does
not write family prediction rows, does not compute scores, does not compare
M0/M1/M2, and does not decide whether a dark-sector component is required.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = formula_body_freeze_rows()
    write_csv(DERIVED / "m0_no_dark_velocity_readout_formula_body_freeze_v08.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_velocity_readout_formula_body_freeze_summary_v08.csv",
        summary(rows),
        SUMMARY_FIELDNAMES,
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_VELOCITY_READOUT_FORMULA_BODY_FREEZE_V08_BUILT")


if __name__ == "__main__":
    main()
