#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDS = [
    "benchmark_profile_id",
    "family_id",
    "formula_slot",
    "profile_component",
    "component_scope",
    "frozen_statement",
    "allowed_values",
    "counting_policy",
    "forbidden_inputs",
    "profile_table_status",
    "numeric_profile_values_written",
    "family_prediction_rows_written",
    "endpoint_scoring_allowed",
    "next_required_artifact",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "benchmark_profile_artifact",
    "family_id",
    "formula_slot",
    "profile_components",
    "numeric_profile_values_written",
    "family_prediction_rows_written",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

NEXT_ARTIFACT = "m2_nuisance_policy_table_v06"
FORBIDDEN_INPUTS = (
    "endpoint_residual;heldout_score;family_winner;best_fit_curve;"
    "posthoc_profile_switch;posthoc_prior_width;numeric_score_value"
)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def profile_rows() -> list[dict[str, object]]:
    base = {
        "family_id": "M2",
        "formula_slot": "benchmark_profile_formula",
        "forbidden_inputs": FORBIDDEN_INPUTS,
        "profile_table_status": "READY",
        "numeric_profile_values_written": "0",
        "family_prediction_rows_written": "0",
        "endpoint_scoring_allowed": "false",
        "next_required_artifact": NEXT_ARTIFACT,
        "claim_boundary": "m2_benchmark_profile_table_only_no_profile_values_no_predictions_no_scores_no_validation",
    }
    return [
        {
            **base,
            "benchmark_profile_id": "M2BPT06_PROFILE_FAMILY",
            "profile_component": "profile_family_registry",
            "component_scope": "standard_benchmark_profile_family_policy",
            "frozen_statement": "M2 profile families must be declared before endpoint scoring and cannot be selected from held-out performance.",
            "allowed_values": "single_primary_profile_or_predeclared_profile_menu_with_counted_switch_policy",
            "counting_policy": "each active profile family or switch privilege must be counted by the later parameter-count table",
        },
        {
            **base,
            "benchmark_profile_id": "M2BPT06_HALO_PARAMETERS",
            "profile_component": "halo_parameter_slots",
            "component_scope": "benchmark_halo_parameter_declarations",
            "frozen_statement": "Halo/profile parameter slots may be declared here, but no numeric halo parameters are written before scoring gates close.",
            "allowed_values": "radius_scale_slot;density_or_velocity_scale_slot;shape_or_core_slot_if_profile_requires_it",
            "counting_policy": "all declared halo/profile parameters count unless fixed by a source-side public benchmark convention",
        },
        {
            **base,
            "benchmark_profile_id": "M2BPT06_PRIOR_POLICY",
            "profile_component": "prior_policy",
            "component_scope": "profile_prior_width_and_bounds_policy",
            "frozen_statement": "Prior widths and bounds must be frozen before scoring and cannot be widened after seeing residuals.",
            "allowed_values": "public_convention_prior;predeclared_broad_prior;predeclared_fixed_prior",
            "counting_policy": "post-freeze prior changes count as endpoint tuning privileges and invalidate the frozen profile slot",
        },
        {
            **base,
            "benchmark_profile_id": "M2BPT06_NUISANCE_HANDOFF",
            "profile_component": "nuisance_policy_link",
            "component_scope": "stellar_gas_uncertainty_and_baryonic_nuisance_handoff",
            "frozen_statement": "Benchmark profile use is blocked until a separate nuisance policy freezes stellar, gas, uncertainty, and prior-handling rules.",
            "allowed_values": "HANDOFF_TO_M2_NUISANCE_POLICY_TABLE",
            "counting_policy": "nuisance privileges are counted in the later M2 nuisance and parameter-count gates",
        },
        {
            **base,
            "benchmark_profile_id": "M2BPT06_PROFILE_SWITCH",
            "profile_component": "profile_switch_policy",
            "component_scope": "wrong_family_and_profile_shopping_guard",
            "frozen_statement": "Switching profile families after endpoint inspection is forbidden unless the switch policy was frozen and counted before scoring.",
            "allowed_values": "NO_POSTHOC_PROFILE_SWITCH;COUNTED_PREDECLARED_SWITCH_POLICY",
            "counting_policy": "unfrozen profile switching blocks M2 verdict eligibility",
        },
        {
            **base,
            "benchmark_profile_id": "M2BPT06_PREDICTION_HANDOFF",
            "profile_component": "prediction_handoff",
            "component_scope": "family_prediction_table_handoff",
            "frozen_statement": "M2 cannot write family prediction rows until nuisance, numeric parameter count, and benchmark value gates are closed.",
            "allowed_values": "NO_M2_PREDICTION_ROWS;HANDOFF_BLOCKED_PENDING_NUISANCE_POLICY",
            "counting_policy": "prediction rows remain blocked and cannot be used as endpoint scores",
        },
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "M2_BENCHMARK_PROFILE_TABLE_V06",
            "benchmark_profile_artifact": "m2_benchmark_profile_table_v06",
            "family_id": "M2",
            "formula_slot": "benchmark_profile_formula",
            "profile_components": len(rows),
            "numeric_profile_values_written": "0",
            "family_prediction_rows_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M2_BENCHMARK_PROFILE_TABLE_READY_NUISANCE_BLOCKED",
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": "m2_benchmark_profile_table_only_no_profile_values_no_predictions_no_scores_no_validation",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m2_benchmark_profile_table_v06.md").write_text(
        f"""# M2 Benchmark Profile Table v06

**Doc class:** M2 benchmark-profile table contract
**Status:** benchmark profile table ready; nuisance policy blocked; no scoring

Script:

```text
scripts/build_m2_benchmark_profile_table.py
```

Derived outputs:

```text
data/derived/m2_benchmark_profile_table_v06.csv
data/derived/m2_benchmark_profile_table_summary_v06.csv
```

This artifact fills the M2 `benchmark_profile_formula` slot as a pre-scoring
contract. It freezes the benchmark profile-family policy, halo-parameter slot
policy, prior policy, nuisance-policy handoff, profile-switch guard, and
prediction handoff.

## Current Result

The expected status is:

```text
M2_BENCHMARK_PROFILE_TABLE_READY_NUISANCE_BLOCKED
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This table does not validate the standard dark sector, does not prove an M2
endpoint result, writes no numeric profile values, writes no M2 prediction
rows, computes no endpoint scores, and makes no dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = profile_rows()
    write_csv(DERIVED / "m2_benchmark_profile_table_v06.csv", rows, FIELDS)
    write_csv(DERIVED / "m2_benchmark_profile_table_summary_v06.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_M2_BENCHMARK_PROFILE_TABLE_V06_BUILT")


if __name__ == "__main__":
    main()
