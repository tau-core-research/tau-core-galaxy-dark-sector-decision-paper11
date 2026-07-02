#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

NEXT_ARTIFACT = "numeric_parameter_count_table_final_values_v10.csv"
STATUS = "SHARED_INPUT_COUNT_DISCOUNT_POLICY_V10_READY_FINAL_NUMERIC_COUNTS_PENDING"
CLAIM_BOUNDARY = "shared_input_count_discount_policy_only_no_discount_no_final_counts_no_parsimony_no_scores"

FIELDS = [
    "policy_row_id",
    "shared_input_id",
    "input_component",
    "component_scope",
    "shared_input_status",
    "discount_policy_status",
    "shared_discount_count_value",
    "discount_rule",
    "final_count_input_allowed",
    "parsimony_input_allowed",
    "next_required_artifact",
    "forbidden_inputs",
    "endpoint_scoring_allowed",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "policy_artifact",
    "shared_input_status",
    "shared_input_rows_checked",
    "zero_discount_rows",
    "unresolved_rows",
    "shared_discount_policy_frozen",
    "shared_discount_count_total",
    "final_numeric_count_values_written",
    "parsimony_scores_written",
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


def shared_input_summary() -> dict[str, str]:
    rows = read_csv(DERIVED / "shared_scoring_input_table_summary_v06.csv")
    if len(rows) != 1:
        raise ValueError("expected one shared scoring-input summary row")
    return rows[0]


def policy_rows() -> list[dict[str, object]]:
    shared_rows = read_csv(DERIVED / "shared_scoring_input_table_v06.csv")
    summary = shared_input_summary()
    rows: list[dict[str, object]] = []
    for index, row in enumerate(shared_rows, start=1):
        rows.append(
            {
                "policy_row_id": f"SICDP10_{index:03d}",
                "shared_input_id": row["shared_input_id"],
                "input_component": row["input_component"],
                "component_scope": row["component_scope"],
                "shared_input_status": summary["overall_status"],
                "discount_policy_status": "RESOLVED_ZERO_NO_SHARED_INPUT_COUNT_DISCOUNT",
                "shared_discount_count_value": 0,
                "discount_rule": "shared family-independent input policies receive no negative parameter discount and no family-specific rescue credit; any later family-specific loader, mask, grid, uncertainty, or component exception must be counted or block scoring",
                "final_count_input_allowed": "true",
                "parsimony_input_allowed": "false",
                "next_required_artifact": NEXT_ARTIFACT,
                "forbidden_inputs": row["forbidden_inputs"],
                "endpoint_scoring_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    zero_rows = [row for row in rows if row["shared_discount_count_value"] == 0]
    unresolved = len(rows) - len(zero_rows)
    return [
        {
            "summary_id": "SHARED_INPUT_COUNT_DISCOUNT_POLICY_V10",
            "policy_artifact": "shared_input_count_discount_policy_v10",
            "shared_input_status": shared_input_summary()["overall_status"],
            "shared_input_rows_checked": len(rows),
            "zero_discount_rows": len(zero_rows),
            "unresolved_rows": unresolved,
            "shared_discount_policy_frozen": "true" if unresolved == 0 else "false",
            "shared_discount_count_total": sum(int(row["shared_discount_count_value"]) for row in rows),
            "final_numeric_count_values_written": 0,
            "parsimony_scores_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": STATUS if unresolved == 0 else "SHARED_INPUT_COUNT_DISCOUNT_POLICY_V10_BLOCKED",
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "shared_input_count_discount_policy_v10.md").write_text(
        f"""# Shared Input Count-Discount Policy v10

**Doc class:** shared input count-discount policy
**Status:** shared-input discount policy frozen at zero; final numeric counts pending
**Canonical parent:** Shared scoring input table v06

Script:

```text
scripts/build_shared_input_count_discount_policy.py
```

Derived outputs:

```text
data/derived/shared_input_count_discount_policy_v10.csv
data/derived/shared_input_count_discount_policy_summary_v10.csv
```

This artifact closes the shared-input count-discount blocker. It audits the six
family-independent shared input components and freezes the discount value at
zero for each component:

```text
RESOLVED_ZERO_NO_SHARED_INPUT_COUNT_DISCOUNT
```

The rule is intentionally conservative: common input policies do not receive a
negative parameter discount, and any later family-specific loader, mask, grid,
uncertainty, or component exception must be counted or must block scoring.

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This policy writes only shared-input discount-policy rows. It writes no final numeric parameter counts,
computes no parsimony penalty, computes no endpoint scores, compares no families,
and makes no dark-sector verdict.

Claim boundary:

```text
{CLAIM_BOUNDARY}
```
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = policy_rows()
    write_csv(DERIVED / "shared_input_count_discount_policy_v10.csv", rows, FIELDS)
    write_csv(DERIVED / "shared_input_count_discount_policy_summary_v10.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_SHARED_INPUT_COUNT_DISCOUNT_POLICY_V10_BUILT")


if __name__ == "__main__":
    main()
