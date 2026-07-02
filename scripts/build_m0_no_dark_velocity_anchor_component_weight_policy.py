#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDNAMES = [
    "weight_policy_check_id",
    "weight_policy_layer",
    "source_columns",
    "weight_symbol_policy",
    "sign_policy",
    "normalization_policy",
    "required_condition",
    "observed_status",
    "weight_policy_decision",
    "next_required_artifact",
    "forbidden_inputs",
    "component_weight_policy_written",
    "component_weight_values_frozen",
    "combined_anchor_values_written",
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


def weight_policy_rows() -> list[dict[str, object]]:
    component_combination = summary_row("m0_no_dark_velocity_anchor_component_combination_rule_summary_v08.csv")
    dimensional_trace = summary_row("m0_no_dark_payload_dimensional_trace_summary_v12.csv")
    leakage_pass = summary_row("leakage_audit_pass_review_summary_v78.csv")
    coefficient_policy = summary_row("m0_no_dark_coefficient_policy_summary_v07.csv")
    source_columns = "v_gas_km_s;v_disk_km_s;v_bulge_km_s"
    common_forbidden = (
        "v_obs_km_s;endpoint_residual;heldout_score;family_winner;best_fit_curve;"
        "posthoc_weight_fit;posthoc_sign_choice;posthoc_normalization;"
        "posthoc_component_combination;numeric_prediction_value"
    )
    rows = [
        {
            "weight_policy_check_id": "M0NDVACWP08_COMPONENT_COMBINATION_HANDOFF",
            "weight_policy_layer": "component_combination_handoff",
            "source_columns": source_columns,
            "weight_symbol_policy": "dimensionless_pre_scoring_weight_symbols_only",
            "sign_policy": "pre_scoring_sign_policy_required_no_endpoint_choice",
            "normalization_policy": "dimensionless_pre_scoring_normalization_only",
            "required_condition": "component-combination rule is present and identifies component-weight policy as the next blocker",
            "observed_status": component_combination["overall_status"],
            "weight_policy_decision": "READY_FOR_COMPONENT_WEIGHT_POLICY_REVIEW",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_weight_value_freeze_v08",
        },
        {
            "weight_policy_check_id": "M0NDVACWP08_WEIGHT_SYMBOL_CLASS",
            "weight_policy_layer": "weight_symbol_class",
            "source_columns": source_columns,
            "weight_symbol_policy": "dimensionless_symbols_attached_to_frozen_source_components",
            "sign_policy": "not_numerically_chosen_here",
            "normalization_policy": "not_numerically_chosen_here",
            "required_condition": "weights may only be symbolic source-side component modifiers before value freeze",
            "observed_status": coefficient_policy["overall_status"],
            "weight_policy_decision": "COMPONENT_WEIGHT_SYMBOL_POLICY_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_weight_value_freeze_v08",
        },
        {
            "weight_policy_check_id": "M0NDVACWP08_SIGN_POLICY_CLASS",
            "weight_policy_layer": "sign_policy_class",
            "source_columns": source_columns,
            "weight_symbol_policy": "no_numeric_weight_values",
            "sign_policy": "pre_scoring_sign_rule_required_no_endpoint_sign_choice",
            "normalization_policy": "not_numerically_chosen_here",
            "required_condition": "any signs must be declared before scoring and cannot be chosen from fit quality",
            "observed_status": leakage_pass["overall_status"],
            "weight_policy_decision": "COMPONENT_SIGN_POLICY_CLASS_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_weight_value_freeze_v08",
        },
        {
            "weight_policy_check_id": "M0NDVACWP08_NORMALIZATION_POLICY_CLASS",
            "weight_policy_layer": "normalization_policy_class",
            "source_columns": source_columns,
            "weight_symbol_policy": "dimensionless_symbols_only",
            "sign_policy": "pre_scoring_sign_rule_required",
            "normalization_policy": "dimensionless_no_posthoc_amplitude_fit",
            "required_condition": "normalization must be dimensionless and cannot be fitted from endpoint performance",
            "observed_status": dimensional_trace["overall_status"],
            "weight_policy_decision": "COMPONENT_NORMALIZATION_POLICY_CLASS_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_weight_value_freeze_v08",
        },
        {
            "weight_policy_check_id": "M0NDVACWP08_LEAKAGE_GUARD",
            "weight_policy_layer": "weight_policy_leakage_guard",
            "source_columns": source_columns,
            "weight_symbol_policy": "no_endpoint_feedback",
            "sign_policy": "no_endpoint_feedback",
            "normalization_policy": "no_endpoint_feedback",
            "required_condition": "weight policy cannot use observed velocities, residuals, heldout scores, best-fit curves, or family winners",
            "observed_status": leakage_pass["overall_status"],
            "weight_policy_decision": "COMPONENT_WEIGHT_LEAKAGE_GUARD_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_weight_value_freeze_v08",
        },
        {
            "weight_policy_check_id": "M0NDVACWP08_VALUE_FREEZE",
            "weight_policy_layer": "component_weight_value_freeze",
            "source_columns": source_columns,
            "weight_symbol_policy": "no_numeric_weight_values_frozen",
            "sign_policy": "no_numeric_sign_values_frozen",
            "normalization_policy": "no_numeric_normalization_frozen",
            "required_condition": "a later pre-scoring artifact must freeze actual symbolic or numeric component-weight values before combined anchors can be written",
            "observed_status": "NO_COMPONENT_WEIGHT_VALUE_FREEZE_PRESENT",
            "weight_policy_decision": "BLOCKED_COMPONENT_WEIGHT_VALUE_FREEZE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_weight_value_freeze_v08",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["component_weight_policy_written"] = "true"
        row["component_weight_values_frozen"] = "false"
        row["combined_anchor_values_written"] = 0
        row["velocity_formula_written"] = "false"
        row["numeric_prediction_rows_written"] = 0
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_velocity_anchor_component_weight_policy_only_no_weight_values_no_formula_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = sum(str(row["weight_policy_decision"]).startswith("BLOCKED") for row in rows)
    declared = sum(str(row["weight_policy_decision"]).endswith("_DECLARED") for row in rows)
    return [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_ANCHOR_COMPONENT_WEIGHT_POLICY_V08",
            "anchor_component_weight_policy_artifact": "m0_no_dark_velocity_anchor_component_weight_policy_v08",
            "component_weight_policy_checks": len(rows),
            "declared_component_weight_policy_guards": declared,
            "blocked_component_weight_policy_checks": blocked,
            "component_weight_policy_written": "true",
            "component_weight_values_frozen": "false",
            "combined_anchor_values_written": 0,
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": 0,
            "families_with_numeric_predictions": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_ANCHOR_COMPONENT_WEIGHT_POLICY_PRESENT_BLOCKED_WEIGHT_VALUE_FREEZE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_weight_value_freeze_v08",
            "claim_boundary": "m0_no_dark_velocity_anchor_component_weight_policy_only_no_weight_value_freeze_no_combined_values_no_velocity_formula_no_predictions_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_velocity_anchor_component_weight_policy_v08.md").write_text(
        """# M0 No-Dark Velocity-Anchor Component Weight Policy v08

**Doc class:** velocity-anchor component-weight policy gate
**Status:** component-weight policy present; weight-value freeze missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_anchor_component_weight_policy.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_anchor_component_weight_policy_v08.csv
data/derived/m0_no_dark_velocity_anchor_component_weight_policy_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_anchor_component_weight_policy_v08`
presence blocker by declaring the admissible policy class for weights, signs,
and normalization on the frozen source-side components:

```text
v_gas_km_s;v_disk_km_s;v_bulge_km_s
```

The policy is deliberately non-numeric. It requires any later weights, signs,
or normalization to be fixed before scoring, dimensionless where they modify
velocity components, and independent of observed velocities, endpoint
residuals, heldout scores, family winners, best-fit curves, or posthoc fit
quality.

The gate does not freeze component-weight values, does not compute combined
anchor values, and does not produce a velocity formula. Those choices require a
later pre-scoring component-weight value-freeze artifact.

## Current Result

The expected status is:

```text
M0_NO_DARK_ANCHOR_COMPONENT_WEIGHT_POLICY_PRESENT_BLOCKED_WEIGHT_VALUE_FREEZE_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_anchor_component_weight_value_freeze_v08
```

## Claim Boundary

This gate declares only an admissible source-side component-weight policy
class. It does not freeze actual weight values, does not compute combined
anchor values, does not write a velocity formula, does not write prediction
rows, does not run endpoint scoring, and does not decide whether a dark-sector
component is required.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = weight_policy_rows()
    write_csv(DERIVED / "m0_no_dark_velocity_anchor_component_weight_policy_v08.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_velocity_anchor_component_weight_policy_summary_v08.csv",
        summary(rows),
        [
            "summary_id",
            "anchor_component_weight_policy_artifact",
            "component_weight_policy_checks",
            "declared_component_weight_policy_guards",
            "blocked_component_weight_policy_checks",
            "component_weight_policy_written",
            "component_weight_values_frozen",
            "combined_anchor_values_written",
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
    print("PAPER11_M0_NO_DARK_VELOCITY_ANCHOR_COMPONENT_WEIGHT_POLICY_V08_BUILT")


if __name__ == "__main__":
    main()
