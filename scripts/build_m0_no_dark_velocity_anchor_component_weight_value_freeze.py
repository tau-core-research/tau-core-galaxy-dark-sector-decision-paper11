#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDNAMES = [
    "weight_value_freeze_id",
    "weight_value_layer",
    "source_columns",
    "frozen_symbol_slots",
    "frozen_value_kind",
    "required_condition",
    "observed_status",
    "weight_value_freeze_decision",
    "next_required_artifact",
    "forbidden_inputs",
    "component_weight_values_frozen",
    "numeric_weight_values_written",
    "combined_anchor_rule_written",
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


def weight_value_freeze_rows() -> list[dict[str, object]]:
    weight_policy = summary_row("m0_no_dark_velocity_anchor_component_weight_policy_summary_v08.csv")
    coefficient_policy = summary_row("m0_no_dark_coefficient_policy_summary_v07.csv")
    dimensional_trace = summary_row("m0_no_dark_payload_dimensional_trace_summary_v12.csv")
    leakage_pass = summary_row("leakage_audit_pass_review_summary_v78.csv")
    source_columns = "v_gas_km_s;v_disk_km_s;v_bulge_km_s"
    common_forbidden = (
        "v_obs_km_s;endpoint_residual;heldout_score;family_winner;best_fit_curve;"
        "posthoc_weight_fit;posthoc_sign_choice;posthoc_normalization;"
        "posthoc_combined_anchor_value;numeric_prediction_value"
    )
    rows = [
        {
            "weight_value_freeze_id": "M0NDVACWVF08_WEIGHT_POLICY_HANDOFF",
            "weight_value_layer": "component_weight_policy_handoff",
            "source_columns": source_columns,
            "frozen_symbol_slots": "w_gas;w_disk;w_bulge;s_gas;s_disk;s_bulge;n_anchor",
            "frozen_value_kind": "symbolic_slots_only_no_numeric_values",
            "required_condition": "component-weight policy is present and identifies weight-value freeze as the next blocker",
            "observed_status": weight_policy["overall_status"],
            "weight_value_freeze_decision": "READY_FOR_COMPONENT_WEIGHT_VALUE_FREEZE_REVIEW",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_rule_v08",
        },
        {
            "weight_value_freeze_id": "M0NDVACWVF08_WEIGHT_SYMBOL_SLOTS",
            "weight_value_layer": "weight_symbol_slots",
            "source_columns": source_columns,
            "frozen_symbol_slots": "w_gas;w_disk;w_bulge",
            "frozen_value_kind": "dimensionless_weight_symbols",
            "required_condition": "weight slots are frozen as symbolic source-side modifiers, not endpoint-fitted numbers",
            "observed_status": coefficient_policy["overall_status"],
            "weight_value_freeze_decision": "WEIGHT_SYMBOL_SLOTS_FROZEN_NO_NUMERIC_VALUES",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_rule_v08",
        },
        {
            "weight_value_freeze_id": "M0NDVACWVF08_SIGN_SYMBOL_SLOTS",
            "weight_value_layer": "sign_symbol_slots",
            "source_columns": source_columns,
            "frozen_symbol_slots": "s_gas;s_disk;s_bulge",
            "frozen_value_kind": "sign_symbol_slots",
            "required_condition": "sign slots are frozen as pre-scoring symbolic slots and cannot be selected from fit quality",
            "observed_status": leakage_pass["overall_status"],
            "weight_value_freeze_decision": "SIGN_SYMBOL_SLOTS_FROZEN_NO_SIGN_VALUES",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_rule_v08",
        },
        {
            "weight_value_freeze_id": "M0NDVACWVF08_NORMALIZATION_SLOT",
            "weight_value_layer": "normalization_symbol_slot",
            "source_columns": source_columns,
            "frozen_symbol_slots": "n_anchor",
            "frozen_value_kind": "dimensionless_normalization_symbol",
            "required_condition": "normalization slot is frozen symbolically and cannot be tuned from endpoint performance",
            "observed_status": dimensional_trace["overall_status"],
            "weight_value_freeze_decision": "NORMALIZATION_SYMBOL_SLOT_FROZEN_NO_NUMERIC_VALUE",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_rule_v08",
        },
        {
            "weight_value_freeze_id": "M0NDVACWVF08_LEAKAGE_GUARD",
            "weight_value_layer": "weight_value_leakage_guard",
            "source_columns": source_columns,
            "frozen_symbol_slots": "w_gas;w_disk;w_bulge;s_gas;s_disk;s_bulge;n_anchor",
            "frozen_value_kind": "source_side_symbolic_freeze_only",
            "required_condition": "frozen slots cannot be derived from observed velocity, residuals, heldout scores, best-fit curves, or family winners",
            "observed_status": leakage_pass["overall_status"],
            "weight_value_freeze_decision": "WEIGHT_VALUE_FREEZE_LEAKAGE_GUARD_DECLARED",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_rule_v08",
        },
        {
            "weight_value_freeze_id": "M0NDVACWVF08_COMBINED_ANCHOR_RULE",
            "weight_value_layer": "combined_anchor_rule",
            "source_columns": source_columns,
            "frozen_symbol_slots": "w_gas;w_disk;w_bulge;s_gas;s_disk;s_bulge;n_anchor",
            "frozen_value_kind": "no_combined_anchor_rule",
            "required_condition": "a later pre-scoring rule must specify how frozen symbolic slots enter a combined anchor before any anchor value exists",
            "observed_status": "NO_COMBINED_ANCHOR_RULE_PRESENT",
            "weight_value_freeze_decision": "BLOCKED_COMBINED_ANCHOR_RULE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_rule_v08",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["component_weight_values_frozen"] = "true"
        row["numeric_weight_values_written"] = 0
        row["combined_anchor_rule_written"] = "false"
        row["combined_anchor_values_written"] = 0
        row["velocity_formula_written"] = "false"
        row["numeric_prediction_rows_written"] = 0
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_velocity_anchor_component_weight_value_freeze_only_symbolic_no_combined_anchor_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = sum(str(row["weight_value_freeze_decision"]).startswith("BLOCKED") for row in rows)
    frozen = sum("FROZEN" in str(row["weight_value_freeze_decision"]) for row in rows)
    return [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_ANCHOR_COMPONENT_WEIGHT_VALUE_FREEZE_V08",
            "anchor_component_weight_value_freeze_artifact": "m0_no_dark_velocity_anchor_component_weight_value_freeze_v08",
            "component_weight_value_freeze_checks": len(rows),
            "symbolic_weight_value_slots_frozen": frozen,
            "blocked_component_weight_value_freeze_checks": blocked,
            "component_weight_values_frozen": "true",
            "numeric_weight_values_written": 0,
            "combined_anchor_rule_written": "false",
            "combined_anchor_values_written": 0,
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": 0,
            "families_with_numeric_predictions": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_ANCHOR_COMPONENT_WEIGHT_VALUE_FREEZE_PRESENT_BLOCKED_COMBINED_ANCHOR_RULE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_rule_v08",
            "claim_boundary": "m0_no_dark_velocity_anchor_component_weight_value_freeze_only_symbolic_slots_no_combined_values_no_velocity_formula_no_predictions_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_velocity_anchor_component_weight_value_freeze_v08.md").write_text(
        """# M0 No-Dark Velocity-Anchor Component Weight Value Freeze v08

**Doc class:** velocity-anchor component-weight value-freeze gate
**Status:** symbolic weight-value slots frozen; combined-anchor rule missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_anchor_component_weight_value_freeze.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_anchor_component_weight_value_freeze_v08.csv
data/derived/m0_no_dark_velocity_anchor_component_weight_value_freeze_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_anchor_component_weight_value_freeze_v08`
presence blocker by freezing the allowed symbolic slots for the source-side
component weights, signs, and normalization:

```text
w_gas;w_disk;w_bulge;s_gas;s_disk;s_bulge;n_anchor
```

The freeze is symbolic and pre-scoring. It writes no numeric weight values and
does not choose signs or normalization from observed velocities, endpoint
residuals, heldout scores, family winners, best-fit curves, or posthoc fit
quality.

The gate does not specify how the frozen symbolic slots are combined into an
anchor expression. That requires a later pre-scoring combined-anchor rule.

## Current Result

The expected status is:

```text
M0_NO_DARK_ANCHOR_COMPONENT_WEIGHT_VALUE_FREEZE_PRESENT_BLOCKED_COMBINED_ANCHOR_RULE_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_anchor_combined_anchor_rule_v08
```

## Claim Boundary

This gate freezes only symbolic source-side component-weight slots. It does not
write numeric weight values, does not compute combined anchor values, does not
write a velocity formula, does not write prediction rows, does not run endpoint
scoring, and does not decide whether a dark-sector component is required.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = weight_value_freeze_rows()
    write_csv(DERIVED / "m0_no_dark_velocity_anchor_component_weight_value_freeze_v08.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_velocity_anchor_component_weight_value_freeze_summary_v08.csv",
        summary(rows),
        [
            "summary_id",
            "anchor_component_weight_value_freeze_artifact",
            "component_weight_value_freeze_checks",
            "symbolic_weight_value_slots_frozen",
            "blocked_component_weight_value_freeze_checks",
            "component_weight_values_frozen",
            "numeric_weight_values_written",
            "combined_anchor_rule_written",
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
    print("PAPER11_M0_NO_DARK_VELOCITY_ANCHOR_COMPONENT_WEIGHT_VALUE_FREEZE_V08_BUILT")


if __name__ == "__main__":
    main()
