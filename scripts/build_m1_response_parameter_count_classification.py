#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

NEXT_ARTIFACT = "m1_response_parameter_count_value_ledger_v12.csv"
STATUS = "M1_RESPONSE_PARAMETER_COUNT_CLASSIFICATION_V11_READY_COUNT_VALUE_PENDING"
CLAIM_BOUNDARY = "m1_response_parameter_count_classification_only_no_counts_no_values_no_scores"

FIELDS = [
    "classification_row_id",
    "inventory_row_id",
    "readiness_id",
    "family_id",
    "response_component",
    "global_slot_name",
    "countability_class",
    "countability_rule",
    "fixed_if",
    "counts_if",
    "disqualifies_if",
    "classification_status",
    "numeric_count_value_written",
    "numeric_response_value_written",
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
    "numeric_response_values_written",
    "per_galaxy_privilege_values_written",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

CLASSIFICATION_RULES = {
    "activation_rule": {
        "countability_class": "FIXED_ADMISSIBILITY_GUARD_COUNTS_IF_ROW_SPECIFIC_SWITCH",
        "countability_rule": "M1 activation is count-neutral only as a pre-scoring admissibility guard; row-specific or fitted activation switches count",
        "fixed_if": "activation_rule_is_predeclared_and_source_side",
        "counts_if": "row_specific_activation_switch_or_fitted_activation_threshold_is_used",
        "disqualifies_if": "activation_is_chosen_from_endpoint_residuals_or_family_winner",
    },
    "carrier": {
        "countability_class": "FIXED_PLACEHOLDER_COUNTS_IF_PHYSICAL_CARRIER_PARAMETERIZED",
        "countability_rule": "the carrier placeholder is count-neutral as protocol structure; a parameterized physical response carrier counts after lawful declaration",
        "fixed_if": "carrier_remains_protocol_placeholder_without_numeric_degree_of_freedom",
        "counts_if": "carrier_amplitude_density_scale_kernel_or_shape_parameter_is_introduced",
        "disqualifies_if": "carrier_type_is_selected_or_retyped_from_endpoint_score",
    },
    "amplitude_law": {
        "countability_class": "COUNT_IF_ADJUSTABLE_RESPONSE_AMPLITUDE",
        "countability_rule": "response amplitude is not written here; any later adjustable amplitude, normalization, or strength parameter counts",
        "fixed_if": "amplitude_law_is_absent_or_fully_source_frozen_without_numeric_response_degree",
        "counts_if": "adjustable_response_amplitude_normalization_or_strength_parameter_is_used",
        "disqualifies_if": "amplitude_is_tuned_to_rescue_residuals_or_heldout_score",
    },
    "scale_law": {
        "countability_class": "COUNT_IF_ADJUSTABLE_RESPONSE_SCALE",
        "countability_rule": "response scale is count-neutral only when absent or source-frozen; adjustable radial, mass, morphology, or transition scales count",
        "fixed_if": "scale_law_is_absent_or_fully_source_frozen_before_scoring",
        "counts_if": "adjustable_response_radial_mass_morphology_or_transition_scale_is_used",
        "disqualifies_if": "scale_is_selected_from_radial_zone_score_improvement",
    },
    "channel_handoff": {
        "countability_class": "FIXED_PROTOCOL_HANDOFF_CHILD_SLOTS_COUNT",
        "countability_rule": "handoff is an audit container; it is count-neutral only when it adds no response degree of freedom",
        "fixed_if": "handoff_order_and_dependencies_are_predeclared",
        "counts_if": "handoff_introduces_adjustable_response_weight_switch_or_privilege",
        "disqualifies_if": "handoff_is_reordered_after_endpoint_residual_inspection",
    },
    "zero_response_policy": {
        "countability_class": "FIXED_NULL_ROUTE_COUNTS_IF_RESCUE_TERM",
        "countability_rule": "zero-response policy is a fixed null/failure route; numeric rescue terms or exceptions count at full weight",
        "fixed_if": "inactive_missing_or_inadmissible_routes_are_explicit_zero_response_cases",
        "counts_if": "numeric_zero_response_exception_rescue_or_fallback_parameter_is_used",
        "disqualifies_if": "silent_nonzero_fallback_bypasses_response_admissibility",
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
    rows = read_csv(DERIVED / "m1_response_parameter_inventory_summary_v10.csv")
    return rows[0]["overall_status"]


def classification_rows() -> list[dict[str, object]]:
    inventory = read_csv(DERIVED / "m1_response_parameter_inventory_v10.csv")
    out: list[dict[str, object]] = []
    for index, row in enumerate(inventory, start=1):
        rule = CLASSIFICATION_RULES[row["response_component"]]
        out.append(
            {
                "classification_row_id": f"M1RPCC11_{index:03d}",
                "inventory_row_id": row["inventory_row_id"],
                "readiness_id": row["readiness_id"],
                "family_id": row["family_id"],
                "response_component": row["response_component"],
                "global_slot_name": row["global_slot_name"],
                "countability_class": rule["countability_class"],
                "countability_rule": rule["countability_rule"],
                "fixed_if": rule["fixed_if"],
                "counts_if": rule["counts_if"],
                "disqualifies_if": rule["disqualifies_if"],
                "classification_status": "CLASSIFIED_COUNT_VALUE_PENDING",
                "numeric_count_value_written": 0,
                "numeric_response_value_written": 0,
                "per_galaxy_privilege_value_written": 0,
                "next_required_artifact": NEXT_ARTIFACT,
                "forbidden_inputs": row["forbidden_inputs"],
                "endpoint_scoring_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    fixed = sum("FIXED" in str(row["countability_class"]) for row in rows)
    count_if = sum("COUNT_IF" in str(row["countability_class"]) for row in rows)
    disqualifying = sum("DISQUALIFIES" in str(row["countability_class"]) for row in rows)
    return [
        {
            "summary_id": "M1_RESPONSE_PARAMETER_COUNT_CLASSIFICATION_V11",
            "classification_artifact": "m1_response_parameter_count_classification_v11",
            "inventory_status": inventory_status(),
            "classification_rows": len(rows),
            "classified_rows": sum(row["classification_status"] == "CLASSIFIED_COUNT_VALUE_PENDING" for row in rows),
            "fixed_or_guard_classes": fixed,
            "count_if_adjustable_classes": count_if,
            "disqualifying_classes": disqualifying,
            "numeric_count_values_written": 0,
            "numeric_response_values_written": 0,
            "per_galaxy_privilege_values_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": STATUS,
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m1_response_parameter_count_classification_v11.md").write_text(
        f"""# M1 Response Parameter Count Classification v11

**Doc class:** M1 response-parameter countability classification
**Reader role:** scoring-frontier parameter-count reviewer
**Status:** countability classified; count-value ledger pending
**Canonical parent:** M1 response parameter inventory v10

Script:

```text
scripts/build_m1_response_parameter_count_classification.py
```

Derived outputs:

```text
data/derived/m1_response_parameter_count_classification_v11.csv
data/derived/m1_response_parameter_count_classification_summary_v11.csv
```

## Current Result

The v11 classification assigns countability rules to the six M1 response
slots. It separates fixed protocol/admissibility guards from slots that count
if they later become adjustable response amplitudes, scales, carriers,
switches, handoffs, or rescue routes.

The expected status is:

```text
{STATUS}
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This artifact writes no final numeric parameter count, no response value, no
Response_tau formula, no per-galaxy response privilege count, no parsimony
penalty, no endpoint scores, and no dark-sector verdict. It only classifies how
M1 response slots must be treated by the later count-value ledger.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = classification_rows()
    write_csv(DERIVED / "m1_response_parameter_count_classification_v11.csv", rows, FIELDS)
    write_csv(
        DERIVED / "m1_response_parameter_count_classification_summary_v11.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER11_M1_RESPONSE_PARAMETER_COUNT_CLASSIFICATION_V11_BUILT")


if __name__ == "__main__":
    main()
