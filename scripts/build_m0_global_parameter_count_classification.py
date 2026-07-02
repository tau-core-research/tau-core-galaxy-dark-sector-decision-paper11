#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

NEXT_ARTIFACT = "m0_global_parameter_count_value_ledger_v12.csv"
STATUS = "M0_GLOBAL_PARAMETER_COUNT_CLASSIFICATION_V11_READY_COUNT_VALUE_PENDING"
CLAIM_BOUNDARY = "m0_global_parameter_count_classification_only_no_numeric_counts_no_scores"

FIELDS = [
    "classification_row_id",
    "inventory_row_id",
    "readiness_id",
    "family_id",
    "global_slot_name",
    "slot_class",
    "countability_class",
    "countability_rule",
    "fixed_if",
    "counts_if",
    "disqualifies_if",
    "classification_status",
    "numeric_count_value_written",
    "numeric_value_written",
    "per_galaxy_privilege_value_written",
    "next_required_artifact",
    "forbidden_inputs",
    "endpoint_scoring_allowed",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "classification_artifact",
    "inventory_status",
    "classification_rows",
    "classified_rows",
    "fixed_or_neutral_classes",
    "count_if_adjustable_classes",
    "disqualifying_classes",
    "numeric_count_values_written",
    "numeric_values_written",
    "per_galaxy_privilege_values_written",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

CLASSIFICATION_RULES = {
    "source_state": {
        "countability_class": "COUNT_IF_ADJUSTABLE_SOURCE_STATE_OR_POST_FREEZE_SWITCH",
        "countability_rule": "source-state slots are count-neutral only when frozen source-side; adjustable source-state coefficients or post-freeze morphology switches count",
        "fixed_if": "source_state_is_frozen_from_pre_score_source_records",
        "counts_if": "adjustable_source_state_coefficient_or_post_freeze_morphology_switch_is_used",
        "disqualifies_if": "source_state_is_chosen_from_endpoint_residuals_or_family_winner",
    },
    "no_dark_constraint": {
        "countability_class": "FIXED_FAMILY_GUARD_DISQUALIFIES_IF_COMPENSATOR",
        "countability_rule": "the no-dark marker is a fixed M0 eligibility guard; a hidden dark-response-like coefficient disqualifies M0 rather than becoming an uncounted parameter",
        "fixed_if": "dimensionless_no_dark_family_marker_is_preserved",
        "counts_if": "none_inside_M0",
        "disqualifies_if": "hidden_dark_sector_amplitude_scale_density_or_response_coefficient_is_used",
    },
    "baryonic_input": {
        "countability_class": "COUNT_IF_ADJUSTABLE_BARYONIC_NORMALIZATION_OR_SCALE",
        "countability_rule": "baryonic bindings are count-neutral only when shared and source-side; adjustable normalization, scale, or mass-model privilege counts",
        "fixed_if": "baryonic_input_and_units_are_shared_source_side_records",
        "counts_if": "adjustable_baryonic_normalization_scale_or_mass_model_privilege_is_used",
        "disqualifies_if": "baryonic_proxy_or_normalization_is_selected_from_best_fit_curve_quality",
    },
    "readout_operator": {
        "countability_class": "COUNT_IF_ADJUSTABLE_READOUT_OPERATOR_PARAMETER",
        "countability_rule": "readout operators are count-neutral only as fixed symbolic operators; adjustable amplitude, radial scale, threshold, or kernel-shape parameters count",
        "fixed_if": "readout_operator_is_predeclared_symbolic_or_source_side_fixed",
        "counts_if": "adjustable_readout_amplitude_radial_scale_threshold_or_kernel_shape_parameter_is_used",
        "disqualifies_if": "operator_is_selected_by_heldout_score_or_family_winner",
    },
    "failure_route": {
        "countability_class": "COUNT_IF_EXCEPTION_OR_RESCUE_ROUTE_IS_NUMERIC",
        "countability_rule": "null, blocked, and fallback routes are guards; per-galaxy exceptions or rescue coefficients count at full weight and cannot be hidden globally",
        "fixed_if": "route_is_explicit_null_blocked_missing_or_fallback_guard_without_numeric_rescue",
        "counts_if": "per_galaxy_exception_failure_route_rescue_or_numeric_fallback_parameter_is_used",
        "disqualifies_if": "silent_exception_bypasses_missing_symbolic_or_input_requirements",
    },
    "assembly": {
        "countability_class": "AGGREGATE_AUDIT_ROW_CHILD_SLOTS_COUNT",
        "countability_rule": "assembly is an audit container; child adjustable coefficients, scales, switches, and privileges count in the value ledger",
        "fixed_if": "assembly_order_is_predeclared_and_contains_no_additional_numeric_degree_of_freedom",
        "counts_if": "assembly_introduces_adjustable_coefficient_scale_switch_or_privilege",
        "disqualifies_if": "assembly_is_reordered_or_augmented_after_endpoint_residual_inspection",
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def inventory_status() -> str:
    rows = read_csv(DERIVED / "m0_global_parameter_inventory_summary_v10.csv")
    return rows[0]["overall_status"]


def classification_rows() -> list[dict[str, object]]:
    inventory = read_csv(DERIVED / "m0_global_parameter_inventory_v10.csv")
    out: list[dict[str, object]] = []
    for index, row in enumerate(inventory, start=1):
        rule = CLASSIFICATION_RULES[row["global_slot_name"]]
        out.append(
            {
                "classification_row_id": f"M0GPCC11_{index:03d}",
                "inventory_row_id": row["inventory_row_id"],
                "readiness_id": row["readiness_id"],
                "family_id": row["family_id"],
                "global_slot_name": row["global_slot_name"],
                "slot_class": row["slot_class"],
                "countability_class": rule["countability_class"],
                "countability_rule": rule["countability_rule"],
                "fixed_if": rule["fixed_if"],
                "counts_if": rule["counts_if"],
                "disqualifies_if": rule["disqualifies_if"],
                "classification_status": "CLASSIFIED_COUNT_VALUE_PENDING",
                "numeric_count_value_written": 0,
                "numeric_value_written": 0,
                "per_galaxy_privilege_value_written": 0,
                "next_required_artifact": NEXT_ARTIFACT,
                "forbidden_inputs": row["forbidden_inputs"],
                "endpoint_scoring_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    fixed = sum(str(row["countability_class"]).startswith("FIXED_") for row in rows)
    disqualifying = sum("DISQUALIFIES" in str(row["countability_class"]) for row in rows)
    count_if = sum("COUNT_IF" in str(row["countability_class"]) for row in rows)
    return [
        {
            "summary_id": "M0_GLOBAL_PARAMETER_COUNT_CLASSIFICATION_V11",
            "classification_artifact": "m0_global_parameter_count_classification_v11",
            "inventory_status": inventory_status(),
            "classification_rows": len(rows),
            "classified_rows": sum(row["classification_status"] == "CLASSIFIED_COUNT_VALUE_PENDING" for row in rows),
            "fixed_or_neutral_classes": fixed,
            "count_if_adjustable_classes": count_if,
            "disqualifying_classes": disqualifying,
            "numeric_count_values_written": 0,
            "numeric_values_written": 0,
            "per_galaxy_privilege_values_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": STATUS,
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_global_parameter_count_classification_v11.md").write_text(
        f"""# M0 Global Parameter Count Classification v11

**Doc class:** M0 global parameter countability classification
**Reader role:** scoring-frontier parameter-count reviewer
**Status:** countability classified; numeric count values pending
**Canonical parent:** M0 global parameter inventory v10

Script:

```text
scripts/build_m0_global_parameter_count_classification.py
```

Derived outputs:

```text
data/derived/m0_global_parameter_count_classification_v11.csv
data/derived/m0_global_parameter_count_classification_summary_v11.csv
```

## Current Result

The v11 classification assigns each M0 global slot a countability rule. It
distinguishes fixed source-side guards from adjustable parameters, explicit
per-galaxy or rescue privileges, and disqualifying hidden dark-compensation
routes.

The expected status is:

```text
{STATUS}
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This artifact writes no final numeric parameter count, no coefficient values,
no per-galaxy privilege count, no parsimony penalty, no endpoint scores, and no
dark-sector verdict. It only classifies how each global M0 slot must be treated
by the later numeric count-value ledger.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = classification_rows()
    write_csv(DERIVED / "m0_global_parameter_count_classification_v11.csv", rows, FIELDS)
    write_csv(
        DERIVED / "m0_global_parameter_count_classification_summary_v11.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER11_M0_GLOBAL_PARAMETER_COUNT_CLASSIFICATION_V11_BUILT")


if __name__ == "__main__":
    main()
