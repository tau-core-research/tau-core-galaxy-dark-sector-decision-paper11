#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

NEXT_ARTIFACT = "m2_benchmark_parameter_final_count_candidate_v14.csv"
STATUS = "M2_BENCHMARK_PARAMETER_ADJUSTABLE_SLOT_RESOLUTION_V13_READY_FOR_FINAL_COUNT_CANDIDATE"
CLAIM_BOUNDARY = "m2_benchmark_parameter_adjustable_slot_resolution_only_no_final_k_no_values_no_predictions_no_scores"

FIELDS = [
    "resolution_row_id",
    "ledger_row_id",
    "classification_row_id",
    "readiness_id",
    "family_id",
    "benchmark_component",
    "countability_class",
    "prior_count_value_status",
    "slot_resolution_status",
    "slot_count_value",
    "resolution_evidence",
    "adjustable_benchmark_parameter_found",
    "final_count_candidate_input_allowed",
    "benchmark_value_input_allowed",
    "parsimony_input_allowed",
    "next_required_artifact",
    "forbidden_inputs",
    "endpoint_scoring_allowed",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "resolution_artifact",
    "ledger_status",
    "conditional_rows_checked",
    "resolved_zero_rows",
    "unresolved_rows",
    "adjustable_benchmark_parameters_found",
    "final_m2_global_count_candidate_ready",
    "final_m2_global_count_written",
    "numeric_benchmark_values_written",
    "family_prediction_rows_written",
    "parsimony_scores_written",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

EVIDENCE_REQUIREMENTS = {
    "profile_family_registry": [
        ("m2_benchmark_profile_table_v06.csv", "benchmark_profile_id", "M2BPT06_PROFILE_FAMILY", "profile_table_status", "READY"),
        ("m2_benchmark_profile_table_v06.csv", "benchmark_profile_id", "M2BPT06_PROFILE_FAMILY", "numeric_profile_values_written", "0"),
        ("m2_benchmark_profile_table_v06.csv", "benchmark_profile_id", "M2BPT06_PROFILE_FAMILY", "family_prediction_rows_written", "0"),
    ],
    "halo_parameter_slots": [
        ("m2_benchmark_profile_table_v06.csv", "benchmark_profile_id", "M2BPT06_HALO_PARAMETERS", "profile_table_status", "READY"),
        ("m2_benchmark_profile_table_v06.csv", "benchmark_profile_id", "M2BPT06_HALO_PARAMETERS", "numeric_profile_values_written", "0"),
        ("m2_benchmark_profile_table_v06.csv", "benchmark_profile_id", "M2BPT06_HALO_PARAMETERS", "family_prediction_rows_written", "0"),
    ],
    "prior_policy": [
        ("m2_benchmark_profile_table_v06.csv", "benchmark_profile_id", "M2BPT06_PRIOR_POLICY", "profile_table_status", "READY"),
        ("m2_benchmark_profile_table_v06.csv", "benchmark_profile_id", "M2BPT06_PRIOR_POLICY", "numeric_profile_values_written", "0"),
        ("m2_benchmark_profile_table_v06.csv", "benchmark_profile_id", "M2BPT06_PRIOR_POLICY", "family_prediction_rows_written", "0"),
    ],
    "profile_switch_policy": [
        ("m2_benchmark_profile_table_v06.csv", "benchmark_profile_id", "M2BPT06_PROFILE_SWITCH", "profile_table_status", "READY"),
        ("m2_benchmark_profile_table_v06.csv", "benchmark_profile_id", "M2BPT06_PROFILE_SWITCH", "numeric_profile_values_written", "0"),
        ("m2_benchmark_profile_table_v06.csv", "benchmark_profile_id", "M2BPT06_PROFILE_SWITCH", "family_prediction_rows_written", "0"),
    ],
    "stellar_mass_to_light_policy": [
        ("m2_nuisance_policy_table_v06.csv", "nuisance_policy_id", "M2NPT06_STELLAR_MASS_TO_LIGHT", "nuisance_policy_status", "READY"),
        ("m2_nuisance_policy_table_v06.csv", "nuisance_policy_id", "M2NPT06_STELLAR_MASS_TO_LIGHT", "numeric_nuisance_values_written", "0"),
        ("m2_nuisance_policy_table_v06.csv", "nuisance_policy_id", "M2NPT06_STELLAR_MASS_TO_LIGHT", "family_prediction_rows_written", "0"),
    ],
    "gas_scaling_policy": [
        ("m2_nuisance_policy_table_v06.csv", "nuisance_policy_id", "M2NPT06_GAS_SCALING", "nuisance_policy_status", "READY"),
        ("m2_nuisance_policy_table_v06.csv", "nuisance_policy_id", "M2NPT06_GAS_SCALING", "numeric_nuisance_values_written", "0"),
        ("shared_scoring_input_table_v06.csv", "shared_input_id", "SSIT06_BARYONIC_COMPONENTS", "shared_input_status", "READY"),
    ],
    "uncertainty_policy": [
        ("m2_nuisance_policy_table_v06.csv", "nuisance_policy_id", "M2NPT06_UNCERTAINTY", "nuisance_policy_status", "READY"),
        ("m2_nuisance_policy_table_v06.csv", "nuisance_policy_id", "M2NPT06_UNCERTAINTY", "numeric_nuisance_values_written", "0"),
        ("shared_scoring_input_table_v06.csv", "shared_input_id", "SSIT06_UNCERTAINTY", "shared_input_status", "READY"),
    ],
    "nuisance_prior_policy": [
        ("m2_nuisance_policy_table_v06.csv", "nuisance_policy_id", "M2NPT06_PRIORS", "nuisance_policy_status", "READY"),
        ("m2_nuisance_policy_table_v06.csv", "nuisance_policy_id", "M2NPT06_PRIORS", "numeric_nuisance_values_written", "0"),
        ("m2_nuisance_policy_table_v06.csv", "nuisance_policy_id", "M2NPT06_PRIORS", "family_prediction_rows_written", "0"),
    ],
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


def require_value(filename: str, id_field: str, row_id: str, status_field: str, ready_value: str) -> str:
    rows = read_csv(DERIVED / filename)
    matches = [row for row in rows if row[id_field] == row_id]
    if len(matches) != 1:
        raise ValueError(f"expected one {row_id} row in {filename}")
    status = matches[0][status_field]
    if status != ready_value:
        raise ValueError(f"{row_id} in {filename} has {status_field}={status}, expected {ready_value}")
    return f"{filename}:{row_id}:{status_field}={ready_value}"


def ledger_status() -> str:
    rows = read_csv(DERIVED / "m2_benchmark_parameter_count_value_ledger_summary_v12.csv")
    return rows[0]["overall_status"]


def resolution_rows() -> list[dict[str, object]]:
    ledger = read_csv(DERIVED / "m2_benchmark_parameter_count_value_ledger_v12.csv")
    conditional = [row for row in ledger if row["resolution_needed"] == "true"]
    out: list[dict[str, object]] = []
    for index, row in enumerate(conditional, start=1):
        component = row["benchmark_component"]
        evidence = [
            require_value(filename, id_field, row_id, status_field, ready_value)
            for filename, id_field, row_id, status_field, ready_value in EVIDENCE_REQUIREMENTS[component]
        ]
        out.append(
            {
                "resolution_row_id": f"M2BPASR13_{index:03d}",
                "ledger_row_id": row["ledger_row_id"],
                "classification_row_id": row["classification_row_id"],
                "readiness_id": row["readiness_id"],
                "family_id": row["family_id"],
                "benchmark_component": component,
                "countability_class": row["countability_class"],
                "prior_count_value_status": row["count_value_status"],
                "slot_resolution_status": "RESOLVED_ZERO_NO_ACTIVE_BENCHMARK_SLOT_UNDER_CURRENT_SCAFFOLD",
                "slot_count_value": "0",
                "resolution_evidence": ";".join(evidence),
                "adjustable_benchmark_parameter_found": "false",
                "final_count_candidate_input_allowed": "true",
                "benchmark_value_input_allowed": "false",
                "parsimony_input_allowed": "false",
                "next_required_artifact": NEXT_ARTIFACT,
                "forbidden_inputs": row["forbidden_inputs"],
                "endpoint_scoring_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    unresolved = sum(
        row["slot_resolution_status"] != "RESOLVED_ZERO_NO_ACTIVE_BENCHMARK_SLOT_UNDER_CURRENT_SCAFFOLD"
        for row in rows
    )
    adjustable = sum(row["adjustable_benchmark_parameter_found"] == "true" for row in rows)
    ready = unresolved == 0 and adjustable == 0
    return [
        {
            "summary_id": "M2_BENCHMARK_PARAMETER_ADJUSTABLE_SLOT_RESOLUTION_V13",
            "resolution_artifact": "m2_benchmark_parameter_adjustable_slot_resolution_v13",
            "ledger_status": ledger_status(),
            "conditional_rows_checked": len(rows),
            "resolved_zero_rows": sum(row["slot_count_value"] == "0" for row in rows),
            "unresolved_rows": unresolved,
            "adjustable_benchmark_parameters_found": adjustable,
            "final_m2_global_count_candidate_ready": "true" if ready else "false",
            "final_m2_global_count_written": "false",
            "numeric_benchmark_values_written": 0,
            "family_prediction_rows_written": 0,
            "parsimony_scores_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": STATUS if ready else "M2_BENCHMARK_PARAMETER_ADJUSTABLE_SLOT_RESOLUTION_V13_UNRESOLVED",
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m2_benchmark_parameter_adjustable_slot_resolution_v13.md").write_text(
        f"""# M2 Benchmark Parameter Adjustable Slot Resolution v13

**Doc class:** M2 benchmark-parameter adjustable-slot resolution ledger
**Reader role:** scoring-frontier parameter-count reviewer
**Status:** conditional M2 benchmark/nuisance slots resolved for final-count candidate
**Canonical parent:** M2 benchmark parameter count-value ledger v12

Script:

```text
scripts/build_m2_benchmark_parameter_adjustable_slot_resolution.py
```

Derived outputs:

```text
data/derived/m2_benchmark_parameter_adjustable_slot_resolution_v13.csv
data/derived/m2_benchmark_parameter_adjustable_slot_resolution_summary_v13.csv
```

## Current Result

The v13 resolution checks the eight conditional M2 benchmark and nuisance slots
left open by the v12 count-value ledger: profile-family registry,
halo/profile-parameter slots, prior policy, profile-switch policy, stellar
mass-to-light policy, gas-scaling policy, uncertainty policy, and
nuisance-prior policy. Each slot is resolved as a zero-count slot only for the
present scaffold state, where the profile and nuisance policy tables are
`READY` but still write no numeric benchmark values, no M2 prediction rows, no
parsimony values, and no endpoint scores.

The expected status is:

```text
{STATUS}
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This artifact does not prove that benchmark or dark-sector models are
physically absent, does not write a final M2 global parameter count, does not
write benchmark/profile values, does not write nuisance values, does not emit
M2 prediction rows, does not compute parsimony, does not authorize endpoint
scoring, and does not decide the dark-sector question. It only records that
the present M2 scaffold has no active adjustable benchmark/nuisance slot before
a later final-count candidate.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = resolution_rows()
    write_csv(DERIVED / "m2_benchmark_parameter_adjustable_slot_resolution_v13.csv", rows, FIELDS)
    write_csv(
        DERIVED / "m2_benchmark_parameter_adjustable_slot_resolution_summary_v13.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER11_M2_BENCHMARK_PARAMETER_ADJUSTABLE_SLOT_RESOLUTION_V13_BUILT")


if __name__ == "__main__":
    main()
