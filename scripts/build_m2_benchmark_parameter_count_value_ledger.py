#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

NEXT_ARTIFACT = "m2_benchmark_parameter_adjustable_slot_resolution_v13.csv"
STATUS = "M2_BENCHMARK_PARAMETER_COUNT_VALUE_LEDGER_V12_PARTIAL_VALUES_READY_ADJUSTABLE_SLOT_RESOLUTION_PENDING"
CLAIM_BOUNDARY = "m2_benchmark_parameter_count_value_ledger_only_no_final_k_no_values_no_predictions_no_scores"

FIELDS = [
    "ledger_row_id",
    "classification_row_id",
    "readiness_id",
    "family_id",
    "benchmark_component",
    "countability_class",
    "count_value_status",
    "slot_count_value",
    "count_value_rule",
    "resolution_needed",
    "resolution_reason",
    "final_m2_global_count_input_allowed",
    "benchmark_value_input_allowed",
    "parsimony_input_allowed",
    "next_required_artifact",
    "forbidden_inputs",
    "endpoint_scoring_allowed",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "ledger_artifact",
    "classification_status",
    "ledger_rows",
    "resolved_zero_rows",
    "conditional_pending_rows",
    "numeric_slot_count_values_written",
    "final_m2_global_count_written",
    "numeric_benchmark_values_written",
    "family_prediction_rows_written",
    "parsimony_scores_written",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

VALUE_RULES = {
    "profile_family_registry": {
        "count_value_status": "CONDITIONAL_COUNT_VALUE_PENDING",
        "slot_count_value": "VALUE_PENDING_BENCHMARK_SLOT_RESOLUTION",
        "count_value_rule": "0 if a single source-fixed profile convention is used; otherwise count each active profile-family or switch privilege",
        "resolution_needed": "true",
        "resolution_reason": "requires evidence that profile-family freedom is fixed or explicitly counted before scoring",
    },
    "halo_parameter_slots": {
        "count_value_status": "CONDITIONAL_COUNT_VALUE_PENDING",
        "slot_count_value": "VALUE_PENDING_BENCHMARK_SLOT_RESOLUTION",
        "count_value_rule": "0 only for public fixed benchmark conventions; otherwise count declared halo/profile scale, density, velocity, shape, core, or transition parameters",
        "resolution_needed": "true",
        "resolution_reason": "requires declared benchmark profile parameter policy before an M2 global count can be frozen",
    },
    "prior_policy": {
        "count_value_status": "CONDITIONAL_COUNT_VALUE_PENDING",
        "slot_count_value": "VALUE_PENDING_BENCHMARK_SLOT_RESOLUTION",
        "count_value_rule": "0 if prior widths and bounds are fixed by public or predeclared convention; otherwise count adjustable prior and bound freedoms",
        "resolution_needed": "true",
        "resolution_reason": "requires evidence that profile prior widths and bounds are not endpoint-tuned freedoms",
    },
    "nuisance_policy_link": {
        "count_value_status": "RESOLVED_ZERO_PROTOCOL_HANDOFF_CONTAINER",
        "slot_count_value": "0",
        "count_value_rule": "handoff contributes zero direct parameters when it only records dependency order and delegates child nuisance slots",
        "resolution_needed": "false",
        "resolution_reason": "protocol container without direct numeric benchmark degree of freedom",
    },
    "profile_switch_policy": {
        "count_value_status": "CONDITIONAL_COUNT_VALUE_PENDING",
        "slot_count_value": "VALUE_PENDING_BENCHMARK_SLOT_RESOLUTION",
        "count_value_rule": "0 if profile switching is disallowed; otherwise count predeclared profile-switch privileges",
        "resolution_needed": "true",
        "resolution_reason": "requires evidence that no profile-switch privilege is active or that it is explicitly counted",
    },
    "prediction_handoff": {
        "count_value_status": "RESOLVED_ZERO_PREDICTION_HANDOFF_GUARD",
        "slot_count_value": "0",
        "count_value_rule": "prediction handoff contributes zero direct parameters while M2 prediction rows remain blocked",
        "resolution_needed": "false",
        "resolution_reason": "blocked handoff route without direct benchmark value or prediction-row privilege",
    },
    "stellar_mass_to_light_policy": {
        "count_value_status": "CONDITIONAL_COUNT_VALUE_PENDING",
        "slot_count_value": "VALUE_PENDING_BENCHMARK_SLOT_RESOLUTION",
        "count_value_rule": "0 if stellar mass-to-light is source-fixed; otherwise count fitted values, prior widths, or population switches",
        "resolution_needed": "true",
        "resolution_reason": "requires source-side nuisance policy evidence before an M2 global count can be frozen",
    },
    "gas_scaling_policy": {
        "count_value_status": "CONDITIONAL_COUNT_VALUE_PENDING",
        "slot_count_value": "VALUE_PENDING_BENCHMARK_SLOT_RESOLUTION",
        "count_value_rule": "0 if gas scaling and component inclusion are shared source-side records; otherwise count adjustable gas/component privileges",
        "resolution_needed": "true",
        "resolution_reason": "requires evidence that gas scaling and baryonic component choices are fixed or counted",
    },
    "uncertainty_policy": {
        "count_value_status": "CONDITIONAL_COUNT_VALUE_PENDING",
        "slot_count_value": "VALUE_PENDING_BENCHMARK_SLOT_RESOLUTION",
        "count_value_rule": "0 if the uncertainty model is source-fixed; otherwise count adjustable error floors, covariance choices, weights, or rescalings",
        "resolution_needed": "true",
        "resolution_reason": "requires evidence that uncertainty policy was not tuned from endpoint residuals",
    },
    "nuisance_prior_policy": {
        "count_value_status": "CONDITIONAL_COUNT_VALUE_PENDING",
        "slot_count_value": "VALUE_PENDING_BENCHMARK_SLOT_RESOLUTION",
        "count_value_rule": "0 if nuisance priors are public or predeclared fixed values; otherwise count fitted prior widths, bounds, centers, or switches",
        "resolution_needed": "true",
        "resolution_reason": "requires source-side nuisance prior resolution before count freeze",
    },
    "shared_baryonic_fairness_policy": {
        "count_value_status": "RESOLVED_ZERO_SHARED_INPUT_GUARD",
        "slot_count_value": "0",
        "count_value_rule": "shared-input fairness contributes zero direct parameters when it only enforces equal inputs across families",
        "resolution_needed": "false",
        "resolution_reason": "shared fairness guard without family-specific exception under the current scaffold",
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


def classification_status() -> str:
    rows = read_csv(DERIVED / "m2_benchmark_parameter_count_classification_summary_v11.csv")
    return rows[0]["overall_status"]


def ledger_rows() -> list[dict[str, object]]:
    classified = read_csv(DERIVED / "m2_benchmark_parameter_count_classification_v11.csv")
    out: list[dict[str, object]] = []
    for index, row in enumerate(classified, start=1):
        rule = VALUE_RULES[row["benchmark_component"]]
        pending = rule["resolution_needed"] == "true"
        out.append(
            {
                "ledger_row_id": f"M2BPCVL12_{index:03d}",
                "classification_row_id": row["classification_row_id"],
                "readiness_id": row["readiness_id"],
                "family_id": row["family_id"],
                "benchmark_component": row["benchmark_component"],
                "countability_class": row["countability_class"],
                "count_value_status": rule["count_value_status"],
                "slot_count_value": rule["slot_count_value"],
                "count_value_rule": rule["count_value_rule"],
                "resolution_needed": rule["resolution_needed"],
                "resolution_reason": rule["resolution_reason"],
                "final_m2_global_count_input_allowed": "false",
                "benchmark_value_input_allowed": "false",
                "parsimony_input_allowed": "false",
                "next_required_artifact": NEXT_ARTIFACT if pending else "none_until_benchmark_slot_resolution",
                "forbidden_inputs": row["forbidden_inputs"],
                "endpoint_scoring_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    resolved_zero = sum(str(row["slot_count_value"]) == "0" for row in rows)
    conditional = sum(str(row["resolution_needed"]) == "true" for row in rows)
    return [
        {
            "summary_id": "M2_BENCHMARK_PARAMETER_COUNT_VALUE_LEDGER_V12",
            "ledger_artifact": "m2_benchmark_parameter_count_value_ledger_v12",
            "classification_status": classification_status(),
            "ledger_rows": len(rows),
            "resolved_zero_rows": resolved_zero,
            "conditional_pending_rows": conditional,
            "numeric_slot_count_values_written": resolved_zero,
            "final_m2_global_count_written": "false",
            "numeric_benchmark_values_written": 0,
            "family_prediction_rows_written": 0,
            "parsimony_scores_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": STATUS,
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m2_benchmark_parameter_count_value_ledger_v12.md").write_text(
        f"""# M2 Benchmark Parameter Count Value Ledger v12

**Doc class:** M2 benchmark-parameter count-value ledger
**Reader role:** scoring-frontier parameter-count reviewer
**Status:** partial slot values ready; benchmark-slot resolution pending
**Canonical parent:** M2 benchmark parameter count classification v11

Script:

```text
scripts/build_m2_benchmark_parameter_count_value_ledger.py
```

Derived outputs:

```text
data/derived/m2_benchmark_parameter_count_value_ledger_v12.csv
data/derived/m2_benchmark_parameter_count_value_ledger_summary_v12.csv
```

## Current Result

The v12 ledger converts the v11 M2 benchmark-slot countability classes into
slot-level count-value rows. Protocol handoff, prediction handoff, and
shared-input guard rows receive zero slot values. Profile-family, halo/profile,
prior, switch, stellar mass-to-light, gas, uncertainty, and nuisance-prior
slots remain conditional until a later benchmark-slot resolution proves whether
each freedom is fixed, absent, or countable.

The expected status is:

```text
{STATUS}
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This artifact writes no final M2 global parameter count, no benchmark/profile
value, no nuisance value, no M2 prediction row, no per-galaxy benchmark
privilege count, no parsimony penalty, no endpoint scores, and no dark-sector
verdict. It only records slot-level count-value rules and the remaining
benchmark-slot evidence needed before a final M2 global count can be formed.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = ledger_rows()
    write_csv(DERIVED / "m2_benchmark_parameter_count_value_ledger_v12.csv", rows, FIELDS)
    write_csv(
        DERIVED / "m2_benchmark_parameter_count_value_ledger_summary_v12.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER11_M2_BENCHMARK_PARAMETER_COUNT_VALUE_LEDGER_V12_BUILT")


if __name__ == "__main__":
    main()
