#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDNAMES = [
    "expression_freeze_id",
    "expression_layer",
    "source_columns",
    "symbolic_slots",
    "frozen_expression",
    "dimensional_class",
    "required_condition",
    "observed_status",
    "expression_freeze_decision",
    "next_required_artifact",
    "forbidden_inputs",
    "combined_anchor_expression_frozen",
    "combined_anchor_values_written",
    "velocity_formula_written",
    "numeric_prediction_rows_written",
    "endpoint_scoring_allowed",
    "claim_boundary",
]


FROZEN_EXPRESSION = (
    "v_anchor_sq_km2_s2 = "
    "(s_gas*w_gas*v_gas_km_s^2 + "
    "s_disk*w_disk*v_disk_km_s^2 + "
    "s_bulge*w_bulge*v_bulge_km_s^2) / n_anchor"
)


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


def expression_freeze_rows() -> list[dict[str, object]]:
    combined_rule = summary_row("m0_no_dark_velocity_anchor_combined_anchor_rule_summary_v08.csv")
    value_freeze = summary_row("m0_no_dark_velocity_anchor_component_weight_value_freeze_summary_v08.csv")
    dimensional_trace = summary_row("m0_no_dark_payload_dimensional_trace_summary_v12.csv")
    leakage_pass = summary_row("leakage_audit_pass_review_summary_v78.csv")
    source_columns = "v_gas_km_s;v_disk_km_s;v_bulge_km_s"
    symbolic_slots = "w_gas;w_disk;w_bulge;s_gas;s_disk;s_bulge;n_anchor"
    common_forbidden = (
        "v_obs_km_s;endpoint_residual;heldout_score;family_winner;best_fit_curve;"
        "posthoc_combined_anchor_value;posthoc_formula_switch;posthoc_weight_fit;"
        "posthoc_sign_choice;posthoc_normalization;numeric_prediction_value"
    )
    rows = [
        {
            "expression_freeze_id": "M0NDVACAEF08_RULE_HANDOFF",
            "expression_layer": "combined_anchor_rule_handoff",
            "source_columns": source_columns,
            "symbolic_slots": symbolic_slots,
            "frozen_expression": FROZEN_EXPRESSION,
            "dimensional_class": "velocity_squared_anchor_expression",
            "required_condition": "combined-anchor rule is present and identifies expression freeze as the next blocker",
            "observed_status": combined_rule["overall_status"],
            "expression_freeze_decision": "READY_FOR_COMBINED_ANCHOR_EXPRESSION_FREEZE_REVIEW",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08",
        },
        {
            "expression_freeze_id": "M0NDVACAEF08_SOURCE_COMPONENTS",
            "expression_layer": "source_component_expression",
            "source_columns": source_columns,
            "symbolic_slots": symbolic_slots,
            "frozen_expression": FROZEN_EXPRESSION,
            "dimensional_class": "squared_source_velocity_components_only",
            "required_condition": "expression may use only frozen source-side baryonic velocity components",
            "observed_status": value_freeze["overall_status"],
            "expression_freeze_decision": "SOURCE_COMPONENT_EXPRESSION_FROZEN",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08",
        },
        {
            "expression_freeze_id": "M0NDVACAEF08_SYMBOL_BINDING",
            "expression_layer": "symbol_binding",
            "source_columns": source_columns,
            "symbolic_slots": symbolic_slots,
            "frozen_expression": FROZEN_EXPRESSION,
            "dimensional_class": "dimensionless_symbolic_modifiers",
            "required_condition": "each component is modified only by its frozen symbolic weight and sign slots",
            "observed_status": value_freeze["overall_status"],
            "expression_freeze_decision": "SYMBOLIC_SLOT_BINDING_FROZEN",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08",
        },
        {
            "expression_freeze_id": "M0NDVACAEF08_DIMENSIONAL_AUDIT",
            "expression_layer": "dimensional_audit",
            "source_columns": source_columns,
            "symbolic_slots": symbolic_slots,
            "frozen_expression": FROZEN_EXPRESSION,
            "dimensional_class": "km2_s2_anchor_body_with_dimensionless_normalization",
            "required_condition": "squared velocity terms divided by dimensionless n_anchor preserve velocity-squared units",
            "observed_status": dimensional_trace["overall_status"],
            "expression_freeze_decision": "DIMENSIONAL_EXPRESSION_CLASS_FROZEN",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08",
        },
        {
            "expression_freeze_id": "M0NDVACAEF08_LEAKAGE_GUARD",
            "expression_layer": "expression_leakage_guard",
            "source_columns": source_columns,
            "symbolic_slots": symbolic_slots,
            "frozen_expression": FROZEN_EXPRESSION,
            "dimensional_class": "pre_scoring_source_side_expression",
            "required_condition": "expression is frozen without observed velocity, residual, score, family-winner, or best-fit feedback",
            "observed_status": leakage_pass["overall_status"],
            "expression_freeze_decision": "COMBINED_ANCHOR_EXPRESSION_LEAKAGE_GUARD_FROZEN",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08",
        },
        {
            "expression_freeze_id": "M0NDVACAEF08_VALUE_FREEZE",
            "expression_layer": "combined_anchor_value_freeze",
            "source_columns": source_columns,
            "symbolic_slots": symbolic_slots,
            "frozen_expression": FROZEN_EXPRESSION,
            "dimensional_class": "no_evaluated_anchor_values",
            "required_condition": "a later artifact must evaluate or freeze combined-anchor values before any velocity formula or predictions can be written",
            "observed_status": "NO_COMBINED_ANCHOR_VALUE_FREEZE_PRESENT",
            "expression_freeze_decision": "BLOCKED_COMBINED_ANCHOR_VALUE_FREEZE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["combined_anchor_expression_frozen"] = "true"
        row["combined_anchor_values_written"] = 0
        row["velocity_formula_written"] = "false"
        row["numeric_prediction_rows_written"] = 0
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_only_no_values_no_formula_no_predictions"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = sum(str(row["expression_freeze_decision"]).startswith("BLOCKED") for row in rows)
    frozen = sum(str(row["expression_freeze_decision"]).endswith("_FROZEN") for row in rows)
    return [
        {
            "summary_id": "M0_NO_DARK_VELOCITY_ANCHOR_COMBINED_ANCHOR_EXPRESSION_FREEZE_V08",
            "anchor_combined_anchor_expression_artifact": "m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08",
            "expression_freeze_checks": len(rows),
            "frozen_expression_checks": frozen,
            "blocked_expression_freeze_checks": blocked,
            "combined_anchor_expression_frozen": "true",
            "frozen_expression": FROZEN_EXPRESSION,
            "combined_anchor_values_written": 0,
            "velocity_formula_written": "false",
            "numeric_prediction_rows_written": 0,
            "families_with_numeric_predictions": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_ANCHOR_COMBINED_ANCHOR_EXPRESSION_FROZEN_BLOCKED_VALUE_FREEZE_MISSING",
            "next_required_artifact": "m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08",
            "claim_boundary": "m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_only_no_combined_values_no_velocity_formula_no_predictions_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08.md").write_text(
        """# M0 No-Dark Velocity-Anchor Combined Anchor Expression Freeze v08

**Doc class:** velocity-anchor combined-anchor expression-freeze gate
**Status:** exact symbolic expression frozen; combined-anchor values missing; no predictions

Script:

```text
scripts/build_m0_no_dark_velocity_anchor_combined_anchor_expression_freeze.py
```

Derived outputs:

```text
data/derived/m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08.csv
data/derived/m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_summary_v08.csv
```

This artifact closes the `m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08`
presence blocker by freezing the exact symbolic expression used for the
source-side M0 no-dark velocity anchor:

```text
v_anchor_sq_km2_s2 =
    (s_gas*w_gas*v_gas_km_s^2
   + s_disk*w_disk*v_disk_km_s^2
   + s_bulge*w_bulge*v_bulge_km_s^2) / n_anchor
```

The expression is a velocity-squared baryonic carrier. It combines only the
frozen SPARC source-side velocity components:

```text
v_gas_km_s;v_disk_km_s;v_bulge_km_s
```

with the frozen symbolic slots:

```text
w_gas;w_disk;w_bulge;s_gas;s_disk;s_bulge;n_anchor
```

The weight, sign, and normalization slots remain pre-scoring symbolic slots.
No observed velocity, endpoint residual, heldout score, family winner,
best-fit curve, posthoc fit quality, or numeric prediction value is allowed in
the expression-freeze route.

## Current Result

The expected status is:

```text
M0_NO_DARK_ANCHOR_COMBINED_ANCHOR_EXPRESSION_FROZEN_BLOCKED_VALUE_FREEZE_MISSING
```

The next required artifact is:

```text
m0_no_dark_velocity_anchor_combined_anchor_value_freeze_v08
```

## Claim Boundary

This gate freezes only the exact symbolic combined-anchor expression. It does not evaluate combined-anchor values, does not choose numeric weights or signs, does not write a velocity formula, does not write prediction rows, does not run endpoint scoring, and does not decide whether a dark-sector component is required.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = expression_freeze_rows()
    write_csv(DERIVED / "m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_v08.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_velocity_anchor_combined_anchor_expression_freeze_summary_v08.csv",
        summary(rows),
        [
            "summary_id",
            "anchor_combined_anchor_expression_artifact",
            "expression_freeze_checks",
            "frozen_expression_checks",
            "blocked_expression_freeze_checks",
            "combined_anchor_expression_frozen",
            "frozen_expression",
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
    print("PAPER11_M0_NO_DARK_VELOCITY_ANCHOR_COMBINED_ANCHOR_EXPRESSION_FREEZE_V08_BUILT")


if __name__ == "__main__":
    main()
