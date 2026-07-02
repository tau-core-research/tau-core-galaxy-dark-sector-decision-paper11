#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDNAMES = [
    "component_rule_check_id",
    "component_rule_layer",
    "source_columns",
    "allowed_operation_class",
    "required_condition",
    "observed_status",
    "component_combination_decision",
    "next_required_artifact",
    "forbidden_inputs",
    "component_combination_rule_written",
    "component_weight_policy_written",
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


def component_combination_rows() -> list[dict[str, object]]:
    unit_normalization = summary_row("m0_no_dark_velocity_anchor_unit_normalization_summary_v08.csv")
    dimensional_trace = summary_row("m0_no_dark_payload_dimensional_trace_summary_v12.csv")
    leakage_pass = summary_row("leakage_audit_pass_review_summary_v78.csv")
    real_value_gate = summary_row("source_import_real_values_summary_v12.csv")
    source_columns = "v_gas_km_s;v_disk_km_s;v_bulge_km_s"
    common_forbidden = (
        "v_obs_km_s;endpoint_residual;heldout_score;family_winner;best_fit_curve;"
        "posthoc_component_combination;posthoc_weight_fit;posthoc_sign_choice;"
        "posthoc_unit_rescale;numeric_prediction_value"
    )
    rows = [
        {
            "component_rule_check_id": "M0NDVACCR08_UNIT_NORMALIZATION_HANDOFF",
            "component_rule_layer": "unit_normalization_handoff",
            "source_columns": source_columns,
            "allowed_operation_class": "source_columns_only_no_numeric_combination",
            "required_condition": "unit-normalization gate is present and identifies component combination as the next blocker",
            "observed_status": unit_normalization["overall_status"],
            "component_combination_decision": "READY_FOR_COMPONENT_COMBINATION_RULE_REVIEW",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_weight_policy_v08",
        },
        {
            "component_rule_check_id": "M0NDVACCR08_SOURCE_COMPONENT_DOMAIN",
            "component_rule_layer": "source_component_domain",
            "source_columns": source_columns,
            "allowed_operation_class": "frozen_source_component_domain",
            "required_condition": "component-combination rule may use only the frozen source-side velocity components",
            "observed_status": real_value_gate["overall_status"],
            "component_combination_decision": "SOURCE_COMPONENT_DOMAIN_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_weight_policy_v08",
        },
        {
            "component_rule_check_id": "M0NDVACCR08_DIMENSIONAL_HOMOGENEITY",
            "component_rule_layer": "dimensional_homogeneity",
            "source_columns": source_columns,
            "allowed_operation_class": "velocity_dimension_preserving_combination_class",
            "required_condition": "any later combination must preserve velocity dimension and cannot introduce a fitted scale",
            "observed_status": dimensional_trace["overall_status"],
            "component_combination_decision": "DIMENSIONAL_COMBINATION_GUARD_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_weight_policy_v08",
        },
        {
            "component_rule_check_id": "M0NDVACCR08_SOURCE_SIDE_ONLY",
            "component_rule_layer": "source_side_only_guard",
            "source_columns": source_columns,
            "allowed_operation_class": "no_observed_velocity_no_endpoint_feedback",
            "required_condition": "combination policy cannot be selected from observed velocity, residuals, heldout score, or family winner",
            "observed_status": leakage_pass["overall_status"],
            "component_combination_decision": "SOURCE_SIDE_ONLY_GUARD_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_weight_policy_v08",
        },
        {
            "component_rule_check_id": "M0NDVACCR08_RULE_CLASS",
            "component_rule_layer": "combination_rule_class",
            "source_columns": source_columns,
            "allowed_operation_class": "pre_scoring_structural_combination_rule_required",
            "required_condition": "component operation class is declared only as a pre-scoring structural rule slot, not as a numeric formula",
            "observed_status": "COMBINATION_RULE_CLASS_DECLARED_NO_VALUES",
            "component_combination_decision": "COMPONENT_COMBINATION_RULE_CLASS_PRESENT",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_weight_policy_v08",
        },
        {
            "component_rule_check_id": "M0NDVACCR08_WEIGHT_POLICY",
            "component_rule_layer": "component_weight_policy",
            "source_columns": source_columns,
            "allowed_operation_class": "no_weights_or_signs_declared",
            "required_condition": "a later pre-scoring policy must declare allowed component weights, signs, and normalization before any combined anchor value exists",
            "observed_status": "NO_COMPONENT_WEIGHT_POLICY_PRESENT",
            "component_combination_decision": "BLOCKED_COMPONENT_WEIGHT_POLICY_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_weight_policy_v08",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["component_combination_rule_written"] = "true"
        row["component_weight_policy_written"] = "false"
        row["combined_anchor_values_written"] = 0
        row["velocity_formula_written"] = "false"
        row["numeric_prediction_rows_written"] = 0
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_velocity_anchor_component_combination_rule_only_no_weights_no_formula_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = sum(str(row["component_combination_decision"]).startswith("BLOCKED") for row in rows)
    declared = sum(
        str(row["component_combination_decision"])
        in {
            "SOURCE_COMPONENT_DOMAIN_DECLARED",
            "DIMENSIONAL_COMBINATION_GUARD_DECLARED",
            "SOURCE_SIDE_ONLY_GUARD_DECLARED",
            "COMPONENT_COMBINATION_RULE_CLASS_PRESENT",
        }
        for row in rows
    )
    return [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_ANCHOR_COMPONENT_COMBINATION_RULE_V08",
            "anchor_component_combination_artifact": "m0_no_dark_velocity_anchor_component_combination_rule_v08",
            "component_combination_checks": len(rows),
            "declared_component_combination_guards": declared,
            "blocked_component_combination_checks": blocked,
            "component_combination_rule_written": "true",
            "component_weight_policy_written": "false",
            "combined_anchor_values_written": 0,
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": 0,
            "families_with_numeric_predictions": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_ANCHOR_COMPONENT_COMBINATION_RULE_PRESENT_BLOCKED_COMPONENT_WEIGHT_POLICY_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_component_weight_policy_v08",
            "claim_boundary": "m0_no_dark_velocity_anchor_component_combination_rule_only_no_weight_policy_no_combined_values_no_velocity_formula_no_predictions_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_velocity_anchor_component_combination_rule_v08.md").write_text(
        """# M0 No-Dark Velocity-Anchor Component Combination Rule v08

**Doc class:** velocity-anchor component-combination rule gate
**Status:** component-combination rule class present; component-weight policy missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_anchor_component_combination_rule.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_anchor_component_combination_rule_v08.csv
data/derived/m0_no_dark_velocity_anchor_component_combination_rule_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_anchor_component_combination_rule_v08`
presence blocker by declaring the allowed source-side combination-rule layer for
the frozen velocity-anchor components:

```text
v_gas_km_s;v_disk_km_s;v_bulge_km_s
```

The rule is deliberately structural. It says the later no-dark anchor may only
combine frozen source-side velocity components, must preserve velocity
dimension, and must not choose its operation from observed velocity, endpoint
residuals, heldout scores, family winners, best-fit curves, or posthoc
component choices.

The gate does not choose component weights, signs, normalization, a combined
anchor value, or a velocity formula. Those choices require a later pre-scoring
component-weight policy.

## Current Result

The expected status is:

```text
M0_NO_DARK_ANCHOR_COMPONENT_COMBINATION_RULE_PRESENT_BLOCKED_COMPONENT_WEIGHT_POLICY_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_anchor_component_weight_policy_v08
```

## Claim Boundary

This gate declares only a source-side structural component-combination rule
class. It does not set weights, signs, or normalization, does not compute
combined anchor values, does not write a velocity formula, does not write
prediction rows, does not run endpoint scoring, and does not decide whether a
dark-sector component is required.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = component_combination_rows()
    write_csv(DERIVED / "m0_no_dark_velocity_anchor_component_combination_rule_v08.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_velocity_anchor_component_combination_rule_summary_v08.csv",
        summary(rows),
        [
            "summary_id",
            "anchor_component_combination_artifact",
            "component_combination_checks",
            "declared_component_combination_guards",
            "blocked_component_combination_checks",
            "component_combination_rule_written",
            "component_weight_policy_written",
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
    print("PAPER11_M0_NO_DARK_VELOCITY_ANCHOR_COMPONENT_COMBINATION_RULE_V08_BUILT")


if __name__ == "__main__":
    main()
