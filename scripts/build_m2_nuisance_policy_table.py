#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDS = [
    "nuisance_policy_id",
    "family_id",
    "formula_slot",
    "nuisance_component",
    "component_scope",
    "frozen_statement",
    "allowed_values",
    "counting_policy",
    "forbidden_inputs",
    "nuisance_policy_status",
    "numeric_nuisance_values_written",
    "family_prediction_rows_written",
    "endpoint_scoring_allowed",
    "next_required_artifact",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "nuisance_policy_artifact",
    "benchmark_profile_status",
    "family_id",
    "formula_slot",
    "nuisance_components",
    "numeric_nuisance_values_written",
    "family_prediction_rows_written",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

NEXT_ARTIFACT = "shared_scoring_input_table_v06"
READY_STATUS = "M2_NUISANCE_POLICY_TABLE_READY_SHARED_INPUTS_BLOCKED"
FORBIDDEN_INPUTS = (
    "endpoint_residual;heldout_score;family_winner;best_fit_curve;"
    "posthoc_prior_width;posthoc_uncertainty_policy;posthoc_baryonic_rescaling"
)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def benchmark_profile_status() -> str:
    rows = read_csv(DERIVED / "m2_benchmark_profile_table_summary_v06.csv")
    if not rows:
        return "M2_BENCHMARK_PROFILE_TABLE_MISSING"
    return rows[0]["overall_status"]


def policy_rows() -> list[dict[str, object]]:
    base = {
        "family_id": "M2",
        "formula_slot": "benchmark_nuisance_policy",
        "forbidden_inputs": FORBIDDEN_INPUTS,
        "nuisance_policy_status": "READY",
        "numeric_nuisance_values_written": "0",
        "family_prediction_rows_written": "0",
        "endpoint_scoring_allowed": "false",
        "next_required_artifact": NEXT_ARTIFACT,
        "claim_boundary": "m2_nuisance_policy_table_only_no_nuisance_values_no_predictions_no_scores_no_validation",
    }
    return [
        {
            **base,
            "nuisance_policy_id": "M2NPT06_STELLAR_MASS_TO_LIGHT",
            "nuisance_component": "stellar_mass_to_light_policy",
            "component_scope": "stellar_mass_to_light_handling_before_scoring",
            "frozen_statement": "Stellar mass-to-light handling must be declared before endpoint scoring and cannot be tuned from held-out residuals.",
            "allowed_values": "public_fixed_value;public_prior_range;predeclared_source_catalog_value",
            "counting_policy": "each fitted or switchable stellar mass-to-light degree of freedom must be counted by the later parameter-count gate",
        },
        {
            **base,
            "nuisance_policy_id": "M2NPT06_GAS_SCALING",
            "nuisance_component": "gas_scaling_policy",
            "component_scope": "gas_component_scaling_and_baryonic_component_guard",
            "frozen_statement": "Gas scaling and baryonic component inclusion rules must be fixed before endpoint residuals are inspected.",
            "allowed_values": "public_catalog_gas;predeclared_gas_scaling_factor;no_posthoc_component_drop",
            "counting_policy": "gas scaling privileges and component switches are counted if not fixed by a public convention",
        },
        {
            **base,
            "nuisance_policy_id": "M2NPT06_UNCERTAINTY",
            "nuisance_component": "uncertainty_policy",
            "component_scope": "measurement_uncertainty_and_error_floor_policy",
            "frozen_statement": "Uncertainty handling, error floors, and weighting choices must be frozen before any endpoint family comparison.",
            "allowed_values": "published_uncertainties;predeclared_error_floor;predeclared_covariance_policy",
            "counting_policy": "post-freeze uncertainty widening invalidates endpoint verdict eligibility",
        },
        {
            **base,
            "nuisance_policy_id": "M2NPT06_PRIORS",
            "nuisance_component": "nuisance_prior_policy",
            "component_scope": "nuisance_prior_width_bounds_and_source_policy",
            "frozen_statement": "Nuisance priors must be source-side or publicly predeclared and cannot be widened after seeing endpoint performance.",
            "allowed_values": "public_prior;predeclared_broad_prior;predeclared_fixed_nuisance_value",
            "counting_policy": "all nuisance priors with fitted freedom count toward the later numeric parameter-count table",
        },
        {
            **base,
            "nuisance_policy_id": "M2NPT06_SHARED_FAIRNESS",
            "nuisance_component": "shared_baryonic_fairness_policy",
            "component_scope": "cross_family_shared_baryonic_inputs",
            "frozen_statement": "Baryonic inputs used by M2 must be compatible with the shared scoring-input policy used for every family.",
            "allowed_values": "same_observed_grid;same_baryonic_source_table;same_masking_policy;same_uncertainty_policy",
            "counting_policy": "family-specific exceptions must be declared and counted before scoring or the endpoint remains blocked",
        },
        {
            **base,
            "nuisance_policy_id": "M2NPT06_PREDICTION_HANDOFF",
            "nuisance_component": "prediction_handoff",
            "component_scope": "shared_scoring_input_handoff",
            "frozen_statement": "M2 cannot write benchmark prediction rows until shared scoring inputs, parameter counts, controls, and thresholds are closed.",
            "allowed_values": "NO_M2_PREDICTION_ROWS;HANDOFF_BLOCKED_PENDING_SHARED_INPUTS",
            "counting_policy": "prediction rows remain blocked and cannot be used as endpoint scores",
        },
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "M2_NUISANCE_POLICY_TABLE_V06",
            "nuisance_policy_artifact": "m2_nuisance_policy_table_v06",
            "benchmark_profile_status": benchmark_profile_status(),
            "family_id": "M2",
            "formula_slot": "benchmark_nuisance_policy",
            "nuisance_components": len(rows),
            "numeric_nuisance_values_written": "0",
            "family_prediction_rows_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": READY_STATUS,
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": "m2_nuisance_policy_table_only_no_nuisance_values_no_predictions_no_scores_no_validation",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m2_nuisance_policy_table_v06.md").write_text(
        f"""# M2 Nuisance Policy Table v06

**Doc class:** M2 nuisance-policy table contract
**Status:** nuisance policy ready; shared scoring inputs blocked; no scoring

Script:

```text
scripts/build_m2_nuisance_policy_table.py
```

Derived outputs:

```text
data/derived/m2_nuisance_policy_table_v06.csv
data/derived/m2_nuisance_policy_table_summary_v06.csv
```

This artifact fills the M2 `benchmark_nuisance_policy` slot as a pre-scoring
contract. It freezes the stellar mass-to-light policy, gas scaling policy,
uncertainty policy, nuisance prior policy, shared baryonic fairness policy, and
prediction handoff before endpoint scoring.

## Current Result

The expected status is:

```text
{READY_STATUS}
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This table does not validate the standard dark sector, does not prove an M2
endpoint result, writes no numeric nuisance values, writes no M2 prediction
rows, computes no endpoint scores, and makes no dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = policy_rows()
    write_csv(DERIVED / "m2_nuisance_policy_table_v06.csv", rows, FIELDS)
    write_csv(DERIVED / "m2_nuisance_policy_table_summary_v06.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_M2_NUISANCE_POLICY_TABLE_V06_BUILT")


if __name__ == "__main__":
    main()
