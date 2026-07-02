#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/source_manifest"
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

NEXT_ARTIFACT = "numeric_count_readiness_closure_v09.csv"
BLOCKED_STATUS = "NUMERIC_PARAMETER_COUNT_TABLE_V08_BLOCKED_BY_COUNT_READINESS"
FINAL_VALUES_STATUS = "NUMERIC_PARAMETER_COUNT_TABLE_V08_BLOCKED_ON_FINAL_NUMERIC_COUNT_VALUES"
READY_STATUS = "NUMERIC_PARAMETER_COUNT_TABLE_V08_READY_FOR_PARSIMONY_INPUT"
FINAL_VALUES_ARTIFACT = "numeric_parameter_count_table_final_values_v10.csv"

FIELDS = [
    "count_value_row_id",
    "readiness_id",
    "family_id",
    "count_domain",
    "readiness_status",
    "blocked_by",
    "minimum_completion_condition",
    "final_numeric_count_status",
    "numeric_parameter_count_value",
    "per_galaxy_privilege_count_value",
    "parsimony_input_allowed",
    "next_required_artifact",
    "forbidden_inputs",
    "endpoint_scoring_allowed",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "count_artifact",
    "source_contract_status",
    "readiness_rows_checked",
    "blocked_count_rows",
    "numeric_count_values_written",
    "per_galaxy_privilege_values_written",
    "parsimony_scores_written",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]


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


def source_contract_status() -> str:
    rows = read_csv(DERIVED / "numeric_parameter_count_table_summary_v06.csv")
    if not rows:
        return "NUMERIC_PARAMETER_COUNT_TABLE_V06_MISSING"
    return rows[0]["overall_status"]


def closure_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "numeric_count_readiness_closure_summary_v09.csv")
    return rows[0] if rows else {}


def value_rows() -> list[dict[str, object]]:
    readiness = read_csv(SOURCE / "numeric_count_readiness_v05.csv")
    closure = closure_summary()
    closure_ready = closure.get("overall_status") == "NUMERIC_COUNT_READINESS_CLOSURE_READY_FOR_FINAL_COUNTS"
    out: list[dict[str, object]] = []
    for index, row in enumerate(readiness, start=1):
        ready = row["count_readiness_status"] == "COUNT_READY" or closure_ready
        out.append(
            {
                "count_value_row_id": f"NPCT08_{index:03d}",
                "readiness_id": row["readiness_id"],
                "family_id": row["family_id"],
                "count_domain": row["count_domain"],
                "readiness_status": row["count_readiness_status"],
                "blocked_by": row["blocked_by"],
                "minimum_completion_condition": row["minimum_completion_condition"],
                "final_numeric_count_status": "FINAL_NUMERIC_COUNT_VALUE_PENDING_EXPLICIT_FINAL_VALUES"
                if closure_ready
                else "FINAL_NUMERIC_COUNT_VALUE_READY"
                if ready
                else "FINAL_NUMERIC_COUNT_VALUE_BLOCKED",
                "numeric_parameter_count_value": "VALUE_PENDING_READINESS_CLOSURE",
                "per_galaxy_privilege_count_value": "VALUE_PENDING_READINESS_CLOSURE",
                "parsimony_input_allowed": "false",
                "next_required_artifact": FINAL_VALUES_ARTIFACT
                if closure_ready
                else "none"
                if ready
                else NEXT_ARTIFACT,
                "forbidden_inputs": row["forbidden_inputs"],
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "numeric_parameter_count_table_v08_only_no_parsimony_no_scores_no_verdict",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = sum(row["final_numeric_count_status"] != "FINAL_NUMERIC_COUNT_VALUE_READY" for row in rows)
    closure_ready = closure_summary().get("overall_status") == "NUMERIC_COUNT_READINESS_CLOSURE_READY_FOR_FINAL_COUNTS"
    return [
        {
            "summary_id": "NUMERIC_PARAMETER_COUNT_TABLE_V08",
            "count_artifact": "numeric_parameter_count_table_v08",
            "source_contract_status": source_contract_status(),
            "readiness_rows_checked": len(rows),
            "blocked_count_rows": blocked,
            "numeric_count_values_written": 0,
            "per_galaxy_privilege_values_written": 0,
            "parsimony_scores_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": FINAL_VALUES_STATUS if closure_ready else BLOCKED_STATUS if blocked else READY_STATUS,
            "next_required_artifact": FINAL_VALUES_ARTIFACT
            if closure_ready
            else NEXT_ARTIFACT
            if blocked
            else "control_runner_outputs_v08.csv",
            "claim_boundary": "numeric_parameter_count_table_v08_only_no_parsimony_no_scores_no_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "numeric_parameter_count_table_v08.md").write_text(
        f"""# Numeric Parameter Count Table v08

**Doc class:** numeric parameter-count value gate
**Status:** final numeric counts blocked by readiness closure; no scoring

Script:

```text
scripts/build_numeric_parameter_count_table_v08.py
```

Derived outputs:

```text
data/derived/numeric_parameter_count_table_v08.csv
data/derived/numeric_parameter_count_table_summary_v08.csv
```

This artifact attempts to open the final numeric parameter-count table required
by endpoint scoring. It reads the frozen v06 count-rule contract and the
`numeric_count_readiness_v05` ledger, then records that final numeric count
values remain blocked until the count-readiness rows are closed.

## Current Result

The expected status is:

```text
{BLOCKED_STATUS}
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This table writes no final numeric parameter counts, no per-galaxy privilege
counts, no parsimony penalty, no endpoint scores, and no dark-sector verdict.
It only turns the broad v08 blocker into explicit count-readiness closure
work.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = value_rows()
    write_csv(DERIVED / "numeric_parameter_count_table_v08.csv", rows, FIELDS)
    write_csv(DERIVED / "numeric_parameter_count_table_summary_v08.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_NUMERIC_PARAMETER_COUNT_TABLE_V08_BUILT")


if __name__ == "__main__":
    main()
