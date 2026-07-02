#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

NEXT_ARTIFACT = "m2_benchmark_parameter_count_classification_v11.csv"
STATUS = "M2_BENCHMARK_PARAMETER_INVENTORY_V10_PRESENT_COUNTABILITY_CLASSIFICATION_PENDING"
CLAIM_BOUNDARY = "m2_benchmark_parameter_inventory_only_no_counts_no_values_no_predictions_no_scores"

FIELDS = [
    "inventory_row_id",
    "readiness_id",
    "family_id",
    "inventory_scope",
    "source_artifact",
    "source_row_id",
    "benchmark_component",
    "global_slot_name",
    "inventory_statement",
    "counting_policy",
    "countability_status",
    "count_value_written",
    "numeric_benchmark_value_written",
    "family_prediction_rows_written",
    "per_galaxy_privilege_written",
    "completion_status",
    "next_required_artifact",
    "forbidden_inputs",
    "endpoint_scoring_allowed",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "inventory_artifact",
    "readiness_id",
    "family_id",
    "inventory_rows",
    "profile_source_rows",
    "nuisance_source_rows",
    "inventory_rows_present",
    "countability_classified_rows",
    "numeric_count_values_written",
    "numeric_benchmark_values_written",
    "family_prediction_rows_written",
    "per_galaxy_privilege_values_written",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
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


def inventory_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    profile_rows = read_csv(DERIVED / "m2_benchmark_profile_table_v06.csv")
    nuisance_rows = read_csv(DERIVED / "m2_nuisance_policy_table_v06.csv")
    index = 1
    for row in profile_rows:
        rows.append(
            {
                "inventory_row_id": f"M2BPI10_{index:03d}",
                "readiness_id": "NCR05_M2_GLOBAL",
                "family_id": "M2",
                "inventory_scope": "benchmark_profile_parameters",
                "source_artifact": "m2_benchmark_profile_table_v06",
                "source_row_id": row["benchmark_profile_id"],
                "benchmark_component": row["profile_component"],
                "global_slot_name": row["profile_component"],
                "inventory_statement": row["frozen_statement"],
                "counting_policy": row["counting_policy"],
                "countability_status": "COUNTABILITY_CLASSIFICATION_PENDING",
                "count_value_written": 0,
                "numeric_benchmark_value_written": 0,
                "family_prediction_rows_written": 0,
                "per_galaxy_privilege_written": 0,
                "completion_status": "INVENTORY_PRESENT_COUNTABILITY_PENDING",
                "next_required_artifact": NEXT_ARTIFACT,
                "forbidden_inputs": row["forbidden_inputs"],
                "endpoint_scoring_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        index += 1
    for row in nuisance_rows:
        rows.append(
            {
                "inventory_row_id": f"M2BPI10_{index:03d}",
                "readiness_id": "NCR05_M2_GLOBAL",
                "family_id": "M2",
                "inventory_scope": "benchmark_profile_parameters",
                "source_artifact": "m2_nuisance_policy_table_v06",
                "source_row_id": row["nuisance_policy_id"],
                "benchmark_component": row["nuisance_component"],
                "global_slot_name": row["nuisance_component"],
                "inventory_statement": row["frozen_statement"],
                "counting_policy": row["counting_policy"],
                "countability_status": "COUNTABILITY_CLASSIFICATION_PENDING",
                "count_value_written": 0,
                "numeric_benchmark_value_written": 0,
                "family_prediction_rows_written": 0,
                "per_galaxy_privilege_written": 0,
                "completion_status": "INVENTORY_PRESENT_COUNTABILITY_PENDING",
                "next_required_artifact": NEXT_ARTIFACT,
                "forbidden_inputs": row["forbidden_inputs"],
                "endpoint_scoring_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        index += 1
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    profile_source_rows = sum(row["source_artifact"] == "m2_benchmark_profile_table_v06" for row in rows)
    nuisance_source_rows = sum(row["source_artifact"] == "m2_nuisance_policy_table_v06" for row in rows)
    classified = sum(row["countability_status"] != "COUNTABILITY_CLASSIFICATION_PENDING" for row in rows)
    return [
        {
            "summary_id": "M2_BENCHMARK_PARAMETER_INVENTORY_V10",
            "inventory_artifact": "m2_benchmark_parameter_inventory_v10",
            "readiness_id": "NCR05_M2_GLOBAL",
            "family_id": "M2",
            "inventory_rows": len(rows),
            "profile_source_rows": profile_source_rows,
            "nuisance_source_rows": nuisance_source_rows,
            "inventory_rows_present": len(rows),
            "countability_classified_rows": classified,
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
    (DOCS / "m2_benchmark_parameter_inventory_v10.md").write_text(
        f"""# M2 Benchmark Parameter Inventory v10

**Doc class:** M2 global benchmark-parameter inventory
**Reader role:** scoring-frontier parameter-count reviewer
**Status:** inventory present; countability classification pending
**Canonical parent:** numeric count readiness closure v09

Script:

```text
scripts/build_m2_benchmark_parameter_inventory.py
```

Derived outputs:

```text
data/derived/m2_benchmark_parameter_inventory_v10.csv
data/derived/m2_benchmark_parameter_inventory_summary_v10.csv
```

## Current Result

The inventory lifts the M2 benchmark-profile and nuisance-policy rows into a
global benchmark-parameter audit table. It records the profile-family,
halo-parameter, prior, profile-switch, stellar mass-to-light, gas-scaling,
uncertainty, nuisance-prior, shared-fairness, and prediction-handoff slots that
must be classified before any M2 numeric benchmark-parameter count can be
written.

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
verdict. It only makes the M2 global benchmark-parameter inventory explicit so
the next artifact can classify which slots are fixed, countable, disqualifying,
or still blocked.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = inventory_rows()
    write_csv(DERIVED / "m2_benchmark_parameter_inventory_v10.csv", rows, FIELDS)
    write_csv(DERIVED / "m2_benchmark_parameter_inventory_summary_v10.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_M2_BENCHMARK_PARAMETER_INVENTORY_V10_BUILT")


if __name__ == "__main__":
    main()
