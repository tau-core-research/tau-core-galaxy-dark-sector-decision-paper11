#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

NEXT_ARTIFACT = "m1_response_parameter_count_classification_v11.csv"
STATUS = "M1_RESPONSE_PARAMETER_INVENTORY_V10_PRESENT_COUNTABILITY_CLASSIFICATION_PENDING"
CLAIM_BOUNDARY = "m1_response_parameter_inventory_only_no_counts_no_values_no_scores"

FIELDS = [
    "inventory_row_id",
    "readiness_id",
    "family_id",
    "inventory_scope",
    "source_response_table_id",
    "source_admissibility_id",
    "response_component",
    "global_slot_name",
    "inventory_statement",
    "admissibility_rule",
    "countability_status",
    "count_value_written",
    "numeric_response_value_written",
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
    "inventory_rows_present",
    "countability_classified_rows",
    "numeric_count_values_written",
    "numeric_response_values_written",
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


def admissibility_by_component() -> dict[str, dict[str, str]]:
    rows = read_csv(DERIVED / "m1_admissibility_table_v06.csv")
    return {row["response_component"]: row for row in rows}


def inventory_rows() -> list[dict[str, object]]:
    response_rows = read_csv(DERIVED / "m1_tau_response_formula_table_v06.csv")
    admissibility = admissibility_by_component()
    rows: list[dict[str, object]] = []
    for index, row in enumerate(response_rows, start=1):
        adm = admissibility[row["response_component"]]
        rows.append(
            {
                "inventory_row_id": f"M1RPI10_{index:03d}",
                "readiness_id": "NCR05_M1_GLOBAL",
                "family_id": "M1",
                "inventory_scope": "global_response_parameters",
                "source_response_table_id": row["response_table_id"],
                "source_admissibility_id": adm["admissibility_id"],
                "response_component": row["response_component"],
                "global_slot_name": row["response_component"],
                "inventory_statement": row["frozen_statement"],
                "admissibility_rule": adm["admissibility_rule"],
                "countability_status": "COUNTABILITY_CLASSIFICATION_PENDING",
                "count_value_written": 0,
                "numeric_response_value_written": 0,
                "per_galaxy_privilege_written": 0,
                "completion_status": "INVENTORY_PRESENT_COUNTABILITY_PENDING",
                "next_required_artifact": NEXT_ARTIFACT,
                "forbidden_inputs": row["forbidden_inputs"],
                "endpoint_scoring_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    classified = sum(row["countability_status"] != "COUNTABILITY_CLASSIFICATION_PENDING" for row in rows)
    return [
        {
            "summary_id": "M1_RESPONSE_PARAMETER_INVENTORY_V10",
            "inventory_artifact": "m1_response_parameter_inventory_v10",
            "readiness_id": "NCR05_M1_GLOBAL",
            "family_id": "M1",
            "inventory_rows": len(rows),
            "inventory_rows_present": len(rows),
            "countability_classified_rows": classified,
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
    (DOCS / "m1_response_parameter_inventory_v10.md").write_text(
        f"""# M1 Response Parameter Inventory v10

**Doc class:** M1 global response-parameter inventory
**Reader role:** scoring-frontier parameter-count reviewer
**Status:** inventory present; countability classification pending
**Canonical parent:** numeric count readiness closure v09

Script:

```text
scripts/build_m1_response_parameter_inventory.py
```

Derived outputs:

```text
data/derived/m1_response_parameter_inventory_v10.csv
data/derived/m1_response_parameter_inventory_summary_v10.csv
```

## Current Result

The inventory lifts the M1 response formula-table and admissibility-table rows
into a global response-parameter audit table. It records the activation,
carrier, amplitude, scale, handoff, and zero-response policy slots that must be
classified before any M1 numeric response-parameter count can be written.

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
penalty, no endpoint scores, and no dark-sector verdict. It only makes the M1
global response-parameter inventory explicit so the next artifact can classify
which slots are fixed, countable, disqualifying, or still blocked.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = inventory_rows()
    write_csv(DERIVED / "m1_response_parameter_inventory_v10.csv", rows, FIELDS)
    write_csv(DERIVED / "m1_response_parameter_inventory_summary_v10.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_M1_RESPONSE_PARAMETER_INVENTORY_V10_BUILT")


if __name__ == "__main__":
    main()
