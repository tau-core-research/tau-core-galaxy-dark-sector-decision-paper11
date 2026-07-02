#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/source_manifest"
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDS = [
    "count_row_id",
    "family_id",
    "component",
    "count_scope",
    "count_rule_source",
    "frozen_count_rule",
    "count_value_status",
    "numeric_count_value",
    "counting_policy",
    "forbidden_inputs",
    "endpoint_scoring_allowed",
    "next_required_artifact",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "count_artifact",
    "shared_input_status",
    "count_rows",
    "numeric_count_values_written",
    "parsimony_scores_written",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

READY_STATUS = "NUMERIC_PARAMETER_COUNT_TABLE_CONTRACT_READY_FINAL_COUNTS_BLOCKED"
NEXT_ARTIFACT = "numeric_parameter_count_table_v08.csv"


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


def shared_input_status() -> str:
    rows = read_csv(DERIVED / "shared_scoring_input_table_summary_v06.csv")
    if not rows:
        return "SHARED_SCORING_INPUT_TABLE_MISSING"
    return rows[0]["overall_status"]


def count_rows() -> list[dict[str, object]]:
    rows = read_csv(SOURCE / "family_parameter_count_freeze_v03.csv")
    out: list[dict[str, object]] = []
    for index, row in enumerate(rows, start=1):
        out.append(
            {
                "count_row_id": f"NPCT06_{index:03d}",
                "family_id": row["family_id"],
                "component": row["component"],
                "count_scope": "global_or_per_galaxy_privilege_rule",
                "count_rule_source": row["row_id"],
                "frozen_count_rule": row["parameter_count_policy"],
                "count_value_status": "FINAL_NUMERIC_COUNT_VALUE_BLOCKED_UNTIL_V08",
                "numeric_count_value": "VALUE_NOT_WRITTEN_IN_V06",
                "counting_policy": row["decision_use"],
                "forbidden_inputs": row["forbidden_inputs"],
                "endpoint_scoring_allowed": "false",
                "next_required_artifact": NEXT_ARTIFACT,
                "claim_boundary": "numeric_parameter_count_table_contract_only_no_final_counts_no_parsimony_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "NUMERIC_PARAMETER_COUNT_TABLE_V06",
            "count_artifact": "numeric_parameter_count_table_v06",
            "shared_input_status": shared_input_status(),
            "count_rows": len(rows),
            "numeric_count_values_written": "0",
            "parsimony_scores_written": "0",
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": READY_STATUS,
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": "numeric_parameter_count_table_contract_only_no_final_counts_no_parsimony_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "numeric_parameter_count_table_v06.md").write_text(
        f"""# Numeric Parameter Count Table v06

**Doc class:** numeric parameter-count contract
**Status:** count-rule ledger ready; final numeric counts blocked; no scoring

Script:

```text
scripts/build_numeric_parameter_count_table.py
```

Derived outputs:

```text
data/derived/numeric_parameter_count_table_v06.csv
data/derived/numeric_parameter_count_table_summary_v06.csv
```

This artifact fills the `numeric_parameter_count_table` slot as a pre-scoring
count-rule ledger. It imports the frozen family count policies and exposes the
families/components that must receive final numeric counts before endpoint
scoring.

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

This table writes no final numeric count values, computes no parsimony penalty,
computes no endpoint scores, compares no families, and makes no dark-sector
verdict. It only closes the count-rule contract slot and hands off to the
final numeric count artifact.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = count_rows()
    write_csv(DERIVED / "numeric_parameter_count_table_v06.csv", rows, FIELDS)
    write_csv(DERIVED / "numeric_parameter_count_table_summary_v06.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_NUMERIC_PARAMETER_COUNT_TABLE_V06_BUILT")


if __name__ == "__main__":
    main()
