#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDNAMES = [
    "combined_anchor_rule_id",
    "combined_anchor_layer",
    "source_columns",
    "symbolic_slots",
    "allowed_symbolic_rule_class",
    "required_condition",
    "observed_status",
    "combined_anchor_rule_decision",
    "next_required_artifact",
    "forbidden_inputs",
    "combined_anchor_rule_written",
    "combined_anchor_expression_written",
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


def combined_anchor_rule_rows() -> list[dict[str, object]]:
    value_freeze = summary_row("m0_no_dark_velocity_anchor_component_weight_value_freeze_summary_v08.csv")
    component_rule = summary_row("m0_no_dark_velocity_anchor_component_combination_rule_summary_v08.csv")
    dimensional_trace = summary_row("m0_no_dark_payload_dimensional_trace_summary_v12.csv")
    leakage_pass = summary_row("leakage_audit_pass_review_summary_v78.csv")
    source_columns = "v_gas_km_s;v_disk_km_s;v_bulge_km_s"
    symbolic_slots = "w_gas;w_disk;w_bulge;s_gas;s_disk;s_bulge;n_anchor"
    common_forbidden = (
        "v_obs_km_s;endpoint_residual;heldout_score;family_winner;best_fit_curve;"
        "posthoc_combined_anchor_value;posthoc_formula_switch;posthoc_weight_fit;"
        "numeric_prediction_value"
    )
    rows = [
        {
            "combined_anchor_rule_id": "M0NDVACAR08_WEIGHT_VALUE_FREEZE_HANDOFF",
            "combined_anchor_layer": "weight_value_freeze_handoff",
            "source_columns": source_columns,
            "symbolic_slots": symbolic_slots,
            "allowed_symbolic_rule_class": "source_side_symbolic_anchor_expression_class",
            "required_condition": "component-weight value freeze is present and identifies combined-anchor rule as the next blocker",
            "observed_status": value_freeze["overall_status"],
            "combined_anchor_rule_decision": "READY_FOR_COMBINED_ANCHOR_RULE_REVIEW",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08",
        },
        {
            "combined_anchor_rule_id": "M0NDVACAR08_SOURCE_COMPONENT_BINDING",
            "combined_anchor_layer": "source_component_binding",
            "source_columns": source_columns,
            "symbolic_slots": symbolic_slots,
            "allowed_symbolic_rule_class": "each_frozen_source_component_may_bind_only_to_its_symbolic_weight_and_sign_slots",
            "required_condition": "combined-anchor rule binds only frozen source components to frozen symbolic slots",
            "observed_status": component_rule["overall_status"],
            "combined_anchor_rule_decision": "SOURCE_COMPONENT_BINDING_RULE_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08",
        },
        {
            "combined_anchor_rule_id": "M0NDVACAR08_DIMENSIONAL_CLASS",
            "combined_anchor_layer": "dimensional_rule_class",
            "source_columns": source_columns,
            "symbolic_slots": symbolic_slots,
            "allowed_symbolic_rule_class": "velocity_dimension_preserving_symbolic_anchor_class",
            "required_condition": "combined anchor expression class must preserve km/s before any later readout formula",
            "observed_status": dimensional_trace["overall_status"],
            "combined_anchor_rule_decision": "DIMENSIONAL_ANCHOR_RULE_CLASS_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08",
        },
        {
            "combined_anchor_rule_id": "M0NDVACAR08_LEAKAGE_GUARD",
            "combined_anchor_layer": "combined_anchor_leakage_guard",
            "source_columns": source_columns,
            "symbolic_slots": symbolic_slots,
            "allowed_symbolic_rule_class": "no_endpoint_feedback_in_anchor_rule",
            "required_condition": "combined-anchor rule cannot be chosen from observed velocity, residuals, heldout score, best-fit curve, or family winner",
            "observed_status": leakage_pass["overall_status"],
            "combined_anchor_rule_decision": "COMBINED_ANCHOR_LEAKAGE_GUARD_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08",
        },
        {
            "combined_anchor_rule_id": "M0NDVACAR08_RULE_CLASS",
            "combined_anchor_layer": "symbolic_rule_class",
            "source_columns": source_columns,
            "symbolic_slots": symbolic_slots,
            "allowed_symbolic_rule_class": "pre_scoring_symbolic_expression_rule_required_no_values",
            "required_condition": "rule class may specify only symbolic expression structure, not evaluated anchor values",
            "observed_status": "COMBINED_ANCHOR_RULE_CLASS_DECLARED_NO_VALUES",
            "combined_anchor_rule_decision": "COMBINED_ANCHOR_RULE_CLASS_PRESENT",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08",
        },
        {
            "combined_anchor_rule_id": "M0NDVACAR08_EXPRESSION_FREEZE",
            "combined_anchor_layer": "combined_anchor_expression_freeze",
            "source_columns": source_columns,
            "symbolic_slots": symbolic_slots,
            "allowed_symbolic_rule_class": "no_frozen_combined_anchor_expression",
            "required_condition": "a later artifact must freeze the exact symbolic combined-anchor expression before values can be written",
            "observed_status": "NO_COMBINED_ANCHOR_EXPRESSION_FREEZE_PRESENT",
            "combined_anchor_rule_decision": "BLOCKED_COMBINED_ANCHOR_EXPRESSION_FREEZE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["combined_anchor_rule_written"] = "true"
        row["combined_anchor_expression_written"] = "false"
        row["combined_anchor_values_written"] = 0
        row["velocity_formula_written"] = "false"
        row["numeric_prediction_rows_written"] = 0
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_velocity_anchor_combined_anchor_rule_only_no_expression_no_values_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = sum(str(row["combined_anchor_rule_decision"]).startswith("BLOCKED") for row in rows)
    declared = sum(str(row["combined_anchor_rule_decision"]).endswith("_DECLARED") for row in rows)
    return [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_ANCHOR_COMBINED_ANCHOR_RULE_V08",
            "anchor_combined_anchor_rule_artifact": "m0_no_dark_velocity_anchor_combined_anchor_rule_v08",
            "combined_anchor_rule_checks": len(rows),
            "declared_combined_anchor_rule_guards": declared,
            "blocked_combined_anchor_rule_checks": blocked,
            "combined_anchor_rule_written": "true",
            "combined_anchor_expression_written": "false",
            "combined_anchor_values_written": 0,
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": 0,
            "families_with_numeric_predictions": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_ANCHOR_COMBINED_ANCHOR_RULE_PRESENT_BLOCKED_EXPRESSION_FREEZE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08",
            "claim_boundary": "m0_no_dark_velocity_anchor_combined_anchor_rule_only_no_expression_freeze_no_combined_values_no_velocity_formula_no_predictions_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_velocity_anchor_combined_anchor_rule_v08.md").write_text(
        """# M0 No-Dark Velocity-Anchor Combined Anchor Rule v08

**Doc class:** velocity-anchor combined-anchor rule gate
**Status:** combined-anchor rule class present; expression freeze missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_anchor_combined_anchor_rule.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_anchor_combined_anchor_rule_v08.csv
data/derived/m0_no_dark_velocity_anchor_combined_anchor_rule_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_anchor_combined_anchor_rule_v08`
presence blocker by declaring the admissible symbolic rule class for combining
the frozen source-side velocity components with the frozen symbolic slots:

```text
v_gas_km_s;v_disk_km_s;v_bulge_km_s
w_gas;w_disk;w_bulge;s_gas;s_disk;s_bulge;n_anchor
```

The rule is structural and pre-scoring. It permits only source-side symbolic
binding, preserves velocity dimension, and forbids endpoint feedback from
observed velocities, residuals, heldout scores, family winners, best-fit
curves, or posthoc fit quality.

The gate does not freeze the exact symbolic expression, evaluate combined
anchor values, or write a velocity formula. Those choices require a later
combined-anchor expression-freeze artifact.

## Current Result

The expected status is:

```text
M0_NO_DARK_ANCHOR_COMBINED_ANCHOR_RULE_PRESENT_BLOCKED_EXPRESSION_FREEZE_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08
```

## Claim Boundary

This gate declares only the admissible source-side symbolic combined-anchor
rule class. It does not freeze the exact expression, does not compute combined
anchor values, does not write a velocity formula, does not write prediction
rows, does not run endpoint scoring, and does not decide whether a dark-sector
component is required.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = combined_anchor_rule_rows()
    write_csv(DERIVED / "m0_no_dark_velocity_anchor_combined_anchor_rule_v08.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_velocity_anchor_combined_anchor_rule_summary_v08.csv",
        summary(rows),
        [
            "summary_id",
            "anchor_combined_anchor_rule_artifact",
            "combined_anchor_rule_checks",
            "declared_combined_anchor_rule_guards",
            "blocked_combined_anchor_rule_checks",
            "combined_anchor_rule_written",
            "combined_anchor_expression_written",
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
    print("PAPER11_M0_NO_DARK_VELOCITY_ANCHOR_COMBINED_ANCHOR_RULE_V08_BUILT")


if __name__ == "__main__":
    main()
