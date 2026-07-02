#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDNAMES = [
    "anchor_unit_check_id",
    "anchor_unit_component",
    "source_column",
    "source_unit",
    "normalized_unit",
    "required_condition",
    "observed_status",
    "unit_normalization_decision",
    "next_required_artifact",
    "forbidden_inputs",
    "unit_normalization_written",
    "component_combination_rule_written",
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


def unit_normalization_rows() -> list[dict[str, object]]:
    value_freeze = summary_row("m0_no_dark_velocity_anchor_value_freeze_summary_v08.csv")
    dimensional_trace = summary_row("m0_no_dark_payload_dimensional_trace_summary_v12.csv")
    real_value_gate = summary_row("source_import_real_values_summary_v12.csv")
    leakage_pass = summary_row("leakage_audit_pass_review_summary_v78.csv")
    common_forbidden = (
        "v_obs_km_s;endpoint_residual;heldout_score;family_winner;"
        "best_fit_curve;posthoc_unit_rescale;posthoc_coefficient_fit;"
        "posthoc_component_combination"
    )
    rows = [
        {
            "anchor_unit_check_id": "M0NDVAUN08_VALUE_FREEZE_HANDOFF",
            "anchor_unit_component": "value_freeze_handoff",
            "source_column": "v_gas_km_s;v_disk_km_s;v_bulge_km_s",
            "source_unit": "km/s",
            "normalized_unit": "km/s",
            "required_condition": "value-freeze gate is present and identifies unit normalization as the next blocker",
            "observed_status": value_freeze["overall_status"],
            "unit_normalization_decision": "READY_FOR_ANCHOR_UNIT_NORMALIZATION_REVIEW",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_combination_rule_v08",
        },
        {
            "anchor_unit_check_id": "M0NDVAUN08_GAS_COMPONENT",
            "anchor_unit_component": "source_component_unit",
            "source_column": "v_gas_km_s",
            "source_unit": "km/s",
            "normalized_unit": "km/s",
            "required_condition": "gas component is already a source-side velocity component in km/s",
            "observed_status": real_value_gate["overall_status"],
            "unit_normalization_decision": "ANCHOR_UNIT_NORMALIZATION_DECLARED_NO_RESCALE",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_combination_rule_v08",
        },
        {
            "anchor_unit_check_id": "M0NDVAUN08_DISK_COMPONENT",
            "anchor_unit_component": "source_component_unit",
            "source_column": "v_disk_km_s",
            "source_unit": "km/s",
            "normalized_unit": "km/s",
            "required_condition": "disk component is already a source-side velocity component in km/s",
            "observed_status": real_value_gate["overall_status"],
            "unit_normalization_decision": "ANCHOR_UNIT_NORMALIZATION_DECLARED_NO_RESCALE",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_combination_rule_v08",
        },
        {
            "anchor_unit_check_id": "M0NDVAUN08_BULGE_COMPONENT",
            "anchor_unit_component": "source_component_unit",
            "source_column": "v_bulge_km_s",
            "source_unit": "km/s",
            "normalized_unit": "km/s",
            "required_condition": "bulge component is already a source-side velocity component in km/s",
            "observed_status": real_value_gate["overall_status"],
            "unit_normalization_decision": "ANCHOR_UNIT_NORMALIZATION_DECLARED_NO_RESCALE",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_combination_rule_v08",
        },
        {
            "anchor_unit_check_id": "M0NDVAUN08_DIMENSIONAL_TRACE",
            "anchor_unit_component": "dimensional_trace_guard",
            "source_column": "v_gas_km_s;v_disk_km_s;v_bulge_km_s",
            "source_unit": "km/s",
            "normalized_unit": "km/s",
            "required_condition": "normalization must preserve velocity dimension and cannot introduce a fitted scale",
            "observed_status": dimensional_trace["overall_status"],
            "unit_normalization_decision": "ANCHOR_UNIT_DIMENSIONAL_GUARD_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_combination_rule_v08",
        },
        {
            "anchor_unit_check_id": "M0NDVAUN08_LEAKAGE_GUARD",
            "anchor_unit_component": "leakage_guard",
            "source_column": "v_gas_km_s;v_disk_km_s;v_bulge_km_s",
            "source_unit": "km/s",
            "normalized_unit": "km/s",
            "required_condition": "unit normalization cannot be adjusted from endpoint fit quality",
            "observed_status": leakage_pass["overall_status"],
            "unit_normalization_decision": "ANCHOR_UNIT_LEAKAGE_GUARD_INHERITED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_combination_rule_v08",
        },
        {
            "anchor_unit_check_id": "M0NDVAUN08_COMPONENT_COMBINATION",
            "anchor_unit_component": "component_combination_rule",
            "source_column": "v_gas_km_s;v_disk_km_s;v_bulge_km_s",
            "source_unit": "km/s",
            "normalized_unit": "km/s",
            "required_condition": "a later pre-scoring rule must say how source components may be combined before a velocity formula exists",
            "observed_status": "NO_ANCHOR_COMPONENT_COMBINATION_RULE_PRESENT",
            "unit_normalization_decision": "BLOCKED_COMPONENT_COMBINATION_RULE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_combination_rule_v08",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["unit_normalization_written"] = "true"
        row["component_combination_rule_written"] = "false"
        row["velocity_formula_written"] = "false"
        row["numeric_prediction_rows_written"] = 0
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_velocity_anchor_unit_normalization_gate_only_no_combination_rule_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = sum(str(row["unit_normalization_decision"]).startswith("BLOCKED") for row in rows)
    normalized = sum(
        str(row["unit_normalization_decision"]) == "ANCHOR_UNIT_NORMALIZATION_DECLARED_NO_RESCALE"
        for row in rows
    )
    return [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_ANCHOR_UNIT_NORMALIZATION_V08",
            "anchor_unit_normalization_artifact": "m0_no_dark_velocity_anchor_unit_normalization_v08",
            "unit_normalization_checks": len(rows),
            "source_component_units_normalized": normalized,
            "blocked_unit_normalization_checks": blocked,
            "unit_normalization_written": "true",
            "component_combination_rule_written": "false",
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": 0,
            "families_with_numeric_predictions": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_ANCHOR_UNIT_NORMALIZATION_PRESENT_BLOCKED_COMPONENT_COMBINATION_RULE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_combination_rule_v08",
            "claim_boundary": "m0_no_dark_velocity_anchor_unit_normalization_gate_only_no_component_combination_no_velocity_formula_no_predictions_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_velocity_anchor_unit_normalization_v08.md").write_text(
        """# M0 No-Dark Velocity-Anchor Unit Normalization v08

**Doc class:** velocity-anchor unit-normalization gate
**Status:** unit normalization present; component-combination rule missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_anchor_unit_normalization.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_anchor_unit_normalization_v08.csv
data/derived/m0_no_dark_velocity_anchor_unit_normalization_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_anchor_unit_normalization_v08`
presence blocker by declaring that the frozen SPARC source columns
`v_gas_km_s`, `v_disk_km_s`, and `v_bulge_km_s` are already source-side
velocity components in `km/s`. No posthoc unit rescale is introduced.

The gate does not combine components, does not square components, does not
choose signs or weights, and does not produce a velocity formula. It only
normalizes the source-unit layer before a later component-combination rule.

## Current Result

The expected status is:

```text
M0_NO_DARK_ANCHOR_UNIT_NORMALIZATION_PRESENT_BLOCKED_COMPONENT_COMBINATION_RULE_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_anchor_component_combination_rule_v08
```

## Claim Boundary

This gate declares only source-unit normalization. It does not combine source components, does not compute an anchor value, does not assign coupling normalization, does not write a velocity formula, does not write prediction rows, does not run endpoint scoring, and does not decide whether a dark-sector component is required.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = unit_normalization_rows()
    write_csv(DERIVED / "m0_no_dark_velocity_anchor_unit_normalization_v08.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_velocity_anchor_unit_normalization_summary_v08.csv",
        summary(rows),
        [
            "summary_id",
            "anchor_unit_normalization_artifact",
            "unit_normalization_checks",
            "source_component_units_normalized",
            "blocked_unit_normalization_checks",
            "unit_normalization_written",
            "component_combination_rule_written",
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
    print("PAPER11_M0_NO_DARK_VELOCITY_ANCHOR_UNIT_NORMALIZATION_V08_BUILT")


if __name__ == "__main__":
    main()
