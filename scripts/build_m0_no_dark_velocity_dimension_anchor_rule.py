#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDNAMES = [
    "dimension_anchor_check_id",
    "dimension_anchor_component",
    "required_condition",
    "observed_status",
    "dimension_anchor_decision",
    "next_required_artifact",
    "forbidden_inputs",
    "dimension_anchor_written",
    "anchor_source_law_written",
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


def dimension_anchor_rows() -> list[dict[str, object]]:
    unit_lift = summary_row("m0_no_dark_velocity_unit_lift_rule_summary_v08.csv")
    dimensional_trace = summary_row("m0_no_dark_payload_dimensional_trace_summary_v12.csv")
    readout_interface = summary_row("m0_no_dark_readout_equation_interface_summary_v08.csv")
    coefficient_policy = summary_row("m0_no_dark_coefficient_policy_summary_v07.csv")
    scale_policy = summary_row("m0_no_dark_scale_policy_summary_v07.csv")
    leakage_certificate = summary_row("m0_no_dark_payload_leakage_certificate_summary_v12.csv")
    common_forbidden = (
        "endpoint_residual;heldout_score;family_winner;best_fit_curve;"
        "posthoc_unit_rescale;posthoc_coefficient_fit;posthoc_anchor_choice;"
        "posthoc_anchor_source_law"
    )
    rows = [
        {
            "dimension_anchor_check_id": "M0NDVDAR08_UNIT_LIFT_HANDOFF",
            "dimension_anchor_component": "unit_lift_handoff",
            "required_condition": "velocity-unit lift gate is present and identifies the missing velocity-dimension anchor",
            "observed_status": unit_lift["overall_status"],
            "dimension_anchor_decision": "READY_FOR_DIMENSION_ANCHOR_REVIEW",
            "next_required_artifact": "m0_no_dark_velocity_anchor_source_law_v08",
        },
        {
            "dimension_anchor_check_id": "M0NDVDAR08_OUTPUT_TARGET",
            "dimension_anchor_component": "output_target_guard",
            "required_condition": "readout interface declares the target velocity unit but does not supply the anchor source law",
            "observed_status": readout_interface["overall_status"],
            "dimension_anchor_decision": "READY_OUTPUT_TARGET_GUARD_ONLY",
            "next_required_artifact": "m0_no_dark_velocity_anchor_source_law_v08",
        },
        {
            "dimension_anchor_check_id": "M0NDVDAR08_UNIT_CLASSES",
            "dimension_anchor_component": "unit_class_guard",
            "required_condition": "dimensional trace classifies unit roles without choosing which physical source anchors velocity",
            "observed_status": dimensional_trace["overall_status"],
            "dimension_anchor_decision": "READY_UNIT_CLASS_GUARD_ONLY",
            "next_required_artifact": "m0_no_dark_velocity_anchor_source_law_v08",
        },
        {
            "dimension_anchor_check_id": "M0NDVDAR08_ANCHOR_SOURCE_LAW",
            "dimension_anchor_component": "anchor_source_law",
            "required_condition": "a source-independent law must declare the allowed physical source of the velocity dimension",
            "observed_status": "NO_VELOCITY_ANCHOR_SOURCE_LAW_PRESENT",
            "dimension_anchor_decision": "BLOCKED_ANCHOR_SOURCE_LAW_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_source_law_v08",
        },
        {
            "dimension_anchor_check_id": "M0NDVDAR08_NORMALIZATION",
            "dimension_anchor_component": "normalization_guard",
            "required_condition": "coefficient and scale policies cannot hide an anchor choice or unit conversion value",
            "observed_status": f"{coefficient_policy['overall_status']}+{scale_policy['overall_status']}",
            "dimension_anchor_decision": "BLOCKED_ANCHOR_NORMALIZATION_SOURCE_LAW_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_source_law_v08",
        },
        {
            "dimension_anchor_check_id": "M0NDVDAR08_LEAKAGE_GUARD",
            "dimension_anchor_component": "leakage_guard",
            "required_condition": "anchor choice must remain source-side and cannot be selected from endpoint scoring or heldout residuals",
            "observed_status": leakage_certificate["overall_status"],
            "dimension_anchor_decision": "READY_LEAKAGE_GUARD_ONLY",
            "next_required_artifact": "m0_no_dark_velocity_anchor_source_law_v08",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["dimension_anchor_written"] = "false"
        row["anchor_source_law_written"] = "false"
        row["velocity_formula_written"] = "false"
        row["numeric_prediction_rows_written"] = 0
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_velocity_dimension_anchor_rule_gate_only_no_anchor_source_law_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = sum(str(row["dimension_anchor_decision"]).startswith("BLOCKED") for row in rows)
    return [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_DIMENSION_ANCHOR_RULE_V08",
            "dimension_anchor_artifact": "m0_no_dark_velocity_dimension_anchor_rule_v08",
            "dimension_anchor_checks": len(rows),
            "blocked_dimension_anchor_checks": blocked,
            "dimension_anchor_written": "false",
            "anchor_source_law_written": "false",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": 0,
            "families_with_numeric_predictions": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_DIMENSION_ANCHOR_PRESENT_BLOCKED_ANCHOR_SOURCE_LAW_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_source_law_v08",
            "claim_boundary": "m0_no_dark_velocity_dimension_anchor_rule_gate_only_no_anchor_source_law_no_predictions_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_velocity_dimension_anchor_rule_v08.md").write_text(
        """# M0 No-Dark Velocity-Dimension Anchor Rule v08

**Doc class:** velocity-dimension anchor gate
**Status:** dimension-anchor gate present; anchor source law missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_dimension_anchor_rule.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_dimension_anchor_rule_v08.csv
data/derived/m0_no_dark_velocity_dimension_anchor_rule_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_dimension_anchor_rule_v08`
presence blocker without declaring the anchor source law. It records that the
no-dark route still needs a source-independent rule for which physical source
may carry the velocity dimension before unit-free morphology/readout terms can
lawfully contribute to a `v_pred_km_s` formula.

## Current Result

The expected status is:

```text
M0_NO_DARK_DIMENSION_ANCHOR_PRESENT_BLOCKED_ANCHOR_SOURCE_LAW_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_anchor_source_law_v08
```

## Claim Boundary

This gate does not declare the anchor source law, does not choose a coupling
normalization, does not assign coefficients or scales, does not write a velocity
formula, does not write prediction rows, does not run endpoint scoring, and does
not decide the dark-sector question. It only narrows the scoring blocker to the
missing velocity-anchor source law.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = dimension_anchor_rows()
    write_csv(DERIVED / "m0_no_dark_velocity_dimension_anchor_rule_v08.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_velocity_dimension_anchor_rule_summary_v08.csv",
        summary(rows),
        [
            "summary_id",
            "dimension_anchor_artifact",
            "dimension_anchor_checks",
            "blocked_dimension_anchor_checks",
            "dimension_anchor_written",
            "anchor_source_law_written",
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
    print("PAPER11_M0_NO_DARK_VELOCITY_DIMENSION_ANCHOR_RULE_V08_BUILT")


if __name__ == "__main__":
    main()
