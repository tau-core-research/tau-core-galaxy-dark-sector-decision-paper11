#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

NEXT_ARTIFACT = "m2_benchmark_parameter_count_value_ledger_v12.csv"
STATUS = "M2_BENCHMARK_PARAMETER_COUNT_CLASSIFICATION_V11_READY_COUNT_VALUE_PENDING"
CLAIM_BOUNDARY = "m2_benchmark_parameter_count_classification_only_no_counts_no_values_no_predictions_no_scores"

FIELDS = [
    "classification_row_id",
    "inventory_row_id",
    "readiness_id",
    "family_id",
    "source_artifact",
    "source_row_id",
    "benchmark_component",
    "global_slot_name",
    "countability_class",
    "countability_rule",
    "fixed_if",
    "counts_if",
    "disqualifies_if",
    "classification_status",
    "numeric_count_value_written",
    "numeric_benchmark_value_written",
    "family_prediction_rows_written",
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
    "fixed_or_guard_classes",
    "count_if_adjustable_classes",
    "disqualifying_classes",
    "numeric_count_values_written",
    "numeric_benchmark_values_written",
    "family_prediction_rows_written",
    "per_galaxy_privilege_values_written",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

CLASSIFICATION_RULES = {
    "profile_family_registry": {
        "countability_class": "COUNT_IF_ACTIVE_PROFILE_FAMILY_OR_SWITCH_PRIVILEGE",
        "countability_rule": "profile-family freedom counts unless the benchmark convention is source-fixed before scoring",
        "fixed_if": "single_profile_family_is_source_fixed_before_scoring",
        "counts_if": "profile_family_is_selected_fitted_or_switchable_for_endpoint_performance",
        "disqualifies_if": "profile_family_is_chosen_from_heldout_residuals_or_family_winner",
    },
    "halo_parameter_slots": {
        "countability_class": "COUNT_IF_DECLARED_HALO_OR_PROFILE_PARAMETER",
        "countability_rule": "declared halo/profile scale, density, velocity, shape, or core slots count unless source-fixed by public benchmark convention",
        "fixed_if": "all_halo_profile_slots_are_public_fixed_convention_values_before_scoring",
        "counts_if": "radius_density_velocity_shape_core_or_transition_parameter_is_fitted_or_free",
        "disqualifies_if": "halo_parameter_is_tuned_after_endpoint_residual_inspection",
    },
    "prior_policy": {
        "countability_class": "COUNT_IF_ADJUSTABLE_PROFILE_PRIOR_OR_BOUND",
        "countability_rule": "profile prior and bound choices count if adjustable, widened, or switched after source freeze",
        "fixed_if": "prior_widths_and_bounds_are_public_or_predeclared_before_scoring",
        "counts_if": "prior_width_bound_or_profile_prior_family_is_adjustable",
        "disqualifies_if": "prior_is_widened_or_recentered_after_seeing_endpoint_performance",
    },
    "nuisance_policy_link": {
        "countability_class": "FIXED_PROTOCOL_HANDOFF_CHILD_SLOTS_COUNT",
        "countability_rule": "nuisance handoff is count-neutral as an audit container; child nuisance freedoms count in their own rows",
        "fixed_if": "handoff_target_and_dependency_order_are_predeclared",
        "counts_if": "handoff_introduces_adjustable_benchmark_weight_switch_or_exception",
        "disqualifies_if": "handoff_is_reordered_after_endpoint_residual_inspection",
    },
    "profile_switch_policy": {
        "countability_class": "COUNT_IF_PREDECLARED_PROFILE_SWITCH_PRIVILEGE",
        "countability_rule": "profile switching counts as a benchmark privilege when allowed before scoring; post-hoc switching is disallowed",
        "fixed_if": "no_profile_switch_is_allowed_after_profile_family_freeze",
        "counts_if": "predeclared_profile_switch_menu_or_switch_parameter_is_allowed",
        "disqualifies_if": "profile_switch_is_selected_from_endpoint_score_improvement",
    },
    "stellar_mass_to_light_policy": {
        "countability_class": "COUNT_IF_FITTED_OR_SWITCHABLE_STELLAR_MASS_TO_LIGHT",
        "countability_rule": "stellar mass-to-light handling is count-neutral only when source-fixed or publicly convention-fixed",
        "fixed_if": "stellar_mass_to_light_is_public_fixed_or_source_catalog_value_before_scoring",
        "counts_if": "stellar_mass_to_light_value_prior_width_or_population_switch_is_fitted",
        "disqualifies_if": "stellar_mass_to_light_is_tuned_from_best_fit_curve_quality",
    },
    "gas_scaling_policy": {
        "countability_class": "COUNT_IF_ADJUSTABLE_GAS_SCALING_OR_COMPONENT_SWITCH",
        "countability_rule": "gas scaling and baryonic component choices count when adjustable or family-specific",
        "fixed_if": "gas_scaling_and_component_inclusion_are_shared_source_side_records",
        "counts_if": "gas_scaling_factor_component_switch_or_family_specific_component_exception_is_used",
        "disqualifies_if": "gas_or_baryonic_component_is_added_dropped_or_rescaled_after_endpoint_inspection",
    },
    "uncertainty_policy": {
        "countability_class": "COUNT_IF_ADJUSTABLE_UNCERTAINTY_MODEL_OR_ERROR_FLOOR",
        "countability_rule": "uncertainty handling counts when error floors, covariance choices, or weights are adjustable",
        "fixed_if": "published_uncertainties_or_predeclared_error_model_are_used_without_tuning",
        "counts_if": "error_floor_covariance_weight_or_uncertainty_rescaling_is_adjustable",
        "disqualifies_if": "uncertainty_is_widened_to_reduce_endpoint_penalty_after_residuals",
    },
    "nuisance_prior_policy": {
        "countability_class": "COUNT_IF_FITTED_NUISANCE_PRIOR_OR_BOUND",
        "countability_rule": "nuisance priors count when fitted, adjustable, or switchable before scoring",
        "fixed_if": "nuisance_priors_are_public_or_predeclared_fixed_values",
        "counts_if": "nuisance_prior_width_bound_center_or_family_is_fitted_or_switchable",
        "disqualifies_if": "nuisance_prior_is_changed_after_endpoint_family_comparison",
    },
    "shared_baryonic_fairness_policy": {
        "countability_class": "FIXED_SHARED_INPUT_GUARD_COUNTS_IF_FAMILY_EXCEPTION",
        "countability_rule": "shared baryonic fairness is count-neutral as a guard; family-specific exceptions count or block scoring",
        "fixed_if": "same_grid_same_baryonic_sources_same_masks_and_same_uncertainty_policy_are_used",
        "counts_if": "family_specific_baryonic_exception_mask_component_drop_or_input_discount_is_used",
        "disqualifies_if": "shared_input_policy_is_bypassed_for_m2_after_endpoint_inspection",
    },
    "prediction_handoff": {
        "countability_class": "FIXED_PREDICTION_HANDOFF_COUNTS_IF_ROW_WRITER_PRIVILEGE",
        "countability_rule": "prediction handoff is count-neutral as a blocked protocol route; row-writing privileges count later",
        "fixed_if": "prediction_rows_remain_blocked_pending_shared_inputs_counts_controls_and_thresholds",
        "counts_if": "handoff_introduces_row_writer_exception_benchmark_weight_or_family_specific_prediction_privilege",
        "disqualifies_if": "m2_prediction_rows_are_written_before_count_and_control_gates_close",
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
    rows = read_csv(DERIVED / "m2_benchmark_parameter_inventory_summary_v10.csv")
    return rows[0]["overall_status"]


def classification_rows() -> list[dict[str, object]]:
    inventory = read_csv(DERIVED / "m2_benchmark_parameter_inventory_v10.csv")
    out: list[dict[str, object]] = []
    for index, row in enumerate(inventory, start=1):
        rule = CLASSIFICATION_RULES[row["benchmark_component"]]
        out.append(
            {
                "classification_row_id": f"M2BPCC11_{index:03d}",
                "inventory_row_id": row["inventory_row_id"],
                "readiness_id": row["readiness_id"],
                "family_id": row["family_id"],
                "source_artifact": row["source_artifact"],
                "source_row_id": row["source_row_id"],
                "benchmark_component": row["benchmark_component"],
                "global_slot_name": row["global_slot_name"],
                "countability_class": rule["countability_class"],
                "countability_rule": rule["countability_rule"],
                "fixed_if": rule["fixed_if"],
                "counts_if": rule["counts_if"],
                "disqualifies_if": rule["disqualifies_if"],
                "classification_status": "CLASSIFIED_COUNT_VALUE_PENDING",
                "numeric_count_value_written": 0,
                "numeric_benchmark_value_written": 0,
                "family_prediction_rows_written": 0,
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
    count_if = sum("COUNT_IF" in str(row["countability_class"]) for row in rows)
    disqualifying = sum("DISQUALIFIES" in str(row["countability_class"]) for row in rows)
    return [
        {
            "summary_id": "M2_BENCHMARK_PARAMETER_COUNT_CLASSIFICATION_V11",
            "classification_artifact": "m2_benchmark_parameter_count_classification_v11",
            "inventory_status": inventory_status(),
            "classification_rows": len(rows),
            "classified_rows": sum(row["classification_status"] == "CLASSIFIED_COUNT_VALUE_PENDING" for row in rows),
            "fixed_or_guard_classes": fixed,
            "count_if_adjustable_classes": count_if,
            "disqualifying_classes": disqualifying,
            "numeric_count_values_written": 0,
            "numeric_benchmark_values_written": 0,
            "family_prediction_rows_written": 0,
            "per_galaxy_privilege_values_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": STATUS,
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m2_benchmark_parameter_count_classification_v11.md").write_text(
        f"""# M2 Benchmark Parameter Count Classification v11

**Doc class:** M2 benchmark-parameter countability classification
**Reader role:** scoring-frontier parameter-count reviewer
**Status:** countability classified; count-value ledger pending
**Canonical parent:** M2 benchmark parameter inventory v10

Script:

```text
scripts/build_m2_benchmark_parameter_count_classification.py
```

Derived outputs:

```text
data/derived/m2_benchmark_parameter_count_classification_v11.csv
data/derived/m2_benchmark_parameter_count_classification_summary_v11.csv
```

## Current Result

The v11 classification assigns countability rules to the twelve M2 benchmark
profile and nuisance slots. It separates fixed protocol/shared-input guards
from profile, halo, nuisance, prior, uncertainty, component, and switch
privileges that count if they become adjustable.

The expected status is:

```text
{STATUS}
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This artifact writes no final numeric parameter count, no benchmark/profile
value, no nuisance value, no M2 prediction row, no per-galaxy benchmark
privilege count, no parsimony penalty, no endpoint scores, and no dark-sector
verdict. It only classifies how M2 benchmark slots must be treated by the later
count-value ledger.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = classification_rows()
    write_csv(DERIVED / "m2_benchmark_parameter_count_classification_v11.csv", rows, FIELDS)
    write_csv(
        DERIVED / "m2_benchmark_parameter_count_classification_summary_v11.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER11_M2_BENCHMARK_PARAMETER_COUNT_CLASSIFICATION_V11_BUILT")


if __name__ == "__main__":
    main()
